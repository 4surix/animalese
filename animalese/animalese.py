
import os
import string
import random

from typing import List, Iterable

# pydub envoie des avertissements qui je trouve font un gros pâté tout moche
#  donc j'ai voulue en faire juste un 'print' avec le message

import warnings

with warnings.catch_warnings(record=True) as warns:

    import pydub

    from pydub import AudioSegment
    from pydub.playback import play

    for warn in warns:
        print('Warning pydub: %s' % warn.message)


CHEMIN = os.path.dirname(__file__)


LANGUES = {
    element
    for element in os.listdir(f'{CHEMIN}/audios')
    if '.' not in element
}


# Chargement des audios basique à l'avance
#  cela évite de les charger à chaque fois et donc plus rapide
LETTRES = {
    langue: {
        lettre: AudioSegment.from_file(
            f'{CHEMIN}/audios/{langue}/{lettre}.{ext}',
            ext
        )
        for (lettre, ext) in [
            fichier.split('.')
            for fichier in os.listdir(f'{CHEMIN}/audios/{langue}')
        ]
    }
    for langue in LANGUES
}

AUDIO_ESPACE = AudioSegment.from_wav(f"{CHEMIN}/audios/_espace.wav")
AUDIO_PONCTUACTION = AudioSegment.from_wav(f"{CHEMIN}/audios/_ponctuations.wav")


SYMBOLES_FIN_DE_PHRASE = {'.', '?', '!'}


class PARAM:

    VARIATION = 0.35

    HAUTEUR_TON = 1.7

    # Durant la convertion, sert à afficher les caractères qui n'ont pas d'audio
    AFF_CARAC_AUCUN_AUDIO = True


def ajout_chemin_app(ffmpeg:str = None, avconv:str = None):
    """
    En ajoutant le chemin vers ffmpeg ou avconv 
      cela évite d'avoir à copier l'application dans le module
      si elle existe déjà autre part sur votre ordinateur.
    """

    if ffmpeg:
        os.environ["PATH"] += f';{ffmpeg}'

    if avconv:
        os.environ["PATH"] += f';{avconv}'


def set_frame_rate(audio: AudioSegment, frame_rate: int):

    nouv_audio = audio._spawn(audio.raw_data, overrides={
        "frame_rate": frame_rate
    })

    return nouv_audio.set_frame_rate(audio.frame_rate)


def config_audio_phrase(
        texte: str,
        audios_caracs: List[AudioSegment],
        type_phrase: str,
    ) -> AudioSegment:
    """
    Prend chaque audio des caratères de la phrase
      pour les modifier suivant le type de phrase
      et les assembler pour former l'audio de la phrase.
    """

    audio_phrase = AudioSegment.empty()

    ZONE_DEBUT_PHRASE = len(texte) * 0.2
    ZONE_FIN_PHRASE = len(texte) * 0.8


    if type_phrase == 'interrogative':
        # Bla bla bla ?

        for index, audio_carac in enumerate(audios_caracs):

            if index >= ZONE_FIN_PHRASE:
                # Fin de phrase montante.
                octaves = ( random.random() * PARAM.VARIATION
                            + (index - index*0.8) * 0.11
                          )

            else:
                octaves = random.random() * PARAM.VARIATION

            octaves += PARAM.HAUTEUR_TON

            audio_phrase += set_frame_rate(
                audio_carac, int(audio_carac.frame_rate * octaves)
            )


    elif type_phrase == 'exclamative':
        # Bla bla bla !

        for index, audio_carac in enumerate(audios_caracs):

            if index <= ZONE_DEBUT_PHRASE:
                # Début de phrase montente.
                octaves = ( random.random() * PARAM.VARIATION 
                            + (index - index*0.2) * 0.11 
                          )

            elif index >= ZONE_FIN_PHRASE:
                # Fin de phrase descendante.
                octaves = ( random.random() * PARAM.VARIATION 
                            - (index - index*0.8) * 0.02
                          )

            else:
                octaves = random.random() * PARAM.VARIATION

            octaves += PARAM.HAUTEUR_TON

            audio_phrase += set_frame_rate(
                audio_carac, int(audio_carac.frame_rate * octaves)
            )


    elif type_phrase == 'affirmative':
        # Bla bla bla.

        for index, audio_carac in enumerate(audios_caracs):

            if index >= ZONE_FIN_PHRASE:
                # Fin de phrase descendante.
                octaves = ( random.random() * PARAM.VARIATION 
                            - (index - index*0.8) * 0.02
                          )

            else:
                octaves = random.random() * PARAM.VARIATION

            octaves += PARAM.HAUTEUR_TON

            audio_phrase += set_frame_rate(
                audio_carac, int(audio_carac.frame_rate * octaves)
            )

    else:

        for index, audio_carac in enumerate(audios_caracs):
            octaves = random.random() * PARAM.VARIATION

            octaves += PARAM.HAUTEUR_TON

            audio_phrase += set_frame_rate(
                audio_carac, int(audio_carac.frame_rate * octaves)
            )


    return audio_phrase
    

def remplace_mot_entre_parentheses(texte: str):
    """
    Les mots entre parenthèse représente le petite texte dans Animal Crossing.
    Cela n'est pas prononcées.
    """

    while '(' in texte and ')' in texte:
        debut = texte.index("(")
        fin   = texte.index(")")
        texte = texte[:debut] + "*" * (fin-debut) + texte[fin+1:]

    return texte


def convertie_phrase_vers_audio(
        phrase: str, 
        langue: str
    ) -> AudioSegment:

    if langue not in LANGUES:
        raise ValueError(f"Langue '{langue}' non pris en charge.")

    audios = []

    phrase = phrase.lower().strip()

    phrase = remplace_mot_entre_parentheses(phrase)

    lettres = LETTRES[langue]

    for index, carac in enumerate(phrase):

        audio = lettres.get(carac)

        if audio:
            pass

        elif carac in SYMBOLES_FIN_DE_PHRASE:
            audio = AUDIO_PONCTUACTION + AUDIO_ESPACE

        elif carac in string.punctuation:
            audio = AUDIO_PONCTUACTION

        elif carac == ' ':
            audio = AUDIO_ESPACE

        else:
            if PARAM.AFF_CARAC_AUCUN_AUDIO:
                print(f"'{carac}' -> aucun audio.")
            continue

        audios.append(audio)

    return config_audio_phrase(
        phrase,
        audios, 
        type_phrase = 'affirmative' if phrase[-1] == '.' 
                       else 'interrogative' if phrase[-1] == '?' 
                            else 'exclamative' if phrase[-1] == '!' 
                                 else None
    )


def convertie_texte_vers_audio(texte: str, langue: str) -> AudioSegment:
    """
    Découpe un texte en séparant chaque phrase qu'il contient
      pour en faire un audio.
    """

    phrases = ['']

    for carac in texte:

        phrases[-1] += carac

        if carac in SYMBOLES_FIN_DE_PHRASE:
            phrases.append('')


    audio = None

    for phrase in phrases:

        if not phrase: # phrase == ''
            continue

        audio_phrase = convertie_phrase_vers_audio(phrase, langue=langue)

        if not audio:
            audio = audio_phrase

        else:
            audio += audio_phrase


    return audio + AUDIO_ESPACE


def enregistre_audio(
        audio: AudioSegment, 
        chemin:str = 'animalese.wav',
        format:str ='wav'
    ) -> AudioSegment:
    """
    Le module 'pydub' ne renvoie pas d'erreur claire 
      l'orsque l'on veut exporter l'audio dans un autre format que 'raw' ou 'wav' 
      mais que 'ffmpeg' ou 'avconv' est introuvable.
    Du coup cette fonction le dis explicitement.
    """

    which = pydub.utils.which

    if which("avconv"):
        app = "avconv"
    elif which("ffmpeg"):
        app = "ffmpeg"
    elif format not in {'raw', 'wav'}:
        raise FileNotFoundError("ffmpeg/avconv introuvable.") 

    return audio.export(chemin, format=format)