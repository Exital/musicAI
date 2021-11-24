from django.shortcuts import render
import os
from rnn_lstm.src.melody_generation import MelodyGenerator
from rocket_webapp.settings import BASE_DIR


def pages_home(request):
    if request.method == 'POST':
        pressed = request.POST.get('pressed')
        print(pressed)
    return render(request, 'pages/index3.html', {})


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
        gen.save_melody(song, file_name=os.path.join(BASE_DIR, 'rnn_lstm/static/midi/generated/mel.mid'))
        return render(request, 'pages/rnn_generate.html', {'generated': True})
    return render(request, 'pages/rnn_generate.html', {'generated': False})
