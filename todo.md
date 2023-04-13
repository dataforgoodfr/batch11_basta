# TODO


Liste des choses à faire pour le projet. Vous pouvez vous ateler à la tâche qui vous convient mais il est possible que certaines demandent que d'autre tâches soient déjà effectuées comme pré-requis.

- [x] Ajouter un script divisé en journées
  - Est-ce que JSON est le meilleur format pour le stocker ?
- [ ] Ajouter un système de journée :
  - Faire une machine d'état ? Ou alors gérer ca avec les dates dans python ?
- [ ] Ajouter des commandes pour gérer les journées telles que :
  - `start day` : pour commencer la journée
  - `stop day` : pour arrêter la journée (sans la lancer automatiquement)
  - `skip day` : pour passer à la journée suivante (et la lancer automatiquement)
  - `make conclusion` : pour lancer le processus de récupération des messages
- [ ] Ajouter un système de timer pour envoyer des messages à une heure précise (des heures ont été décidées durant les réunions)
  - Un système CRON devrait pouvoir faire l'affaire ! Pourquoi pas utiliser [cette librairie](https://github.com/gawel/aiocron) ?