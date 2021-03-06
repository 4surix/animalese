
**Convertisseur Animalese (Langage d'animal crossing)**

# Pourquoi ce module ?

Je cherchais comment fonctionnait la langue d'Animal crossing.  
J'ai découvert que cela s'appelle `Animalese` et d'autre informations sur son fonctionnement avec [cette vidéo](https://www.youtube.com/watch?v=Ye6WDE_aO0M).  
  
Puis j'ai voulu créer mes propres textes, je suis tombée sur le [projet Github d'equalo-official](https://github.com/equalo-official/animalese-generator) et la [vidéo d'henryishuman](https://www.youtube.com/watch?v=IKMjg2fEGgE) et je me suis amusée à essayer leur module.  

J'ai voulue ensuite les améliorer et faire mon propre module.  

# Dépendences

Ces éléments sont nécessaires au bon fonctionnement :

- [`pyhub`](https://pypi.org/project/pyhub/)
- [`ffmpeg`](https://ffmpeg.org/download.html)

# Comment rajouter des fichiers audios ?

**De base le module n'a pas de fichier audio**.  
  
Vous pouvez en trouver avec : le [site sounds-resource](https://www.sounds-resource.com/wii/ssbb/sound/27087/), la [vidéo d'henryishuman](https://www.youtube.com/watch?v=IKMjg2fEGgE) dans laquel ses audios en description m'ont servi pour tester le module, ou encore le [projet Github d'equalo-official](https://github.com/equalo-official/animalese-generator).  

Sinon vous pouvez faire aussi vos propres fichiers audios avec un logiciel d'enregistrement.  
  
Ensuite il suffira de créer un dossier portant le nom de la langue dans laquel les enregistrements ont été fait.  
Dedans vous mettrez les enregistrements audios. Chaque fichier devra avoir comme nom le caractère correspondent à l'audio.  
  
Cela doit ressembler à ça :
```
animalese
|- audios
|  |- en
|  |  |- a.wav
|  |  |- b.wav
|  |  |- c.wav
|  |  |- ...
|  |- fr
|  |  |- a.wav
|  |  |- b.wav
|  |  |- c.wav
|  |  |- ...
```

# Documentation

## convertie_texte_vers_audio(texte, langue) -> Audio

### texte

Le texte à convertir en audio.

### langue

La langue de l'audio à utiliser et donc le nom du dossier avec les fichiers audios de cette langue.  
L'Animalese n'est pas construit de la même manière suivant la langue.
Vous pouvez utiliser du texte de n'importe quelle langue avec un audio de n'importe quelle langue, mais cela sera moins réaliste.

```python
import animalese

texte = """
Bonjour, maire ! 
Aujourd'hui, c'est le solstice d'été, alors ne vous attendez pas du tout à voir la lune ce soir ! 
J'ai préparé un petit quelque chose pour le solstice d'été. Vous êtes curieux de voir ce que j'ai imaginé ? 
Ils sont en échelle nuances ! 
Voyant comment cela restera si chaud et lumineux toute la journée, je me suis dit que celles-ci seraient très utiles ! 
De plus, elles sont à la pointe de la mode ! 
"""

audio = animalese.convertie_texte_vers_audio(texte, langue='en')
```

## convertie_phrase_vers_audio(phrase, langue) -> Audio

### phrase

La phrase à convertir en audio.

### langue

La langue de l'audio à utiliser, et donc le nom du dossier avec les fichiers audios de cette langue.  
L'Animalese n'est pas construit de la même manière suivant la langue.
Vous pouvez utiliser du texte de n'importe quelle langue avec un audio de n'importe quelle langue, mais cela sera moins réaliste. 

```python
import animalese

phrase = "Aujourd'hui est le plus long après-midi de l'année, cela en fait une excellente journée pour jouer !"

audio = animalese.convertie_phrase_vers_audio(phrase, langue='en')
```

## enregistre_audio(audio, chemin, format) -> Raw

### audio

Audio à enregistrer.

### chemin

Endroit du fichier à sauvegarder contenant l'audio.

### format

Format du fichier.

```python
import animalese

texte = "Je pense que cette endroit devrait faire l'affaire, mais j'hésite... Tu en pense quoi ?"

audio = animalese.convertie_texte_vers_audio(texte, langue='en')

animalese.enregistre_audio(audio, chemin='animalese.mp3', format='mp3')
```

## ajout_chemin_app(ffmpeg, avconv)

### ffmpeg

Chemin menant vert l'application `ffmpeg`.

### avconv

Chemin menant vert l'application `avconv`.

```python
import animalese

animalese.ajout_chemin_app(ffmpeg='utile/app')
```