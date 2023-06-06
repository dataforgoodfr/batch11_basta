# Documentation de la configuration du bot

Ce document vise à expliquer la plupart des champs de la configuration du bot.
Je n'ai pas trouvé d'outil permettant de recenser les champs d'un fichier JSON pour faire une documentation rapide donc celle-ci est générée à la main.

## Configuration du bot

- `GENERAL` (dict) : Configuration générale du bot
    - `CHANNELS` (dict) : Configuration sur les channels
      - `MODERATION_ALERTS_CHANNEL` (int) : ID du channel sur lequel envoyer les alertes de modération
      - `DAYS` (list[dict]) : Liste des jours de la semaine. Le nombre de jour varie selon la longueur du tableau
        - `IS_CURRENT_DAY` (bool) : Si c'est le jour actuel
        - `CHANNEL_ID` (int) : ID du channel de discussion pour la journée. -1 si aucun jour n'a été lancé
        - `QUESTION_NO` (int) : Numéro de la dernière question posée. -1 si aucune question n'a encore été posée 
        - `ANO_ANSWERS` (?)  : ?
    - `OPENING_CHANNEL_HOUR` (int) : Heure d'ouverture des canaux de discussion
    - `CLOSING_CHANNEL_HOUR` (int) : Heure de fermeture des canaux de discussion
    - `TIME_RESTRICTED_CHANNELS` (list[int]) : Liste des channels dont l'accès est restreint selon les heures d'ouverture et de fermeture
    - `MESSAGES_HOURS` (list[int]) : Heure d'envoi des messages automatiques. Attention, si il y a plus d'heures que de messages, le bot renverra des messages d'erreurs (dans les logs) lors des heures sans message. Si il y a plus de messages que d'heures, certains messages ne seront pas envoyés.
- `PRIVATE_CHANNELS` (dict) : Configuration relative à l'extension privateChannels
  - `PRIVATE_CHANNEL_ANNOUNCEMENT_CHANNEL` (int) : ID du channel contenant le bouton de création de canaux privés
  - `SHARING_COOLDOWN` (int) : Durée en secondes du délai par utilisateur entre chaque partage de témoignage anonyme