# J'abandonne mon challenge — deck HyperFrames (pilote)

- `python3 build-deck.py` : régénère `index.html` et `compositions/sXX.html` à partir des sources (un seul fichier à éditer).
- `npm run check` : lint + rendu + mise en page + contraste.
- `npm run tournage` : lance le serveur et ouvre **le lecteur de tournage** `tournage.html` (clic = l'animation de la slide se joue puis s'arrête ; → / Espace suite, ← précédente, R rejouer, F plein écran, H cacher le bandeau).
- `npm run present` : mode présentateur natif HyperFrames (notes, aperçu) — attention, en v0.8.164 il *saute* aux images fixes sans jouer les animations.
- `npm run render` : MP4 du deck complet (8 s par slide), dernier rendu dans `renders/`.

Après toute modif de `index.html`, redémarrer le serveur `present` (il met l'îlot JSON en cache).
Blocs du registre utilisés : `char-slam-explode` (slide 2), `mk-line-graph` adapté (slide 13).
