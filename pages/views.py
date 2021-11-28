from django.shortcuts import render
import os
from rnn_lstm.src.melody_generation import MelodyGenerator
from rocket_webapp.settings import BASE_DIR
from rocket_webapp.settings import STATIC_ROOT
from music21 import instrument
from gan.src.utils import generate_samples


def pages_home(request):
    if request.method == 'POST':
        pressed = request.POST.get('pressed')
        print(pressed)
    return render(request, 'pages/index.html', {})


def rnn_preprocess_view(request):
    return render(request, 'pages/rnn_preprocess_inter.html')


def rnn_lstm_generate(request):
    if request.method == "POST":
        pressed = request.POST.get('pressed').split(',')
        if pressed != ['']:
            notes_to_midi = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71, 'Db': 64, 'Eb': 63, 'Gb': 66,
                             'Ab': 68, 'Bb': 70}
            seed = (' _ '.join([str(notes_to_midi[note]) for note in pressed]))
        else:
            seed = None
        trained_model = os.path.join(BASE_DIR, 'rnn_lstm', 'static', 'trained_models', 'trained_erk')
        gen = MelodyGenerator(trained_model)
        song = gen.generate_melody(500, 64, 0.85, seed=seed)
        if os.getenv('DEBUG'):
            mel_path = os.path.join(BASE_DIR, 'rnn_lstm', 'static', 'midi', 'generated', 'mel.mid')
        else:
            mel_path = os.path.join(STATIC_ROOT, 'midi', 'generated', 'mel.mid')
        gen.save_melody(song, file_name=mel_path)
        return render(request, 'pages/rnn_generate.html', {'generated': True})
    return render(request, 'pages/rnn_generate.html', {'generated': False})


def rnn_lstm_generate_multi(request):
    instruments = [instrument.UnpitchedPercussion(), instrument.Piano(),
                   instrument.ElectricBass(), instrument.StringInstrument()]
    if request.method == "POST":
        trained_model = os.path.join(BASE_DIR, 'rnn_lstm', 'static', 'trained_models', 'multi_tracks_model')
        gen = MelodyGenerator(trained_model)
        song = gen.generate_melody(500, 64, 0.85)
        if os.getenv('DEBUG'):
            mel_path = os.path.join(BASE_DIR, 'rnn_lstm', 'static', 'midi', 'generated', 'mel.mid')
        else:
            mel_path = os.path.join(STATIC_ROOT, 'midi', 'generated', 'mel.mid')
        gen.save_melody(song, file_name=mel_path, instruments=instruments)
        return render(request, 'pages/rnn_generate_multi.html', {'generated': True})
    return render(request, 'pages/rnn_generate_multi.html', {'generated': False})


def gan_generate(request):
    if request.method == "POST":
        trained_model = os.path.join(BASE_DIR, 'gan', 'static', 'gan_trained_models', 'modelA', 'generator.pt')
        if os.getenv('DEBUG'):
            mel_path = os.path.join(BASE_DIR, 'rnn_lstm', 'static', 'midi', 'generated', 'mel.mid')
        else:
            mel_path = os.path.join(STATIC_ROOT, 'midi', 'generated', 'mel.mid')
        generate_samples(trained_model, mel_path, num_samples=1, sample_name='mel.mid')
        return render(request, 'pages/gan_generate.html', {'generated': True})
    return render(request, 'pages/gan_generate.html', {'generated': False})
