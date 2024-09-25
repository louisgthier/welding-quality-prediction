# PREPROCESSING

Avant-propos : Etant donné la nature du dataset, qui est composé de seulement 1600 valeurs environ, il faut être délicat.
Notre stratégie sera de d'abord privilégier le remplacement des données, quitte à parfois aller dans le sens
de renforcer les corrélations existantes, cependant nous ne pouvons supprimer des lignes données car la moitié de leurs valeurs de colonnes sont manquantes.

Pour éviter de trop renforcer les hyper-corrélations, nous ajouterons du bruit sur les valeurs que nous remplierons.

## Valeurs manquantes

### *missing_values.py* :

Tout d'abord, nous cherchons à comprendre les valeurs des colonnes.
Pour cela, nous imprimons à plusieurs reprises les pourcentages de valeurs manquantes de chaque colonne.

Voici ce que cela donne :


| Nom de la colonne                                              | Pourcentage de valeurs manquantes |
|----------------------------------------------------------------|-----------------------------------|
| Carbon concentration / weight %                                | 0.00                              |
| Silicon concentration / weight %                               | 0.00                              |
| Manganese concentration / weight %                             | 0.00                              |
| Sulphur concentration / weight %                               | 0.24                              |
| Phosphorus concentration / weight %                            | 0.61                              |
| Nickel concentration / weight %                                | 57.81                             |
| Chromium concentration / weight %                              | 52.54                             |
| Molybdenum concentration / weight %                            | 52.00                             |
| Vanadium concentration / weight %                              | 43.83                             |
| Copper concentration / weight %                                | 65.01                             |
| Cobalt concentration / weight %                                | 92.19                             |
| Tungsten concentration / weight %                              | 95.46                             |
| Oxygen concentration / parts per million by weight             | 23.97                             |
| Titanium concentration / parts per million by weight           | 43.40                             |
| Nitrogen concentration / parts per million by weight           | 24.82                             |
| Aluminium concentration / parts per million by weight          | 45.22                             |
| Boron concentration / parts per million by weight              | 69.49                             |
| Niobium concentration / parts per million by weight            | 54.48                             |
| Tin concentration / parts per million by weight                | 82.08                             |
| Arsenic concentration / parts per million by weight            | 85.84                             |
| Antimony concentration / parts per million by weight           | 84.26                             |
| Current / A                                                    | 15.01                             |
| Voltage / V                                                    | 15.01                             |
| AC or DC                                                       | 13.01                             |
| Electrode positive or negative                                 | 9.44                              |
| Heat input / kJ mm^{-1}                                        | 0.00                              |
| Interpass temperature / °C                                     | 0.00                              |
| Type of weld                                                   | 0.00                              |
| Post weld heat treatment temperature / °C                      | 0.79                              |
| Post weld heat treatment time / hours                          | 0.79                              |
| Yield strength / MPa                                           | 52.78                             |
| Ultimate tensile strength / MPa                                | 55.33                             |
| Elongation / %                                                 | 57.63                             |
| Reduction of Area / %                                          | 57.32                             |
| Charpy temperature / °C                                        | 46.79                             |
| Charpy impact toughness / J                                    | 46.79                             |
| Hardness / kg mm^{-2}                                          | 91.65                             |
| 50% FATT                                                       | 98.12                             |
| Primary ferrite in microstructure / %                          | 94.07                             |
| Ferrite with second phase / %                                  | 94.55                             |
| Acicular ferrite / %                                           | 94.55                             |
| Martensite / %                                                 | 94.61                             |
| Ferrite with carbide aggregate / %                             | 94.61                             |
| Weld ID                                                        | 0.00                              |


Nous constatons un très grand nombre de valeurs manquantes dans les colonnes *Primary ferrite in microstructure* (94,07 %), *Ferrite with second phase* (94,55 %), *Acicular ferrite* (94,55 %), *Martensite* (94,61 %), et *Ferrite with carbide aggregate* (94,61 %). Les valeurs manquantes de ces cinq colonnes sont des *MNAR (Missing Not At Random)*, car elles apparaissent systématiquement de manière conjointe.

Nous avons tenté de calculer le coefficient de corrélation entre chacune de ces colonnes et celles relatives à la qualité des soudures, mais il est extrêmement rare de disposer d'assez de données simultanément présentes dans deux colonnes pour effectuer ce calcul. Lors des quelques cas où cela est possible, l'une des colonnes présente généralement une variance nulle, ce qui rend la corrélation impossible ou nulle.

De ce fait, nous concluons que ces cinq colonnes ne sont pas pertinentes pour l'évaluation de la qualité des soudures et nous décidons de les supprimer du dataset. 

La colonne '50% FATT' manque aussi 98% de valeurs, ce qui nous indique son inutilité.

## Valeurs mal formattées :

Le dataset contenait déjà des mauvaises valuers (doubles espaces, trailing space) avant même l'import.
Nous imprimons les différentes valeurs de chaque colonne afin de savoir à quelle catégorie appartiennent chacun des colonnes.
Nous trouvons que dans certaines colonnes qui semblent être des variables quantitatives, on trouve des valeurs qualitatives qui semblent mal formattées.

Par exemple, pour la concentration en Nitrogène :

```
----------------------------------------
Column 'Nitrogen concentration / parts per million by weight' has 162 unique values:
[nan '72' '54' '57' '47' '44' '46' '68' '55' '53' '50' '48' '52' '89' '70'
 '41' '38' '80' '49' '77' '94' '65' '67' '58' '60' '460' '480' '160' '155'
 '67tot33res' '66totndres' '61tot34res' '54totndres' '54tot24res'
 '52tot18res' '50tot17res' '48tot18res' '78' '88' '75' '84' '85' '79' '76'
 '83' '92' '74' '86' '90' '110' '97' '99' '91' '105' '120' '150' '81' '87'
 '93' '102' '96' '66' '73' '71' '82' '145' '148' '164' '166' '235' '226'
 '243' '239' '253' '249' '240' '100' '143' '119' '539' '515' '494' '489'
 '552' '517' '520' '544' '526' '537' '529' '509' '523' '107' '114' '106'
 '117' '125' '95' '109' '64' '36' '63' '43' '39' '34' '69' '59' '37' '51'
 '56' '140' '190' '170' '124' '133' '108' '61' '122' '121' '131' '101'
 '103' '116' '138' '139' '62' '136' '540' '180' '450' '370' '250' '400'
 '430' '420' '410' '390' '260' '340' '26' '22' '21' '35' '127' '156' '245'
 '312' '266' '123' '236' '165' '113' '269' '45' '27' '42' '98' '373' '376'
 '416' '398' '394']
```
Nous devions faire des recherches sur les significations de "tot" et "res", qui font penser à "total" et "résidus", des termes chimiques correspondants à un résultat de réaction chimique.

"nd" signifierait un manque de données, "non-détecté" (en anglais *non detected*).

**Solution** : les valeurs avants 'tot' sont gardées dans la colonne et une nouvelle colonne est créee pour les résidus. Cependant, cette colonne ne contient pas assez de valeurs par rapport au dataset et sera sûrement inutile. Nous la retirons de notre analyse principale.

Nous la gardons de côté afin de peut-être observer une coincidence avec les résultats finaux (peut-être qu'une réaction avec/sans résidus aura plus de chances de produire un résultat de qualité). Nous gardons cette variable afin d'en faire une colonne booléenne : La concentration a-t-elle des résidus ? Oui/Non.



Nous avons aussi le cas de la colonne Dureté (Hardness) :

Column 'Hardness / kg mm^{-2}' has 97 unique values:
[nan '257' '227' '224' '226' '234' '217' '213' '209' '259' '239' '223'
 '230' '252' '241' '231' '229' '180' '174' '220' '184' '193' '189' '181'
 '183' '194' '216' '191' '164' '154' '265' '225' '196' '202' '197' '172'
 '158(Hv30)' '155(Hv30)' '153(Hv30)' '161(Hv30)' '168(Hv30)' '203(Hv30)'
 '157(Hv30)' '174(Hv30)' '144(Hv30)' '143(Hv30)' '154(Hv30)' '170(Hv30)'
 '459Hv10' '405Hv10' '451Hv10' '432Hv10' '264Hv10' '241Hv10' '251Hv10'
 '225Hv10' '233Hv10' '208Hv10' '373Hv10' '224Hv10' '210Hv10' '212Hv10'
 '202Hv10' '204Hv10' '201Hv10' '398Hv10' '249Hv10' '226Hv10' '234Hv10'
 '219Hv10' '467Hv10' '277Hv10' '254Hv10' '263Hv10' '237Hv10' '362Hv10'
 '291Hv10' '262Hv10' '266Hv10' '253Hv10' '257Hv10' '246Hv10' '264Hv5'
 '269Hv5' '233Hv5' '226Hv5' '222' '205' '253' '219' '182' '199' '240'
 '244' '247' '233' '212']
 

Après plusieurs recherches, nous avons découvert que Hv signifie la force effectuée sur l'objet pour obtenir un tel résultat. Comme cela est une statistique, nous la mettons aussi de côté et trions les données.


# Analyse des variables

## Variables qualitatives

### A COMPLETER 

//Mettre les variables et leurs descriptions

## Variables quantitatives