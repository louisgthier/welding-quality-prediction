# Analyse des données triées par Type de Soudure

Nous avons remarqué que ce dataset contient différents types de soudures, et plusieurs catégories propres à ces différentes soudures.

Nous avions deux options :

- Garder uniquement les colonnes communes à tous les types de soudures, ce qui nous laisserait avec bien moins de colonnes que ce que nous avons au début.

- Séparer le dataset afin de regarder si des paramètres intrinsèques à chaque type de soudure permettrait de mieux les évaluer, et ainsi, trouver les paramètres influant dans chaque type de soudure.

La deuxième approche est gardée, car elle nous permet de garder plus d'informations du dataset originel.


# Analyse des différents types de soudure

### FCA

- Colonnes à supprimer :
Les colonnes comme celles de "Copper", "Cobalt" et "Tungsten", qui sont entièrement vides, peuvent être supprimées.

- Gestion des valeurs manquantes :
Des colonnes comme celles de la "Molybdène", "Titanium", et "Elongation" contiennent des valeurs manquantes, nécessitant une stratégie pour les combler ou les supprimer.

- Conversion et normalisation :
Certaines données sont exprimées en différentes unités (% vs parts per million), donc il faudrait potentiellement normaliser les unités.

Comme cette catégorie contient peu de lignes, on décide de remplir les valeurs manquantes par la moyenne car il n'y a pas assez de valeurs pour instaurer des biais.