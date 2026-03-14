# Les 10 Tips pour Claude Code — Script

**Format :** Tutoriel
**Durée estimée :** ~8 min 20s
**Mots :** ~1 250

---

## HOOK (0:00)

Tu utilises Claude Code mais t'exploites même pas 20% de ce qu'il sait faire. Je le sais parce que moi-même, pendant des semaines, j'utilisais Claude Code comme un simple chatbot dans le terminal. Et puis j'ai découvert ces 10 fonctionnalités qui ont complètement changé ma façon de bosser. Aujourd'hui je te partage tout.

---

## Tip 1 — Context + CLAUDE.md (0:15)

Premier tip, et probablement le plus important : le fichier CLAUDE.md. Quand tu lances Claude Code dans un projet, la première chose qu'il fait c'est chercher ce fichier à la racine. Et dedans, tu mets quoi ? Le contexte. Qui tu es, c'est quoi le projet, comment tu veux qu'il bosse, les règles à respecter. Pense à ça comme un brief que tu donnerais à un freelance. Sans brief, le freelance va improviser. Avec un bon brief, il livre exactement ce que tu veux. Eh ben Claude Code c'est pareil. Et pour le créer, t'as même pas besoin de le faire à la main — tu tapes `/init` et il te le génère automatiquement en analysant ton projet. Fais-le maintenant, tu me remercieras plus tard.

---

## Tip 2 — Les 5 commandes essentielles (1:30)

Deuxième tip : les 5 commandes que tu dois connaître. `/init` on vient d'en parler — ça crée ton CLAUDE.md. `/compact` — quand ta conversation devient longue, Claude Code commence à perdre le fil. Cette commande compresse tout le contexte pour qu'il reste performant. `/clear` — tu veux repartir de zéro, conversation propre. `/cost` — tu veux savoir combien t'as dépensé dans ta session. Et `/help` — si t'oublies tout le reste, retiens celle-là, elle te montre tout ce qui est disponible.

---

## Tip 3 — Le choix du modèle (2:45)

Troisième tip : le choix du modèle. Par défaut, Claude Code utilise Sonnet. C'est un bon modèle, rapide, pas cher, efficace pour 80% des tâches. Mais parfois t'as besoin de plus de puissance — une architecture complexe, un bug vicieux, une réflexion stratégique. Là tu passes sur Opus. C'est plus lent, c'est plus cher, mais la qualité de réflexion est sur un autre niveau. Et pour les trucs simples — renommer des variables, des petites corrections — Haiku fait le job pour quasiment rien. L'idée c'est pas de toujours prendre le plus puissant. C'est de choisir le bon outil pour la bonne tâche. Si tu fais tout en Opus, tu vas cramer ton budget pour rien. Si tu fais tout en Haiku, tu vas t'arracher les cheveux sur les tâches complexes.

---

## Tip 4 — Les flags et modes (4:00)

Quatrième tip : les flags et les modes. Quand tu lances Claude Code, tu peux ajouter des options qui changent complètement son comportement. Le premier que tu dois connaître c'est `--dangerously-skip-permissions`. Le nom fait peur, mais concrètement ça veut juste dire que Claude Code va pas te demander la permission à chaque fois qu'il veut modifier un fichier ou lancer une commande. Sans ça, tu passes ton temps à valider des popups. Ensuite, le flag `-r` — ça te permet de reprendre ta dernière conversation là où tu l'as laissée. Super utile quand tu fermes ton terminal par accident ou que tu reprends le lendemain. Et dans la conversation, t'as `/plan` — tu demandes à Claude Code de réfléchir et de te proposer un plan avant de coder. Et `think` ou `ultrathink` — tu forces Claude à prendre plus de temps pour réfléchir. Sur les problèmes complexes, ça change tout.

---

## Tip 5 — Les hooks (5:10)

Cinquième tip : les hooks. C'est le tip que personne connaît et qui est pourtant incroyable. Les hooks c'est des scripts qui se lancent automatiquement quand Claude Code fait certaines actions. Par exemple, tu peux configurer un hook qui lance un linter à chaque fois qu'il modifie un fichier. Ou un hook qui formate automatiquement ton code après chaque modification. Le résultat c'est que Claude Code produit du code propre à chaque fois, sans que t'aies à le demander. C'est de l'automatisation invisible — tu le configures une fois et t'y penses plus.

---

## Tip 6 — Les MCP servers (6:00)

Sixième tip : les MCP servers. MCP ça veut dire Model Context Protocol. En gros, c'est un moyen de connecter Claude Code à des outils externes. Notion, Figma, une base de données, une API, un navigateur web. Sans MCP, Claude Code c'est un assistant qui code. Avec MCP, c'est un assistant qui code, qui va chercher tes specs dans Notion, qui regarde tes maquettes Figma, et qui met à jour ta base de données. Il passe d'un outil à un écosystème complet. Et la bonne nouvelle c'est que la communauté a déjà créé des centaines de serveurs MCP prêts à l'emploi. T'as juste à les connecter.

---

## Tip 7 — Les raccourcis clavier (6:50)

Septième tip : les raccourcis clavier. C'est pas le tip le plus sexy, mais c'est celui qui te fait gagner du temps au quotidien. Escape pour annuler une génération en cours — indispensable quand Claude Code part dans la mauvaise direction. Tab pour accepter une autocomplétion. Et un que j'adore : quand Claude Code te propose une action et que tu veux juste dire oui, tu tapes pas "oui" — tu appuies juste sur Entrée. C'est des petits trucs, mais sur une journée entière, ça fait une vraie différence.

---

## Tip 8 — Les custom slash commands (7:20)

Huitième tip : les custom slash commands. Tu sais les commandes comme `/init` et `/compact` ? Tu peux créer les tiennes. Tu crées un fichier markdown dans le dossier `.claude/commands/` de ton projet, tu écris ton prompt dedans, et c'est fait. Par exemple, moi j'ai un `/project:commit` — je tape la commande, Claude Code analyse tous mes changements et crée un commit avec un message propre. J'ai un `/project:review` — il relit mon code et me dit ce qui va pas avant que je push. C'est comme créer tes propres macros, sauf que ces macros sont alimentées par l'IA. 30 secondes pour en créer une, et tu la réutilises pour toujours.

---

## Tip 9 — GitHub, ton filet de sécurité (8:00)

Neuvième tip : GitHub. Je sais, si t'es pas dev, GitHub ça fait peur. Mais écoute-moi. Quand tu bosses avec Claude Code, ton projet est en local sur ta machine. Si ton disque dur lâche, si tu fais une mauvaise manip, si Claude Code casse quelque chose — t'as tout perdu. GitHub c'est ta sauvegarde. Ton filet de sécurité. Mais c'est pas que ça. C'est aussi un historique complet — tu peux revenir à n'importe quelle version de ton projet. C'est aussi un outil de collaboration — si demain tu recrutes un dev freelance, il peut bosser sur ton projet sans que tu lui envoies des fichiers par mail. Et Claude Code s'intègre nativement avec GitHub. Il peut créer des pull requests, lire des issues, tout ça depuis le terminal. Mettre ton projet sur GitHub ça prend littéralement 2 minutes. Fais-le.

---

## Tip 10 — Le workflow idéal (8:40)

Et dixième tip, le tip meta : le workflow idéal. Maintenant que tu connais tous ces outils, voilà comment les assembler. Tu commences par créer ton CLAUDE.md avec `/init` — c'est la fondation. Tu mets ton projet sur GitHub — c'est ton filet de sécurité. Tu configures tes hooks pour que le code soit toujours propre. Tu crées tes custom commands pour tes tâches répétitives. Tu connectes tes MCP servers pour les outils que tu utilises au quotidien. Et quand tu bosses, tu choisis le bon modèle selon la tâche, tu utilises `/plan` avant les gros chantiers, et tu `/compact` régulièrement pour garder Claude Code performant. C'est cette combinaison qui fait la différence. Chaque tip seul c'est bien. Les 10 ensemble, c'est une machine.

---

## CTA

Si tu veux que je fasse une vidéo deep dive sur un de ces tips — les hooks, les MCP servers, les custom commands — dis-le moi en commentaire et je fais la vidéo. Et si cette vidéo t'a aidé, un like ça prend une seconde et ça m'aide énormément. À la prochaine.
