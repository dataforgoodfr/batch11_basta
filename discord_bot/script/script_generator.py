import json

"""
Ce notebook permet de générer automatiquement un script.json à partir de la trame.
Attention, les sondages sont à rajouter manuellement.
Le ping est réglé à 1/2, c'est à dire que le bot ping toujours sur le premier message et pas sur le second.
"""


messages = [
    "**Pour lancer cette discussion, j’aimerais que tu postes le gif qui représente le mieux ton expérience d’étudiante ! Tu peux ajouter un # pour expliciter un peu ton choix. Merci !**",
    "Ton expérience d’étudiante est-elle ce à quoi tu t’attendais ?\n\nGlobalement, quelle note sur 10 donnerais-tu à ton expérience d’étudiante ?\n\nTrouves-tu qu’il y a des groupes qui sont moins intégrés / moins écoutés / moins respectés  dans ton école ? Si oui, lesquels ?",
    "**As-tu en tête des anecdotes sur des moments où tu t’es sentie super bien / moins bien intégrée ?\nEst-ce qu’il y a des circonstances dans lesquelles les femmes ont plus de mal à trouver leur place dans l’école ?**",
    "Les femmes font-elles l’objet de stéréotypes ? Si oui, quels sont ceux qui t’énervent le plus ?",
    "**On ne peut pas faire l’impasse sur la journée d’intégration ou le bizutage… \nEst-ce quelque chose qui était source d’appréhension pour toi ? Si oui, pourquoi ?\nQui a participé ? Et quelles ont été les impressions ? **",
    "Enfin, la vie associative au sein de l’école aide-t-elle à s’intégrer ? Tous les témoignages sont les bienvenus !",
    "**41% des femmes entre 15 et 24 ans déclarent avoir été moins bien traitées en raison de leur sexe durant leurs études (rapport annuel 2023 sur l’état des lieux du sexisme en France).\nCe chiffre te surprend-il ?\nPersonnellement, as-tu constaté des différences de traitement entre les femmes et les hommes dans ton école ? Est-ce plus ou moins prononcé selon la spécialisation choisie ?**",
    "Est-ce qu’il y a des obstacles particuliers pour les étudiantes par rapport aux étudiants dans le bon déroulement de leur scolarité ? Dirais-tu que la charge mentale est en général plus élevée pour les étudiantes ?\n\nAs-tu constaté des incivilités au quotidien, comme couper la parole aux étudiantes par exemple ?\nAs-tu fait face à des circonstances dans lesquelles tu t’es sentie rabaissée en tant que femme ? ",
    "**As-tu des exemples, observés ou vécus, de blagues sexistes ou de moqueries ?\nAs-tu déjà été témoin ou victime de comportements machistes ? ou de comportements qui  s’apparentent à du paternalisme ?\nÇa provenait d’autres étudiants ?  Du corps professoral ?  Du personnel administratif ?**",
    "Généralement, la parole des étudiantes est-elle autant prise en compte que celle des étudiants ? Leurs aptitudes et compétences sont-elles autant valorisées ? Lors des travaux en groupe par exemple, ta voix est-elle suffisamment écoutée et respectée ? Trouves-tu l'ambiance propice pour prendre la parole et défendre ton point de vue ?",
    "**Enfin, te sens-tu complètement libre dans tes choix vestimentaires, la façon dont tu te coiffes ou tu te maquilles pour aller à l’école ? Dans quelle mesure le regard masculin a-t-il une influence dans ce domaine ?**",
    "",
    "**Avertissement: nous aborderons des sujets difficiles aujourd’hui, comme les atteintes à l’intégrité physique. Pour celles qui ne voudraient pas du tout participer à la discussion, il est recommandé de se reconnecter demain. Pour les autres, l’objectif est de créer un espace de confiance. L’équipe de modération sera là pour y veiller avec votre aide.\n\nDans le cadre de tes études universitaires, as-tu déjà été la cible de propos, sous-entendus ou attitudes à caractère sexuel qui t’ont mise mal à l’aise ?\nAs-tu été l’objet de propositions sexuelles insistantes ?\nSi oui, penses-tu que ça pourrait se reproduire ? Si non, penses-tu que ça pourrait arriver dans le cadre de ta scolarité ?**",
    "Quel est le sentiment qui prédomine dans ces cas-là ? La colère ? Le fatalisme ? Une forme de honte ?\À ta connaissance, y a-t-il des choses trash comme des photos détournées, des images ou vidéos porno qui circulent sur les réseaux sociaux ou dans certaines boucles de discussion ? L'une de vous a-t-elle déjà eu affaire à un exhibitionniste ou à un voyeur ?\nDirais-tu que tu as fait l’objet de harcèlement ou de chantage dans le cadre de ta vie d’étudiante ? Si oui, de quelle nature ? As-tu vu ou entendu parler de ce genre de problème dans l’école ? Est-ce récurrent ?",
    "**Y-a-t-il déjà eu des formes d’intimidation ou des menaces physiques à ton encontre ? As-tu déjà éprouvé de la peur dans le cadre d’activités scolaires ou extra-scolaires ? Est-ce que parfois tu ne t’es pas sentie en sécurité ? As-tu eu le sentiment d’être dans un environnement hostile ?**",
    "S’il y a des victimes d’agression sexuelle pendant leur scolarité parmi vous et si elles souhaitent témoigner, il est possible de le faire en message privé. Il n’y a malheureusement pas de spécialistes de la prise en charge des victimes sur ce forum, mais nous ferons notre maximum pour orienter celles d’entre vous qui en expriment le besoin.",
    "**En dernier lieu, comment se passent les soirées étudiantes dans l’ensemble ? \nQuels sont tes pires souvenirs de soirée d’école ?**",
    "",
    "**Selon le dernier rapport sur le sexisme en France, seulement 6% de l’ensemble de la population fait totalement confiance aux écoles et universités pour prévenir et lutter contre les actes et violences sexistes… et toi ? \nConnais-tu les dispositifs de lutte contre les violences sexistes et sexuelles (VSS) mis en place par l’établissement ?**",
    "Juges-tu les actions de formation et les campagnes de communication efficaces ? Pourquoi ?\nTrouves-tu que ton école affiche et applique le principe de tolérance zéro en matière de VSS ?",
    "**Te sens-tu suffisamment protégée à titre personnel ? Si une autre étudiante te confiait avoir été victime, saurais-tu  quoi faire et vers qui te tourner ? **",
    "Quels sont à tes yeux les obstacles aux procédures de signalement de violences auprès de l’établissement ? Sont-elles connues et adaptées quand on est témoin d’actes de violence ? Que changerais-tu si tu le pouvais ? \nQui sont les mieux placées pour améliorer la situation ? Les personnes de l’administration ? Des associations de ton école ?  Des personnes externes ? Lesquelles ?",
    "**Penses-tu que ton école est en avance ou en retard dans la lutte contre les VSS ? Pourquoi ?\nSi tu avais un message à faire passer à la direction, quel en serait le contenu ?**",
    "As-tu d’autres idées ou recommandations pour faire bouger les choses ?\nQuelles sont les informations ou ressources dont tu aurais besoin pour mieux conseiller ou accompagner une victime ?",
    "**Il est temps de faire un peu le bilan. Que retiens-tu des derniers jours ? **",
    "As-tu trouvé nos échanges intéressants ? Utiles ?",
    "**Globalement, recommanderais-tu ton école à une amie ?\nEn parlant de l’école à cette amie, sur quels points insisterais-tu ?\nLa mettrais-tu en garde contre certaines choses ?**",
    "Quelle note sur 10 donnerais-tu à l’école sur le plan de l’égalité femmes / hommes ? Merci de préciser un peu les critères sur lesquels se base ta note, qu’elle soit positive ou négative.\n\nC’est aussi l’occasion d’adresser un message aux étudiants-hommes. Qu’as-tu envie de leur dire ?",
    "**En conclusion, as-tu eu l'occasion de t'exprimer comme tu le souhaitais dans le cadre de ce forum ? Est-ce que tu t'es sentie à l'aise et en sécurité lors des échanges ? **",
    "As-tu des remarques ou suggestions pour améliorer le déroulement de ce type de forum ? Certains sujets ont-ils été oubliés ? D’autres auraient-ils mérité d’être plus ou moins développés ?\nUn très grand merci d’avoir accepté de participer.\nJe poste quelques liens et informations à toutes fins utiles.\nPrenez soin de vous et tous mes vœux de succès dans votre scolarité au féminin.",
]


script = []

# Récupère les 6 messages de la journée
jours = [messages[i : i + 6] for i in range(0, len(messages), 6)]


# Crée le script
for jour in jours:
    script.append(
        [
            {
                "message": jour[i],
                "polls": [],
                "ping": True if i % 2 == 0 else False,
            }
            for i in range(len(jour))
        ]
    )


# export to json file
with open("./script/generated_script.json", "w", encoding="utf8") as outfile:
    json.dump(script, outfile, ensure_ascii=False,)
