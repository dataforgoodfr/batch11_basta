# Documentation du script

Ce document vise à expliquer la structure du fichier de script

## Architecture

Le fichier est un tableau qui contient d'autres tableaux ou dictionnaires.
Le premier indice permet d'accéder au script d'un jour précis.
Ex : `script[0]` permet d'accéder au script du premier jour.

Le second indice permet d'accéder à un envoi précis.
Ex : `script[0][0]` permet d'accéder au premier envoi du premier jour.

Un envoi est un dictionnaire contenant un message ainsi qu'un tableau représentant les sondages associés à ce message.
Ex :
`script[0][0]["message"] -> str` permet d'accéder au message du premier envoi du premier jour.
`script[0][0]["polls"] -> list[dict]` permet d'accéder à la liste des sondages du premier envoi du premier jour.

Un sondage est représenté en dictionnaire contenant les informations suivantes :
- `question -> str` : La question du sondage
- `options -> list[str]` : La liste des options du sondage
- `multivode -> bool` : Si le sondage est un sondage à choix multiple ou non
