// Convergence — LES SUJETS DE L'ÉPISODE
// À remplir avant chaque live. Chaque sujet = une carte, dans l'ordre.
// Dans OBS, la scène « 4 · Sujet 1 » affiche le 1er sujet, « 4 · Sujet 2 » le 2e, etc.
//
//   type  : le sur-titre en vert. "TENDANCE" est numéroté tout seul (TENDANCE N°1, N°2…).
//           Tout autre texte s'affiche tel quel : "LE TRADE DE LA SEMAINE", "LA QUESTION DU CHAT"…
//   titre : la phrase en gros.
//   mot   : le mot du titre à mettre en or (facultatif).
//   tags  : les étiquettes en dessous (facultatif).
//   style : "trade" pour la carte spéciale du trade de la semaine (facultatif).
//   trade : pour style "trade" : actif, sens (ACHAT / VENTE), entrée, objectif, invalidation.

window.SUJETS = [
  {
    type: "TENDANCE",
    titre: "L'or casse son record.",
    mot: "or",
    tags: ["OR", "BANQUES CENTRALES"],
  },
  {
    type: "TENDANCE",
    titre: "Le Bitcoin repasse les 85 000 $.",
    mot: "Bitcoin",
    tags: ["BTC", "ETF"],
  },
  {
    type: "LE TRADE DE LA SEMAINE",
    style: "trade",
    titre: "Solana vers 150 $ ?",
    mot: "Solana",
    trade: { actif: "SOL", sens: "ACHAT", entree: "119 $", objectif: "150 $", invalidation: "105 $" },
  },
  {
    type: "LA QUESTION DU CHAT",
    titre: "Faut-il vendre son or maintenant ?",
    mot: "or",
  },
];
