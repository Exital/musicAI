import json
import os
import numpy as np
import music21 as m21
import torch.nn.functional as F
from .dataset import MusicDataset
from .model import LSTM
import torch
import random


def decode_to_parts(song):
    parts = []
    part = []
    for i in range(len(song[0].split(','))):
        for timestep in song:
            events = timestep.split(',')
            part.append(events[i])
        if not all(val == 'r' or val == '_' for val in part):
            parts.append(part)
        part = []
    return parts


class MelodyGenerator:
    def __init__(self, model_path, seq_len=64, device='cpu'):
        self.device = device
        self.model_path = model_path
        self.mapping_path = os.path.join(self.model_path, 'mapping.json')

        with open(self.mapping_path, "r") as fp:
            self._mappings = json.load(fp)

        if model_path is not None:
            self.model = LSTM(len(self._mappings), 256, len(self._mappings), self.mapping_path)
            self.model.load_state_dict(torch.load(os.path.join(self.model_path, 'model.pt'), map_location=self.device))

        self._start_symbols = ["/"] * seq_len

    def _sample_with_temperature(self, probabilities, temperature):
        """Samples an index from a probability array reapplying softmax using temperature
        :param predictions (nd.array): Array containing probabilities for each of the possible outputs.
        :param temperature (float): Float in interval [0, 1]. Numbers closer to 0 make the model more deterministic.
            A number closer to 1 makes the generation more unpredictable.
        :return index (int): Selected output symbol
        """
        probabilities -= torch.min(probabilities)
        predictions = torch.log(probabilities) / temperature
        probabilities = torch.exp(predictions) / torch.sum(torch.exp(predictions))

        choices = range(len(probabilities))
        index = np.random.choice(choices, p=probabilities.numpy())

        return index

    def generate_melody(self, num_steps, max_sequence_length, temperature, seed=None):
        # create seed with start symbols
        if seed is None:
            seed = self.random_seed()
        seed = seed.split()
        melody = seed
        seed = self._start_symbols + seed

        # map seed to int
        seed = [self._mappings[symbol] for symbol in seed]

        for _ in range(num_steps):

            # limit the seed to max_sequence_length
            seed = seed[-max_sequence_length:]

            sequence = MusicDataset.one_hot(np.array(seed), len(self._mappings))
            sequence = torch.from_numpy(sequence[np.newaxis, ...]).float()

            outputs = self.model(sequence)[0]
            probabilities = outputs.data.detach()
            probabilities = F.softmax(probabilities, dim=0)
            output_int = self._sample_with_temperature(probabilities, temperature)

            seed.append(output_int)

            output_symbol = [k for k, v in self._mappings.items() if v == output_int][0]

            # check whether we're at the end of a melody
            if output_symbol == "/":
                break

            # update melody
            melody.append(output_symbol)

        return melody

    def save_melody(self, melody, step_duration=0.25, format="midi", file_name="mel.mid"):
        """Converts a melody into a MIDI file
        :param melody (list of str):
        :param min_duration (float): Duration of each time step in quarter length
        :param file_name (str): Name of midi file
        :return:
        """
        parts = decode_to_parts(melody)
        # create a music21 stream
        stream = m21.stream.Stream()

        step_counter = 1
        for j, melody in enumerate(parts):
            start_symbol = None
            part = m21.stream.Part(id=f'part{j}')
            # parse all the symbols in the melody and create note/rest objects
            for i, symbol in enumerate(melody):

                # handle case in which we have a note/rest
                if symbol != "_" or i + 1 == len(melody):

                    # ensure we're dealing with note/rest beyond the first one
                    if start_symbol is not None:

                        quarter_length_duration = step_duration * step_counter  # 0.25 * 4 = 1

                        # handle rest
                        if start_symbol == "r":
                            m21_event = m21.note.Rest(quarterLength=quarter_length_duration)

                        # handle note
                        elif '.' not in start_symbol:
                            m21_event = m21.note.Note(int(start_symbol), quarterLength=quarter_length_duration)
                        # handle chord
                        else:
                            chord_list = start_symbol.split('.')
                            chord_list = [int(val) for val in chord_list]
                            m21_event = m21.chord.Chord(chord_list, quarterLength=quarter_length_duration)

                        part.append(m21_event)

                        # reset the step counter
                        step_counter = 1

                    start_symbol = symbol

                # handle case in which we have a prolongation sign "_"
                else:
                    step_counter += 1
            stream.insert(0, part)
        # write the m21 stream to a midi file
        stream.write(format, file_name)

    def random_seed(self):
        while True:
            key, value = random.choice(list(self._mappings.items()))
            if all(val not in [',', '_', '/'] for val in key.split(',')):
                return key
