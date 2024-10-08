# Welding Quality Prediction

Le but de ce projet est de prédire la qualité de soudures sur des aciers. Il s’agit d’une problématique d’intérêt pour de nombreux industriels dont le secteur pèse plusieurs milliards d’euros (exemple : soudure de pipe d’éoliennes). De nos jours, la connaissance liée à la qualité des soudures se transmet principalement d’expert à expert soudeur dont les industriels sont dépendants. Il y a un gros enjeu à acquérir de la connaissance via les données pour à la fois extraire et homogénéiser la connaissance experte mais également explorer de nouvelles connaissances via des patterns que l’on pourrait découvrir par l’exploration de la donnée.

## Obtenir les données

Les données publiques pour réaliser ce projet sont accessibles via le lien suivant : https://www.phase-trans.msm.cam.ac.uk/map/data/materials/welddb-b.html. 

## Objectifs du projet

Les objectifs du projet sont les suivants :

- Faire une analyse descriptive de la base de données pour bien la maîtriser et identifier les tâches de preprocessing pertinentes à réaliser. Toute action de preprocessing devra être explicitée, décrite et justifiée. Réfléchir aux unités de mesures des variables, à la nécessité de normaliser ou non les données, appliquer une ACP pour développer de l’intuition sur la problématique, etc.

- Identifier quelles sont les variables représentatives de la qualité de soudure et bien les comprendre. Réfléchir à la façon de prédire la qualité de soudure à partir de ces variables identifiées. Cela implique de réfléchir à une stratégie et il est attendu de bien l’expliciter et la justifier.

- Appliquer différentes approches de ML vues en cours et en TD sur ce dataset pour prédire la qualité de soudure. Pensez à réaliser un protocole de validation croisée rigoureux. Enfin, le dataset n’étant pas complétement labélisé, nous vous invitons à effectuer un travail bibliographique sur des méthodes de ML avancées de type semi-supervisées. Vous êtes invités à en appliquer au minimum une en justifiant votre choix et la pertinence de celle-ci.

- Faire une analyse comparative des performances des différents modèles et méthodes appliqués. Il est donc nécessaire de réfléchir aux choix des métriques pertinentes.

- Conclure sur l’approche la plus appropriée pour prédire la qualité de soudure.

- Après cette étude : quelles sont vos recommandations pour obtenir une bonne qualité de soudure ?

- Écrire un rapport d’environ 5 pages synthétisant le travail effectué et les résultats obtenus. Pensez à indiquer vos noms, le numéro de votre équipe, la date, vos mails et le titre sur la première page. Pensez aussi à mettre quelques figures illustratives. Il sera attendu un plan, une section rappelant la problématique du projet et votre traduction de celle-ci en problème/tâche de ML. Une section décrivant la base de données est aussi attendue (résultat d’ACP etc.), votre compréhension des variables cibles pour prédire la qualité de soudure et comment est-ce que vous proposez de vous y prendre. Une section sur les méthodes ML que vous choisissez d’appliquer avec vos justifications (pensez à les présenter synthétiquement, surtout si elles n’ont pas été vues en cours). Une section sur les résultats numériques sera à réaliser avec une étude comparative des performances. Les formules et/ou description des métriques utilisées devront être présentées. Enfin, pensez à ajouter une dernière section de discussion et conclusion avec un diagramme de GANNT contenant le partage en tâches, le temps que chaque tâche a pris et quel membre de l’équipe s’en est chargée. Bien entendu, une section sur les références bibliographiques clôturera le rapport. Pensez à bien citer vos références dans le corps de rapport.

- Remarques générales : un rapport doit être paginé, les figures et tableaux doivent avoir un titre et être cités dans le corps du rapport quand on y fait référence.

## Identification des variables pertinentes

L'objectif est de prédire la qualité des soudures en fonction de divers paramètres mécaniques et physiques.

Le descriptif des soudures est résumé [ici](https://github.com/louisgthier/welding-quality-prediction/blob/main/columns_description.md)

À première vue, les colonnes pertinentes pour cette évaluation incluent : l'allongement _(Elongation / %)_, réduction de la zone _(Reduction of Area / %)_, résistance limite d'élasticité _(Yield strength / MPa)_, résistance à la traction _(Ultimate tensile strength / MPa)_, dureté _(Hardness / kg mm^{-2})_, ténacité Charpy _(Charpy impact toughness / J)_, et température de transition de fracture (_50% FATT_).

## PreProcessing

## Valeurs manquantes

### _missing_values.py_ :

Nous imprimons premièrement les pourcentages de valeurs manquantes de chaque colonne.

Voici ce que cela donne :

| Nom de la colonne                                     | Pourcentage de valeurs manquantes |
| ----------------------------------------------------- | --------------------------------- |
| Carbon concentration / weight %                       | 0.00                              |
| Silicon concentration / weight %                      | 0.00                              |
| Manganese concentration / weight %                    | 0.00                              |
| Sulphur concentration / weight %                      | 0.24                              |
| Phosphorus concentration / weight %                   | 0.61                              |
| Nickel concentration / weight %                       | 57.81                             |
| Chromium concentration / weight %                     | 52.54                             |
| Molybdenum concentration / weight %                   | 52.00                             |
| Vanadium concentration / weight %                     | 43.83                             |
| Copper concentration / weight %                       | 65.01                             |
| Cobalt concentration / weight %                       | 92.19                             |
| Tungsten concentration / weight %                     | 95.46                             |
| Oxygen concentration / parts per million by weight    | 23.97                             |
| Titanium concentration / parts per million by weight  | 43.40                             |
| Nitrogen concentration / parts per million by weight  | 24.82                             |
| Aluminium concentration / parts per million by weight | 45.22                             |
| Boron concentration / parts per million by weight     | 69.49                             |
| Niobium concentration / parts per million by weight   | 54.48                             |
| Tin concentration / parts per million by weight       | 82.08                             |
| Arsenic concentration / parts per million by weight   | 85.84                             |
| Antimony concentration / parts per million by weight  | 84.26                             |
| Current / A                                           | 15.01                             |
| Voltage / V                                           | 15.01                             |
| AC or DC                                              | 13.01                             |
| Electrode positive or negative                        | 9.44                              |
| Heat input / kJ mm^{-1}                               | 0.00                              |
| Interpass temperature / °C                            | 0.00                              |
| Type of weld                                          | 0.00                              |
| Post weld heat treatment temperature / °C             | 0.79                              |
| Post weld heat treatment time / hours                 | 0.79                              |
| Yield strength / MPa                                  | 52.78                             |
| Ultimate tensile strength / MPa                       | 55.33                             |
| Elongation / %                                        | 57.63                             |
| Reduction of Area / %                                 | 57.32                             |
| Charpy temperature / °C                               | 46.79                             |
| Charpy impact toughness / J                           | 46.79                             |
| Hardness / kg mm^{-2}                                 | 91.65                             |
| 50% FATT                                              | 98.12                             |
| Primary ferrite in microstructure / %                 | 94.07                             |
| Ferrite with second phase / %                         | 94.55                             |
| Acicular ferrite / %                                  | 94.55                             |
| Martensite / %                                        | 94.61                             |
| Ferrite with carbide aggregate / %                    | 94.61                             |
| Weld ID                                               | 0.00                              |

### Suppression de colonnes inexploitables

Nous constatons un très grand nombre de valeurs manquantes dans les colonnes _Primary ferrite in microstructure_ (94,07 %), _Ferrite with second phase_ (94,55 %), _Acicular ferrite_ (94,55 %), _Martensite_ (94,61 %), et _Ferrite with carbide aggregate_ (94,61 %). Les valeurs manquantes de ces cinq colonnes sont des _MNAR (Missing Not At Random)_, car elles apparaissent systématiquement de manière conjointe. Nous supprimons ces colonnes inexploitables contenant trop de valeurs manquantes. De même, nous supprimons les colonnes *50% FATT* et *Hardness / kg mm^{-2}* contenant respectivement 98.12 % et 91.65 % de valeurs manquantes. 

### Suppression de lignes inexploitables

Après suppression des colonnes de trop grand nombre de valeurs manquantes, les variables qui nous intéressent pour la prédiction de la qualité de la soudure sont : *Yield strength / MPa*, *Ultimate tensile strength / MPa*, *Elongation / %'*, *Reduction of Area / %* et *Charpy impact toughness / J*.

Toutefois, nous remarquons que les mesures concernant le test Charpy sont réalisées indépendemment des 4 autres mesures. En effet, une valeur manquante dans la colonne *Charpy impact toughness / J* est très souvent synonyme de la présence de valeurs dans les 4 autres colonnes, et inversement. Pour traiter ces valeurs manquantes de type MNAR, il serait mal venu d'imputer des valeurs (cela nuirait à la précision du modèle), et de supprimer les lignes qui les contiennent (cela supprimerait presque toutes les lignes du dataset, comme les valeurs des colonnes *Charpy impact toughness / J* et des 4 autres colonnes ne sont presque jamais présentes coinjointement). C'est pourquoi nous décidons plutôt de séparer le dataset en 2 : un dataset contenant la colonne *Charpy impact toughness / J* et un autre contenant les 4 autres colonnes. 

### Colonnes quantitatives mal formattées :

* Colonne de la concentration en nitrogène

Nous constatons que la colonne sur la concentration en nitrogène contient des valeurs d'un format inexploitable, comme '67tot33res'. "tot" et "res" font penser à "total" et "résidus", des termes chimiques correspondants à un résultat de réaction chimique. "nd" signifierait un manque de données, "non-détecté" (en anglais _non detected_). Les valeurs avant 'tot' sont gardées dans la colonne et une nouvelle colonne est créée pour les résidus. 

Cependant, cette colonne ne contient pas assez de valeurs par rapport au dataset et sera sûrement inutile. Nous la retirons de notre analyse principale. Nous la gardons de côté afin de peut-être observer une coincidence avec les résultats finaux (peut-être qu'une réaction avec/sans résidus aura plus de chances de produire un résultat de qualité). Nous gardons cette variable afin d'en faire une colonne booléenne : La concentration a-t-elle des résidus ? Oui/Non. (?)

* Autres colonnes sur la concentration

Nous retrouvons souvent le signe "<" devant de nombreuses variables de concentrations, par exemple dans les colonnes *Tin concentration / parts per million by weight* et *Arsenic concentration / parts per million by weight*.

Nous avons établi trois approches possibles concernant ces valeurs :

1 - Garder le nombre derrière le signe
Cela signifie que notre analyse devra être basée sur le fait que nos résultats peuvent provenir de la borne supérieure.

2 - Remplacer le nombre derrière le signe efficacement
Nous pouvons remplacer le nombre derrière le signe par la moyenne des nombres inférieurs à ce nombre, ainsi, nous restons cohérents. Problème : on renforce les liens de corrélations existants, alors pour être vraiment cohérents, on ajoute du bruit sur ces variables.

3 - Diviser le nombre derrière le signe par deux
A défaut d'avoir suffisamment de valeurs pour remplacer de façon cohérente le nombre derrière le signe, on peut partir sur la moitié du nombre afin de remplacer le signe. Cela est bien plus simple à mettre en place.

Nous avons finalement opté pour la 3e approche. 

* Colonne *Hardness / kg mm^{-2}*

Des valeurs inexploitables sont également présentes dans la colonne *Hardness / kg mm^{-2}*. Elles sont de la forme '158(Hv30)'. 

Après plusieurs recherches, nous avons découvert que Hv signifie la force effectuée sur l'objet pour obtenir un tel résultat. Comme cela est une statistique, nous la mettons aussi de côté et trions les données.

* Colonne *Temperature Interpass*

Nous remarquons que certaines valeurs sont présentes sous la forme d'un intervalle (par exemple, '150-200'). Nous remplaçons ces valeurs par la moyenne des deux bornes de l'intervalle. 

# Analyse des variables

Pour analyser les variables, nous avons simplement imprimé les valeurs unique de chaque colonne et déduit le type de chaque colonne [ici](https://github.com/louisgthier/welding-quality-prediction/blob/main/unique_values.md)

## Colonnes qualitatives mal formattées


### Type of weld

Il y a 10 types de soudure différents, identifiés par des chaines de caractère dans la colonne. Pour que cette information soit exploitable, nous effectuons un one-hot encoding résultant en la création de 10 colonnes binaires. Pour éviter la multicollinéarité (corrélation entre 2 colonnes ou plus) dû au one-hot encoding, nous supprimons une des colonnes choisie aléatoirement : il s'agit en particulier de la colonne ShMA.

### WeldID

Le nombre d'IDs différents étant très important, il serait mal venu de réaliser un one-hot encoding sur la colonne WeldID créant un nombre trop important de colonnes par rapport au nombre d'instances du dataset. Toutefois, nous remarquons que les IDs peuvent se regrouper, en fonction du format de l'ID (s'il contiennent un même mot, par exemple Evans), et en fonction des valeurs manquantes (les IDs d'un même groupe ont très souvent des valeurs manquantes dans les mêmes colonnes). Ainsi, nous regroupons les IDs en groupes grâce à des commandes regex. Ensuite, nous effectuons un one-hot encoding sur la colonne WeldID, tout en supprimant une des colonnes (Wolst) pour éviter l'effet indésirable de multicollinéarité dû à cette opération.

### AC or DC

Outre les 13 % de valeurs manquantes, cette colonne contient uniquement deux catégories : AC et DC. Pour rendre ces données plus exploitables, nous avons décidé de convertir les valeurs en format binaire : 0 pour le mode AC et 1 pour le mode DC.

Les valeurs manquantes semblent être des MAR (Missing At Random), liées au type de WeldID. En effet, les valeurs manquantes apparaissent pour des types de WeldID tels que p..-RR82011, RC81033, EvansLetter, et Birmingham. Nous pouvons imputer ces valeurs de manière fiable : lorsque la polarité de l'électrode est explicitement indiquée par un signe + ou -, il s'agit très probablement du mode DC, puisque le mode AC (courant alternatif) n'a pas de polarité fixe. Ainsi, lorsqu'une polarité d'électrode est spécifiée, nous imputons le mode DC.

Cependant, il arrive parfois que des valeurs soient également manquantes dans la colonne indiquant la polarité de l'électrode. Dans ces cas, nous examinons les autres colonnes. Nous constatons que les dernières valeurs manquantes dans la colonne AC/DC apparaissent principalement lorsque le type de soudure est MMA (Manual Metal Arc), un procédé qui est souvent plus stable et efficace en mode DC, surtout dans des conditions exigeant une grande stabilité de l'arc. Bien que le mode AC soit parfois utilisé en MMA, DC est généralement préféré pour éviter les problèmes de stabilité et améliorer la performance du soudage. Il parait donc plus probable que les valeurs manquantes soient des valeurs DC. De plus, 97 % des valeurs de la colonne sont déjà en mode DC. L'imputation des valeurs manquantes en 1 (ie mode DC) est donc en accord avec la distribution générale des données.

### Electrode positive or negative

Nous avons identifié quatre types de valeurs possibles dans cette colonne : +, -, ou 0, et les valeurs manquantes. Les 0 sont liés à l'utilisation du mode AC.

Nous devons transformer les valeurs présentes afin qu'elles soient interprétables par les algorithmes de ML. Plutôt que d'effectuer un one-hot encoding en créant trois colonnes binaires distinctes, ce qui pourrait entraîner de la multicollinéarité et poser des problèmes pour certains algorithmes de ML, nous choisissons de diviser la colonne en seulement deux colonnes binaires : la première indiquera si l'électrode est positive (+), et la seconde si elle est négative (-). Si la valeur est 0 (par exemple dû à un mode AC) ou s'il y a une valeur manquante, les deux colonnes afficheront 0.

## Imputation des valeurs 

Après avoir nettoyé et reformatté des colonnes, il faut imputer les valeurs manquantes qui n'ont pas été supprimées. 

* Colonnes de concentration

 Nous remplaçons les valeurs manquantes de ces colonnes par 0, car nous supposons que s'il y a des valeurs manquantes, c'est que l'élément chimique concerné n'est pas présent dans le composé.

* Autres colonnes (*Voltage / V*, *Current / A*, *Post weld heat treatment temperature*, *Post weld heat treatment time / hours*, *Interpass temperature*)

Les valeurs manquantes de chaque colonnes sont remplacées par la médiane de la colonne concernée. (?)

