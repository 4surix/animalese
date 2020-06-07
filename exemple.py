
import animalese


texte = input('>> Texte: ')

audio = animalese.convertie_texte_vers_audio(texte, langue='en')

animalese.enregistre_audio(audio, chemin='animalese.mp3', format='mp3')