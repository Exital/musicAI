"""talsplace URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from django.views.generic import TemplateView
from pages.views import *

app_name = 'pages'
urlpatterns = [
    # home
    path('', TemplateView.as_view(template_name='pages/index3.html'), name='home'),
    path('team', TemplateView.as_view(template_name='pages/the_team.html'), name='team'),

    # intro
    path('intro', TemplateView.as_view(template_name='pages/intro_to_midi.html'), name='intro'),

    # datasets
    path('dataset', TemplateView.as_view(template_name='pages/dataset.html'), name='dataset'),
    path('dataset/esac', TemplateView.as_view(template_name='pages/esac_dataset.html'), name='dataset-esac'),
    path('dataset/snes', TemplateView.as_view(template_name='pages/snes_dataset.html'), name='dataset-snes'),

    # RNN LSTM model
    path('rnn/preprocess', TemplateView.as_view(template_name='pages/rnn_preprocess.html'),
         name='rnn-preprocess'),
    path('rnn/preprocess/interactive', TemplateView.as_view(template_name='pages/rnn_preprocess_inter.html'),
         name='rnn-preprocess-inter'),
    path('rnn/generate', rnn_lstm_generate, name='rnn_lstm_generate'),
    path('rnn/intro', TemplateView.as_view(template_name='pages/rnn_intro.html'), name='rnn-intro'),
    path('rnn/training', TemplateView.as_view(template_name='pages/rnn_training.html'), name='rnn-training'),
    path('rnn/generate/multi', rnn_lstm_generate_multi, name='rnn_lstm_generate_multi'),

]
