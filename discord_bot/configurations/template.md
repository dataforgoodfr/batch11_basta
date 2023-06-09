# Documentation de la configuration du bot

Ce document vise à expliquer la plupart des champs de la configuration du bot.
Je n'ai pas trouvé d'outil permettant de recenser les champs d'un fichier JSON pour faire une documentation rapide donc celle-ci est générée à la main.

## Configuration du bot

- `GENERAL` (dict) : Configuration générale du bot
    - `CHANNELS` (dict) : Configuration sur les channels
      - `DAYS` (list[dict]) : Liste des jours de la semaine. Le nombre de jour varie selon la longueur du tableau
        - `CHANNEL_ID` (int) : ID du channel de discussion pour la journée. -1 si aucun jour n'a été lancé
        - `QUESTION_NO` (int) : Numéro de la dernière question posée. -1 si aucune question n'a encore été posée 
        - `ANO_ANSWERS` (int)  : ID du channel "réponses-anonymes" du jour
    - `CURRENT_DAY` (int) : Jour actuel du forum (-1 si le forum n'est pas lancé, sinon, commence à 0)
    - `OPENING_CHANNEL_HOUR` (int) : Heure d'ouverture des canaux de discussion
    - `CLOSING_CHANNEL_HOUR` (int) : Heure de fermeture des canaux de discussion
    - `TIME_RESTRICTED_CHANNELS` (list[int]) : Liste des channels dont l'accès est restreint selon les heures d'ouverture et de fermeture
    - `MESSAGES_HOURS` (list[int]) : Heure d'envoi des messages automatiques. Attention, si il y a plus d'heures que de messages, le bot renverra des messages d'erreurs (dans les logs) lors des heures sans message. Si il y a plus de messages que d'heures, certains messages ne seront pas envoyés.
- `PRIVATE_CHANNELS` (dict) : Configuration de l'extension privateChannels
  - `ADMIN_ROLE_ID` (int) : ID du rôle administrateur
  - `SHARING_COOLDOWN` (int) : Durée en secondes du délai par utilisateur entre chaque partage de témoignage anonyme
- `MODERATION` (dict) : Configuration de l'extension moderation
  - `MODERATION_ALERTS_CHANNEL` (int) : ID du channel sur lequel envoyer les alertes de modération
  - `REPORT_EMOJI` (str) : ID de l'emoji devant être utilisé pour signaler un message
- `ROLE_MANAGER` (dict) : Configuration de l'extension RoleManager
  - `RULE_MESSAGE_ID` (int) : ID du message auquel il faut réagir pour obtenir le rôle permettant l'accès au serveur
  - `BASE_ROLE_ID` (int) : ID du rôle permettant l'accès au serveur