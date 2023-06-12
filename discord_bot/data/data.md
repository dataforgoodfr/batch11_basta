# Documentation du fichier data

Le fichier data est unique a chaque serveur et est identifié par son nom qui est l'ID du serveur correspondant.
Ce fichier sert à sauvegarder des données qui ne sont pas de la configuration mais qui restent propres au serveur.
Ce fichier sert de backup mais il est normalement stocké dans la mémoire du bot et sert à récupérer ces données lors d'un crash.

## Structure du fichier

Le fichier est un fichier JSON qui contient un dictionnaire.
Les clefs ne sont pas forcément définies selon si le bot a eu l'utilité de les créer ou non.

Les clefs possibles sont :
- `not_log_channels` (list[int]) : une liste des ids des TextChannels à ne pas récupérer lors de la récupération des messages pour la synthèse. Attention, les logs récupèrent TOUS les evenements et donc tous les messages sans restrictions (pour des raisons légales).
-  `polls` (list[dict]) : une liste de dictionnaires qui contient tous les sondages qui ont été générés. Ce dictionnaire contient 4 clefs :
   - `title` : le titre du sondage 
   - `description` : la description du sondage
   - `tally` : un dictionnaire qui contient les clefs qui sont les réactions et les valeurs qui sont les nombres de réactions
   - `opt_dict` : un dictionnaire qui contient les clefs qui sont les réactions et les valeurs qui sont les options du sondage