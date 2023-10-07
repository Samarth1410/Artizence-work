import librosa
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import os
from main import app

def speech2text(filename):

    #load pre-trained model and tokenizer
    tokenizer = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
    model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

    #load any audio file of your choice
    # path = os.path.abspath(os.path.dirname(__file__))
    path = os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],filename)

    speech, rate = librosa.load(path,sr=16000)

    input_values = tokenizer(speech, return_tensors = 'pt',sampling_rate =rate).input_values

    logits = model(input_values).logits

    #Store predicted id's
    predicted_ids = torch.argmax(logits, dim =-1)

    transcriptions = tokenizer.decode(predicted_ids[0]) 

    os.remove(str(path))
    return transcriptions