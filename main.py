from flask import Flask, request, jsonify
import pandas as pd
import pyttsx3
import base64

app = Flask(__name__) # cria o site

def converter_audio_para_base64(caminho_arquivo):
    with open(caminho_arquivo, "rb") as arquivo_audio:
        audio_base64 = base64.b64encode(arquivo_audio.read())
        return audio_base64.decode('utf-8')  # Convertendo bytes para string

@app.route("/")
def teste():
    #data = request.json
    #frase = data.get('frase', '')  # Obtém a frase do corpo da requisição JSON
    frase = request.args.get('frase', '')
    return jsonify({'message': frase}), 200

@app.route("/bs64")
def bs64():
    caminho_arquivo_audio = "test.mp3"
    audio_base64 = converter_audio_para_base64(caminho_arquivo_audio)
    return jsonify({'base64': audio_base64}), 200

@app.route("/ttl_get")
def ttl_get():
    #data = request.json
    #frase = data.get('frase', '')  # Obtém a frase do corpo da requisição JSON
    frase = request.args.get('frase', '')
    
    if not frase:
        print("Frase não fornecida")
        return jsonify({'message': 'Frase não fornecida'}), 400
    
    engine = pyttsx3.init() # object creation

    '''Configuração do mecanismo de fala (opcional)'''
    engine.setProperty('rate', 170)     # setting up new voice rate
    engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male

    '''Salva fala em um arquivo'''
    engine.save_to_file(frase, 'test.mp3')
    audio = engine.runAndWait()

    '''Converte o arquivo em base64'''
    audio = 'test.mp3'
    audio_base64 = converter_audio_para_base64(audio)
    
    return jsonify({'base64': "data:audio/x-wav;base64," + audio_base64}), 200

    #'''Salva fala em um arquivo'''
    # On linux make sure that 'espeak' and 'ffmpeg' are installed
    #engine.save_to_file(frase, 'test.mp3')
    #engine.runAndWait()



@app.route('/ttl_post', methods=['POST'])
def ttl_post():
    # Verifica se o cabeçalho 'texto' está presente na requisição
    if 'frase' in request.headers:
        # Recupera o conteúdo do campo 'texto' do cabeçalho
        frase = request.headers['frase']
        engine = pyttsx3.init() # object creation

        '''Configuração do mecanismo de fala (opcional)'''
        engine.setProperty('rate', 170)     # setting up new voice rate
        engine.setProperty('volume',1.0)    # setting up volume level  between 0 and 1
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)  #changing index, changes voices. o for male

        '''Salva fala em um arquivo'''
        engine.save_to_file(frase, 'test.mp3')
        audio = engine.runAndWait()

        '''Converte o arquivo em base64'''
        audio = 'test.mp3'
        audio_base64 = converter_audio_para_base64(audio)
        
        return jsonify({'base64': "data:audio/x-wav;base64," + audio_base64}), 200
    else:
        return 'Campo "frase" não encontrado no cabeçalho da requisição', 400
    


app.run(host="0.0.0.0")
#app.run() # no replit use app.run(host="0.0.0.0") # coloca o site no ar
