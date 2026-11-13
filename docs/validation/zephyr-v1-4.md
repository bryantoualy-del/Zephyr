# Zéphyr Companion V1.4

La branche part de `7d7ab89`, le commit de fusion de la PR #20. La PR #4, consacrée à la lisibilité sur iPad, était encore ouverte lors de l’audit.

## Combat sur tablette

Les cartes suivent une grille à douze colonnes. Les Gantelets et leur pouvoir occupent la première rangée (8/4), les châtiments de sort et les Flèches la deuxième (8/4), puis Châtiment divin occupe toute la largeur. La cible Encounter, lorsqu’elle est visible, se place au-dessus de cette grille. Le HUD défile. Le ruban d’économie d’action et les onglets restent visibles dans un même bloc opaque, sous le bandeau RPG Connect.

Après une touche confirmée sur iPad paysage, la barre de Châtiment divin présente le choix et les dés correspondants. En portrait, le dialogue et l’ordre des cartes restent ceux de l’interface existante. Les deux présentations appellent la même transaction d’attaque. Une rotation et un rechargement pendant le choix ont été testés. Le dernier résultat reste lisible dans la barre, y compris si l’attaque rate.

## Gantelets du Titan

L’activation consomme immédiatement l’action bonus et l’utilisation du pouvoir, puis sauvegarde l’état. L’agrandissement se termine après dix minutes ou manuellement et se recharge après un repos court ou long. Peau de pierre occupe l’unique concentration de Zéphyr. La rompre ou lancer un autre sort de concentration laisse l’agrandissement actif. Les sauvegardes antérieures sont reprises en privilégiant le sort déjà suivi lorsqu’une ancienne sauvegarde contient les deux concentrations.

Les FX durent environ 1,2 s à l’activation et 620 ms au retour. Le mode de mouvement réduit affiche un bref fondu. Le serveur de test RPG Connect reçoit les changements d’état, y compris la concentration. Les dégâts physiques non magiques restent à valider à la table. Le protocole de défenses d’Encounter ne fournit pas de modificateur générique avec cette condition pour Zéphyr.

## Recette

- Chromium et WebKit avec Playwright sur 1180 × 820, 1024 × 768, 1366 × 1024, 820 × 1180, 390 × 844 et 430 × 932.
- Navigation tactile, géométrie des cartes, visibilité de Châtiment divin au défilement et avec RPG Connect, reprise d’une touche après rotation et rechargement.
- Critique, Frappe guidée +10, deux attaques, cumul avec le châtiment de sort et le bonus autorisé par le MJ, coûts et entrées de journal uniques.
- Activation et retour des Gantelets, expiration, repos court, remplacement et rupture de concentration, réduction des animations, nettoyage et échanges via WebSocket local.
- 18 tests de résultats de combat en complément.

Les captures de comparaison sont disponibles dans [zephyr-v1-4/](zephyr-v1-4/). Sur appareil réel, vérifier les barres Safari qui se replient au défilement, la rotation pendant une touche confirmée et la fluidité du FX sur l’iPad Air 5. La recette réseau utilise un serveur WebSocket de test. Une partie avec Encounter reste à vérifier.
