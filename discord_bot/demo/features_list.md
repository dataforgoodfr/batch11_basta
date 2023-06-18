# Liste des features à tester dans la demo

## v1.0

### Scénario

- 1. On créé plusieurs comptes utilisatrices sur la landing page
- 2. Cest comptes utilisatrices se connectent sur le serveur de démo
- 3. On créé un environnement de développement à partir du requirements.txt
- 4. Dans l'environnement, on lance le bot à partir de la commande `python bot.py`
- 5. On ouvre le fichier de configuration et on rempli les champs suivants (voir documentation)
  - 1. Les différents jours avec CHANNEL_ID avec la valeur, et QUESTION_NO et ANO_ANSWERS à -1
  - 2. Les différentes heures d'ouverture et fermetures si besoin + d'envoi de message
  - 3. Les channels qui sont censés être ouverts et fermés automatiquement
  - 4. Les informations nécessaire pour les extensions "PRIVATE_CHANNELS", "MODERATION" et "ROLE_MANAGER"
- 6. On rempli le script en suivant les instructions dans la documentation. Ajouter des sondages automatiques dans le script.
- 7. On lance le forum avec l'option associée
- 8. On recommence à créer des comptes utilisatrices et à se connecter sur le serveur de démo
- 9. Les utilisatrices utilisent les réactions pour récupérer le rôle
- 10. On force le bot à envoyer différents messages (via la commande `/next_message`)
- 11. Les utilisatrices discutent
  - 1. Les utilisatrices envoient des messages normalement
  - 2. Les utilisatrices font des signalement de message à la modération  
- 12. Les utilisatrices font des témoignagnes dans des canaux privés (**à étoffer**)
  - 1. Au moins deux utilisatrices font un canal privé
  - 2. Les utilisatrices discutent avec nous (vérification que le staff ait bien accès)
  - 3. Les utilisatrices témoignent
  - 4. Une utilisatrice partage son témoignage au jour où elle a ouvert le canal
  - 5. Une utilisatrice attend le jour suivant pour partager son témoignage et utilise la fonction "rafraîchir"
  - 6. Celle-ci réagit par mégarde à l'un de nos messages (vérification qu'il n'est pas partagé)
- 13. On créé des sondages manuellement
- 14. On force la fin de la journée
- 15. On teste que les utilisatrices ne peuvent plus parler dans les canaux configurés
- 16. On lance une nouvelle journée et on discute de nouveau
- 17. On coupe le bot brutalement et on le relance en utilisant la commande `/start_forum` et `/reload_config`
- 18. On fini le forum avec la commande `/end_forum`