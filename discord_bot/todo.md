# TODO

Liste des choses à faire pour le projet. Vous pouvez vous ateler à la tâche qui vous convient mais il est possible que certaines demandent que d'autre tâches soient déjà effectuées comme pré-requis.

- [x] Ajouter un script divisé en journées
  - Est-ce que JSON est le meilleur format pour le stocker ?
- [ ] Ajouter des commandes pour gérer les journées telles que :
  - [x] `start day` : pour commencer la journée
  - [x] `stop day` : pour arrêter la journée (sans la lancer automatiquement)
  - [ ] `skip day` : pour passer à la journée suivante (et la lancer automatiquement)
  - [ ] `make conclusion` : pour lancer le processus de récupération des messages
- [x] Ajouter un système de timer pour envoyer des messages à une heure précise (des heures ont été décidées durant les réunions)
  - Au final, on utilise la fonction [task de discord.py](https://discordpy.readthedocs.io/en/stable/ext/tasks/index.html) qui convient parfaitement à notre besoin