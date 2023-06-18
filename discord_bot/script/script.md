# Documentation du script

Ce document vise à expliquer la structure du fichier de script

## Architecture

Le fichier est un tableau qui contient d'autres tableaux ou dictionnaires.
Le premier indice permet d'accéder au script d'un jour précis.
Ex : `script[0]` permet d'accéder au script du premier jour.

Le second indice permet d'accéder à un envoi précis.
Ex : `script[0][0]` permet d'accéder au premier envoi du premier jour.

Un envoi est un dictionnaire contenant un message ainsi qu'un tableau représentant les sondages associés à ce message et un champ "ping" pour savoir si on doit pinig les utilisatrices.
Ex :
`script[0][0]["message"] -> str` permet d'accéder au message du premier envoi du premier jour.
`script[0][0]["polls"] -> list[dict]` permet d'accéder à la liste des sondages du premier envoi du premier jour.
`script[0][0]["ping"] -> bool` doit-on ping les utilisatrices pour ce message ?

Un sondage est représenté en dictionnaire contenant les informations suivantes :
- `question -> str` : La question du sondage
- `options -> list[str]` : La liste des options du sondage
- `multivode -> bool` : Si le sondage est un sondage à choix multiple ou non


## Exemple

Ceci est un script qui contient 5 jours avec 3 envois par jour.
Chaque envoi est un message qui est composé comme `day[dayNb]sentence[sentenceNb]]`.
Le premier message du premier jour a un sondage lié à deux choix et sans possibilité de faire du multichoix.7
Le deuxième message du second jour a un sondate liée à 4 choix et avec la possibilité de faire du multichoix.


```json
[
    {
        "message": "day0sentence0",
        "polls": [
            {
                "question": "Est-ce que ?",
                "options": [
                    "oui",
                    "non"
                ],
                "multivote": false
            }
        ],
        "ping": true
    },
    {
        "message": "day0sentence1",
        "polls": [],
        "ping": false

    },
    {
        "message": "day0sentence2",
        "polls": []
    }
],
[
    {
        "message": "day1sentence0",
        "polls": [],
        "ping": false
    },
    {
        "message": "day1sentence1",
        "polls": [
            {
                "question": "Quelles couleurs aimes-tu ?",
                "options": [
                    "vert",
                    "bleu",
                    "rouge",
                    "jaune"
                ],
                "multivote": true
            }
        ]
    },
    {
        "message": "day1sentence2",
        "polls": []
    }
],
[
    {
        "message": "day2sentence0",
        "polls": []
    },
    {
        "message": "day2sentence1",
        "polls": []
    },
    {
        "message": "day2sentence2",
        "polls": []
    }
],
[
    {
        "message": "day3sentence0",
        "polls": []
    },
    {
        "message": "day3sentence1",
        "polls": []
    },
    {
        "message": "day3sentence2",
        "polls": []
    }
],
[
    {
        "message": "day4sentence0",
        "polls": []
    },
    {
        "message": "day4sentence1",
        "polls": []
    },
    {
        "message": "day4sentence2",
        "polls": []
    }
]
```
