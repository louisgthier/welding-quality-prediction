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

De ce fait, nous concluons que ces cinq colonnes ne sont pas pertinentes pour l'évaluation de la qualité des soudures et nous décidons de les supprimer du dataset. De même pour les colonnes *Tin concentration / parts per million by weight*, *Arsenic concentration / parts per million by weight*, *Antimony concentration / parts per million by weight*, *Cobalt concentration / weight %*, *Tungsten concentration / weight %*. La colonne '50% FATT', qui manque 98% de valeurs, est aussi inexploitable du fait du manque de données en comparaison aux autres colonnes. 

Ensuite, nous supprimons les lignes contenant des missing values conjointement à toutes les colonnes qui indiquent la qualité de la soudure (Yield strength / MPa,	Ultimate tensile strength / MPa,	Elongation / %,	Reduction of Area / %,	Charpy temperature / Â°C,	Charpy impact toughness / J).  Nous remarquons qu'il y a des valeurs manquantes soit dans les deux dernières colonnes conjointement, soit dans les quatre premières colonnes conjointement, et qu'à peu près toutes les lignes contiennent au moins une valeur manquante. Supprimer les lignes qui contiennent au moins une valeur manquante ferait donc perdre une grande quantité d'information. Pour gérer les dernières valeurs manquantes de ces six colonnes indiquant la qualité de la soudure, nous pensons qu'il est préférable d'imputer des valeurs. Pour l'imputation des valeurs manquantes de la colonne 'Charpy impact toughness / J', nous optons pour une régression linéaire après avoir constaté la corrélation importante de 0.83 avec la colonne 'Reduction of Area / %'. Pour l'imputation des valeurs manquantes de la colonne 'Charpy temperature', nous optons pour une imputation KNN, comme les corrélations avec les autres colonnes sont trop faibles. L'imputation KNN permet d'imputer les valeurs manquantes en utilisant les valeurs les plus similaires des autres observations.

## Valeurs mal formattées :

Le dataset contenait déjà des mauvaises valeurs (doubles espaces, trailing space) avant même l'import.
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

**Solution** : les valeurs avants 'tot' sont gardées dans la colonne et une nouvelle colonne est créée pour les résidus. Cependant, cette colonne ne contient pas assez de valeurs par rapport au dataset et sera sûrement inutile. Nous la retirons de notre analyse principale.

Nous la gardons de côté afin de peut-être observer une coincidence avec les résultats finaux (peut-être qu'une réaction avec/sans résidus aura plus de chances de produire un résultat de qualité). Nous gardons cette variable afin d'en faire une colonne booléenne : La concentration a-t-elle des résidus ? Oui/Non.



Nous avons aussi le cas de la colonne Dureté (Hardness) :

```
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
 ```
 

Après plusieurs recherches, nous avons découvert que Hv signifie la force effectuée sur l'objet pour obtenir un tel résultat. Comme cela est une statistique, nous la mettons aussi de côté et trions les données.


Aussi, nous retrouvons souvent le signe "<" devant de nombreuses variables de concentrations, par exemple :

----------------------------------------
Column 'Tin concentration / parts per million by weight' has 21 unique values:
[nan '60' '30' '50' '40' '0' '1000' '150' '<100' '100' '200' '90' '70'
 '10' '11' '20' '140' '0.009' '0.008' '<10' '0.002']
----------------------------------------
Column 'Arsenic concentration / parts per million by weight' has 20 unique values:
[nan '10' '40' '30' '50' '70' '<100' '100' '200' '60' '150' '160' '0.01'
 '0.03' '0.008' '0.016' '0.034' '0.032' '0.31' '0.003']
----------------------------------------

Nous avons établi trois approches possibles concernant ces valeurs :

1 - Garder le nombre derrière le signe
Cela signifie que notre analyse devra être basée sur le fait que nos résultats peuvent provenir de la borne supérieure.

2 - Remplacer le nombre derrière le signe efficacement
Nous pouvons remplacer le nombre derrière le signe par la moyenne des nombres inférieurs à ce nombre, ainsi, nous restons cohérents. Problème : on renforce les liens de corrélations existants, alors pour être vraiment cohérents, on ajoute du bruit sur ces variables.

3 - Diviser le nombre derrière le signe par deux
A défaut d'avoir suffisamment de valeurs pour remplacer de façon cohérente le nombre derrière le signe, on peut partir sur la moitié du nombre afin de remplacer le signe. Cela est bien plus simple à mettre en place.

# Analyse des variables

Pour analyser les variables, nous avons simplement imprimé les valeurs unique de chaque colonne et déduit le type de chaque colonne:

```
----------------------------------------
Column 'Carbon concentration / weight %' has 81 unique values:
[0.037  0.044  0.045  0.039  0.041  0.051  0.049  0.038  0.043  0.053
 0.046  0.048  0.074  0.075  0.076  0.068  0.081  0.079  0.078  0.069
 0.08   0.071  0.072  0.066  0.067  0.09   0.088  0.091  0.089  0.094
 0.086  0.04   0.047  0.052  0.05   0.054  0.073  0.077  0.07   0.062
 0.06   0.055  0.059  0.042  0.058  0.065  0.095  0.151  0.147  0.145
 0.061  0.035  0.1    0.12   0.099  0.093  0.101  0.096  0.097  0.03
 0.032  0.031  0.098  0.13   0.11   0.057  0.15   0.064  0.082  0.036
 0.125  0.105  0.115  0.1055 0.14   0.16   0.084  0.092  0.029  0.063
 0.18  ]
----------------------------------------
Column 'Silicon concentration / weight %' has 68 unique values:
[0.3   0.31  0.35  0.33  0.32  0.36  0.29  0.34  0.39  0.44  0.48  0.37
 0.51  0.57  0.27  0.45  0.24  0.41  0.46  0.43  0.42  0.52  0.54  0.18
 0.17  0.2   0.22  0.4   0.26  0.25  0.53  0.38  0.28  0.47  0.23  0.16
 0.62  0.68  0.59  0.7   0.56  0.5   0.58  0.66  0.63  0.67  0.61  0.21
 0.49  0.12  0.13  0.15  0.11  0.19  0.14  0.415 0.08  0.04  0.07  0.55
 0.9   0.8   1.14  0.95  0.76  1.08  0.84  0.64 ]
----------------------------------------
Column 'Manganese concentration / weight %' has 147 unique values:
[0.65 1.03 1.43 1.85 0.66 1.01 1.4  0.63 1.   1.37 1.83 0.62 0.96 1.41
 1.81 0.98 1.79 1.51 1.48 1.42 1.49 1.36 1.31 1.3  1.32 1.5  1.39 1.54
 1.33 1.44 1.04 1.05 1.06 1.45 0.6  0.95 0.59 0.97 0.93 1.29 1.72 0.64
 1.02 1.22 1.35 1.74 1.73 0.99 1.77 1.76 1.17 1.2  1.19 1.24 1.34 1.64
 1.56 0.69 1.8  0.68 1.69 1.38 1.46 1.53 1.75 0.67 0.71 1.1  1.82 1.47
 1.58 1.66 1.21 0.84 0.81 0.83 0.82 0.8  0.92 1.6  1.63 1.62 2.   1.95
 1.99 0.78 1.27 1.71 2.05 0.77 1.09 1.18 1.59 2.25 0.86 2.18 1.12 1.28
 0.9  0.79 1.14 1.08 1.68 1.25 1.07 0.72 0.75 0.85 1.11 1.84 1.86 1.92
 1.9  1.94 0.55 1.15 1.52 1.67 2.22 1.88 1.91 0.73 1.61 1.16 1.93 0.94
 0.89 0.52 1.26 0.58 1.57 1.55 1.65 1.23 0.91 0.48 0.49 0.44 0.53 0.54
 0.7  0.61 0.76 0.88 0.27 0.45 1.13]
----------------------------------------
Column 'Sulphur concentration / weight %' has 34 unique values:
[0.008 0.007 0.006 0.009 0.005 0.004 0.01  0.013 0.011 0.002 0.003 0.016
 0.015 0.014 0.012 0.027 0.024 0.025 0.036 0.017 0.021 0.023 0.022 0.02
 0.018 0.026 0.028 0.032 0.029 0.03  0.019 0.001   nan 0.14 ]
----------------------------------------
Column 'Phosphorus concentration / weight %' has 36 unique values:
[0.012 0.014 0.016 0.011 0.013 0.01  0.015 0.006 0.007 0.009 0.008 0.005
 0.004 0.017 0.024 0.025 0.028 0.031 0.018 0.019 0.02  0.021 0.022 0.041
 0.058 0.026 0.027 0.029 0.045 0.03  0.037 0.075   nan 0.023 0.002 0.25 ]
----------------------------------------
Column 'Nickel concentration / weight %' has 102 unique values:
[0.    0.53  0.49  0.47  0.51  1.09  1.1   1.06  2.38  2.32  2.33  3.5
 3.46  3.47  3.42    nan 1.84  1.9   1.92  1.88  2.2   2.19  2.21  0.08
 0.98  3.01  0.93  0.03  0.02  0.05  0.04  0.55  0.58  0.62  0.01  0.77
 0.75  0.73  0.54  1.39  1.44  1.49  1.5   1.87  1.89  0.45  1.51  1.54
 1.26  0.5   1.2   0.06  0.09  0.1   0.13  0.14  0.15  0.17  0.07  0.056
 0.042 0.058 0.053 0.068 0.065 0.046 0.095 0.028 0.032 0.057 0.069 0.027
 0.067 0.055 0.085 0.21  0.31  0.22  0.69  1.01  0.2   0.036 0.16  0.27
 0.23  0.26  0.086 0.92  2.14  0.88  2.17  3.03  0.95  2.28  3.12  2.24
 3.15  0.57  0.52  0.79  0.6   0.18 ]
----------------------------------------
Column 'Chromium concentration / weight %' has 123 unique values:
[   nan  8.9    9.1    9.02   9.     8.99   8.98   9.08   0.     0.22
  0.24   0.26   0.51   0.53   0.52   1.     1.04   1.08   1.1    2.34
  2.38   2.32   2.36   0.05   9.3    9.12   9.17   9.16   9.31   9.35
  9.25   9.26   8.94   9.2    0.09   0.06   0.12   0.1    0.11   0.08
  0.07   0.027  0.41   0.79   1.22   1.57   1.97   2.28   2.8    0.5
  0.49   0.42   0.4    0.56   0.55   0.54   0.03   0.35   0.02   0.04
  0.052  0.056  0.059  0.066  0.062  0.058  0.069  0.053  0.078  0.049
  0.054  0.075  0.082  0.065  0.055  9.5    8.8    8.3    8.4    8.6
  8.7    8.75   8.77   8.57   8.58   8.61   2.68   2.63   2.7    2.22
  2.3    2.23   2.26   2.27   2.29   0.037  2.2    2.31   2.07   2.02
  2.01   2.39   2.17   2.5    2.47   2.6    2.9    1.8    2.1    2.4
  2.     2.06   1.01   1.59   1.03   1.6    2.15   1.07   1.55   1.96
  1.53   8.2   10.2  ]
----------------------------------------
Column 'Molybdenum concentration / weight %' has 80 unique values:
[  nan 1.    1.01  1.04  1.03  0.34  0.35  0.98  0.96  0.99  0.91  0.84
 0.97  0.01  0.32  0.51  0.54  0.23  0.24  0.27  0.26  0.28  0.29  0.31
 0.37  0.    0.02  0.008 0.5   0.03  0.43  0.44  0.48  0.04  0.003 0.005
 0.009 0.011 0.17  0.15  0.12  0.125 0.145 0.14  0.185 0.11  0.188 0.006
 0.3   0.025 0.18  0.22  0.39  0.022 0.016 0.018 0.017 0.015 0.82  0.93
 0.89  1.02  1.05  1.06  0.385 0.45  1.07  1.3   1.21  1.12  1.1   1.4
 1.2   1.5   0.9   0.8   1.08  0.25  1.11  0.94 ]
----------------------------------------
Column 'Vanadium concentration / weight %' has 75 unique values:
[      nan 2.200e-01 2.300e-01 2.400e-01 2.100e-01 5.000e-04 3.000e-04
 2.100e-02 4.350e-02 6.000e-02 8.150e-02 4.000e-04 2.150e-02 4.400e-02
 6.100e-02 8.500e-02 1.900e-02 4.250e-02 5.950e-02 1.005e-01 2.350e-02
 4.100e-02 6.050e-02 8.300e-02 7.000e-04 1.000e-02 2.000e-01 1.900e-01
 1.800e-01 1.100e-02 9.000e-03 1.500e-02 1.200e-02 1.300e-02 1.600e-02
 8.000e-03 6.000e-03 4.000e-03 1.400e-02 0.000e+00 2.000e-02 5.000e-03
 2.000e-03 3.000e-03 1.000e-03 1.200e-01 9.600e-02 1.220e-01 9.800e-02
 9.500e-02 1.150e-01 1.030e-01 1.100e-01 3.200e-02 3.600e-02 4.600e-02
 4.900e-02 5.000e-02 5.600e-02 1.050e-01 5.700e-02 5.500e-02 9.700e-02
 9.000e-02 8.000e-02 2.500e-01 2.900e-01 2.700e-01 3.100e-01 3.000e-01
 3.200e-01 1.800e-02 5.000e+00 1.700e-01 2.800e-01]
----------------------------------------
Column 'Copper concentration / weight %' has 75 unique values:
[  nan 0.02  0.11  0.19  0.35  0.66  1.4   0.06  0.05  0.13  0.29  0.45
 0.62  0.79  1.01  1.2   1.19  1.05  1.04  0.85  0.81  0.82  0.96  0.92
 0.89  0.87  0.57  0.56  0.55  0.03  0.38  0.4   0.42  0.04  0.43  0.
 0.08  0.12  0.14  0.1   0.18  0.28  0.22  0.25  0.23  0.15  0.26  0.24
 0.21  0.3   0.17  0.09  0.093 0.01  0.105 0.16  0.043 0.044 0.053 0.048
 0.106 0.076 0.041 0.072 0.035 0.128 0.51  0.5   1.03  1.6   0.53  1.44
 1.06  1.63  1.08 ]
----------------------------------------
Column 'Cobalt concentration / weight %' has 13 unique values:
[  nan 0.    0.95  1.89  2.8   0.92  1.87  0.02  0.01  0.005 0.017 0.021
 0.016]
----------------------------------------
Column 'Tungsten concentration / weight %' has 8 unique values:
[ nan 0.   1.03 1.92 2.99 0.98 0.97 0.1 ]
----------------------------------------
Column 'Oxygen concentration / parts per million by weight' has 269 unique values:
[  nan  400.  390.  380.  410.  471.  461.  476.  446.  436.  444.  432.
  422.  431.  423.  375.  407.  381.  374.  379.  360.  312.  397.  427.
  418.  454.  294.  373.  466.  439.  451.  642.  604.  591.  592.  636.
  596.  567.  538.  428.  435.  411.  399.  426.  429.  419.  447.  405.
  415.  413.  460.  368.  424.  393.  417.  370.  409.  433.  406.  330.
  320.  353.  366.  323.  339.  371.  401.  305.  365.  396.  408.  376.
  351.  290.  272.  472.  362.  306.  464.  394.  361.  329.  441.  346.
  324.  475.  459.  392.  337.  291.  282.  404.  341.  278.  285.  297.
  391.  315.  286.  322.  490.  345.  300.  280.  634.  651.  664.  610.
  672.  687.  666.  656.  669.  640.  667.  695.  662.  443.  430.  450.
  395.  364.  336.  321.  310.  421.  491.  326.  318.  342. 1100. 1300.
  622.  780.  837.  781.  796.  684.  816.  495.  412.  690.  736.  771.
  788.  416.  463.  467.  250.  190.  210.  240.  230.  200.  220.  176.
  155.  174.  171.  168.  152.  185.  146.  148.  165.  142.  132.  590.
  563.  521.  502.  487.  575.  425.  228.  233.  511.  569.  621.  543.
  584.  609.  253.  236.  357.  255.  455.  260.  218.  262.  340.  420.
  480.  440.  540.  510.  530.  470.  500.  850.  520.  254.  166.  256.
  292.  344.  243.  334.  303.  283.  237.  660.  350.  891.  768.  922.
  735.  556.  694.  550.  730.  560.  580.  620. 1650. 1440.  750.  680.
 1150. 1180. 1070. 1020.  570.  269.  265.  258.  268.  252.  234.  465.
  479.  513.  434.  307.  789.  774.  821.  699.  765.  711.  720.  646.
  473.  488.  438.  504.  492.  477.  519.  498.  457.  482.  453.  456.
  481.  484.  363.  372.  327.]
----------------------------------------
Column 'Titanium concentration / parts per million by weight' has 89 unique values:
[     nan 4.00e+01 5.00e+00 4.00e+00 3.70e+01 4.30e+01 3.60e+01 3.80e+01
 9.90e+01 8.80e+01 9.20e+01 6.30e+01 6.90e+01 8.00e+01 1.80e+02 1.90e+02
 2.60e+02 2.40e+02 4.60e+02 4.20e+02 4.50e+02 3.90e+01 4.20e+01 3.10e+01
 3.40e+01 4.10e+01 3.20e+01 2.90e+01 3.00e+01 3.50e+01 2.70e+01 2.50e+01
 3.30e+01 6.00e+00 1.60e+01 2.20e+01 2.80e+01 5.50e+01 7.70e+01 1.00e+02
 1.40e+02 2.10e+02 2.55e+02 8.00e+00 9.60e+01 1.60e+02 2.25e+02 7.00e+00
 7.50e+01 2.15e+02 1.05e+02 1.70e+02 1.00e+00 9.00e+01 1.20e+02 4.10e+02
 5.50e+02 5.10e+01 3.00e+02 5.90e+02 4.60e+01 3.20e+02 6.90e+02 1.50e+02
 1.30e+02 1.10e+02 2.20e+02 2.80e+02 3.10e+02 5.70e+02 3.90e+02 2.00e+01
 7.00e+01 4.30e+02 5.20e+01 5.00e+01 6.00e+01 2.30e+02 2.50e+02 2.90e+02
 2.00e+02 6.40e+01 0.00e+00 5.00e-01 1.00e+01 1.15e+02 1.00e-02 1.90e+01
 2.30e+01]
----------------------------------------
Column 'Nitrogen concentration / parts per million by weight' has 154 unique values:
[ nan  72.  54.  57.  47.  44.  46.  68.  55.  53.  50.  48.  52.  89.
  70.  41.  38.  80.  49.  77.  94.  65.  67.  58.  60. 460. 480. 160.
 155.  66.  61.  78.  88.  75.  84.  85.  79.  76.  83.  92.  74.  86.
  90. 110.  97.  99.  91. 105. 120. 150.  81.  87.  93. 102.  96.  73.
  71.  82. 145. 148. 164. 166. 235. 226. 243. 239. 253. 249. 240. 100.
 143. 119. 539. 515. 494. 489. 552. 517. 520. 544. 526. 537. 529. 509.
 523. 107. 114. 106. 117. 125.  95. 109.  64.  36.  63.  43.  39.  34.
  69.  59.  37.  51.  56. 140. 190. 170. 124. 133. 108. 122. 121. 131.
 101. 103. 116. 138. 139.  62. 136. 540. 180. 450. 370. 250. 400. 430.
 420. 410. 390. 260. 340.  26.  22.  21.  35. 127. 156. 245. 312. 266.
 123. 236. 165. 113. 269.  45.  27.  42.  98. 373. 376. 416. 398. 394.]
----------------------------------------
Column 'Aluminium concentration / parts per million by weight' has 74 unique values:
[     nan 6.00e+00 6.00e+01 1.50e+02 2.50e+02 4.20e+02 6.60e+02 5.00e+00
 7.80e+01 1.90e+02 3.40e+02 4.90e+02 6.10e+02 8.00e+00 4.70e+01 1.60e+02
 2.80e+02 4.80e+02 6.40e+02 3.00e+00 3.20e+02 4.40e+02 6.80e+02 1.00e+00
 6.70e+01 3.00e+02 5.00e+02 2.00e+01 4.40e+01 1.20e+02 9.00e+01 8.00e+01
 7.00e+01 3.00e+01 5.00e+01 1.10e+02 2.10e+02 4.60e+02 5.10e+02 4.00e+01
 1.30e+02 3.70e+02 1.80e+02 1.70e+02 1.40e+02 2.00e+02 2.40e+02 2.20e+02
 2.30e+02 2.70e+02 3.50e+01 4.50e+01 6.90e+01 8.80e+01 5.70e+01 4.30e+01
 5.30e+01 1.08e+02 1.05e+02 1.25e+02 1.28e+02 4.20e+01 1.00e+02 3.10e+02
 2.60e+02 1.00e-02 1.40e-02 5.00e-03 4.00e-03 1.30e-02 1.00e+01 3.30e+02
 4.00e+02 3.50e+02]
----------------------------------------
Column 'Boron concentration / parts per million by weight' has 30 unique values:
[nan  3. 17. 32. 64. 19. 36. 69.  5.  1.  2. 16. 28. 21. 25. 26. 15. 14.
 12. 11. 13.  7.  8. 10.  6.  9. 40. 44. 20. 22.]
----------------------------------------
Column 'Niobium concentration / parts per million by weight' has 60 unique values:
[  nan  520.  530.  620.  700.  510.  560.    5.    6.  120.  220.  450.
  880.  255.  465.  985.  105.  235.  455.  940.  125.  230.  895.  460.
  430.  470.  410.  580.  440.   30.   20.   70.   90.  100.   10.   60.
  330.  320.  310.  200.  210.  190.  150.   40.    0.   50.  300.  180.
  160.  170.   80.  140.  900.  800.  340.  240.   68.  260.  500. 1000.]
----------------------------------------
Column 'Tin concentration / parts per million by weight' has 19 unique values:
[    nan 6.0e+01 3.0e+01 5.0e+01 4.0e+01 0.0e+00 1.0e+03 1.5e+02 1.0e+02
 2.0e+02 9.0e+01 7.0e+01 1.0e+01 1.1e+01 2.0e+01 1.4e+02 9.0e-03 8.0e-03
 2.0e-03]
----------------------------------------
Column 'Arsenic concentration / parts per million by weight' has 19 unique values:
[    nan 1.0e+01 4.0e+01 3.0e+01 5.0e+01 7.0e+01 1.0e+02 2.0e+02 6.0e+01
 1.5e+02 1.6e+02 1.0e-02 3.0e-02 8.0e-03 1.6e-02 3.4e-02 3.2e-02 3.1e-01
 3.0e-03]
----------------------------------------
Column 'Antimony concentration / parts per million by weight' has 23 unique values:
[    nan 2.0e+01 3.0e+01 5.0e+01 1.0e+01 4.0e+01 6.0e+01 8.0e+01 9.0e+01
 1.4e+02 6.4e+01 0.0e+00 7.0e+01 1.2e+02 1.5e+02 1.0e+02 2.0e+02 5.0e+00
 4.0e+00 1.5e+01 8.0e-03 9.0e+00 1.0e-03]
----------------------------------------
Column 'Current / A' has 38 unique values:
[170.  180.  165.  280.  285.  680.  665.  670.  640.  660.  700.    nan
 625.  550.  850.  650.  450.  181.  201.  116.  115.  163.  145.  143.
 146.  400.  390.  300.  275.  500.  535.  290.  277.5 150.  525.  545.
 900.  190. ]
----------------------------------------
Column 'Voltage / V' has 25 unique values:
[21.   34.   24.   25.   23.   30.   32.     nan 75.36 72.24 28.   35.
 33.   38.   22.   20.   31.5  11.5  12.5  28.5  29.   63.   26.   27.
 37.5 ]
----------------------------------------
Column 'AC or DC' has 3 unique values:
['DC' 'AC' nan]
----------------------------------------
Column 'Electrode positive or negative' has 4 unique values:
['+' '0' '-' nan]
----------------------------------------
Column 'Heat input / kJ mm^{-1}' has 38 unique values:
[1.     2.     2.1    1.8    2.8    2.9    3.3    4.6    5.3    4.8
 2.7    2.2    2.5    2.4    2.6    1.9    1.7    1.6    4.4    3.6
 0.6    4.3    7.9    7.6    1.3    1.4    1.2    1.1    2.04   1.96
 2.08   1.85   1.75   3.7    2.025  2.475  2.925  1.0925]
----------------------------------------
Column 'Interpass temperature / °C' has 15 unique values:
['200' '150' '175' '107' '100' '250' '140' '300' '20' '240' '150-200'
 '177' '125' '225' '210']
----------------------------------------
Column 'Type of weld' has 10 unique values:
['MMA' 'ShMA' 'FCA' 'SA' 'TSA' 'SAA' 'GTAA' 'GMAA' 'NGSAW' 'NGGMA']
----------------------------------------
Column 'Post weld heat treatment temperature / °C' has 20 unique values:
[250.   0. 580. 750. 500. 620. 200. 600.  nan 720. 740. 760. 746. 690.
 550. 605. 482. 593. 704. 700.]
----------------------------------------
Column 'Post weld heat treatment time / hours' has 22 unique values:
[14.    0.    2.    8.    1.   16.    2.1   1.3   1.7   2.3    nan  0.75
  4.   10.   24.    1.83  2.33  1.92  4.5   3.   20.    3.5 ]
----------------------------------------
Column 'Yield strength / MPa' has 330 unique values:
[392.    nan 370.  413.  402.  468.  436.  514.  479.  411.  401.  464.
 426.  509.  450.  547.  526.  423.  475.  443.  498.  470.  566.  521.
 466.  431.  489.  481.  567.  530.  621.  574.  482.  525.  584.  692.
 662.  484.  471.  502.  462.  488.  453.  504.  513.  499.  568.  583.
 444.  437.  469.  478.  485.  491.  442.  474.  486.  452.  467.  522.
 535.  531.  538.  561.  542.  642.  643.  558.  569.  609.  620.  422.
 410.  463.  500.  446.  417.  494.  460.  543.  617.  570.  472.  427.
 626.  548.  592.  587.  534.  655.  605.  738.  808.  697.  393.  387.
 398.  391.  480.  397.  403.  409.  329.  458.  490.  483.  332.  456.
 434.  505.  493.  372.  455.  536.  527.  599.  414.  523.  578.  589.
 639.  415.  451.  549.  544.  447.  492.  553.  540.  615.  603.  539.
 586.  610.  614.  524.  575.  606.  577.  654.  638.  440.  435.  430.
 433.  465.  497.  487.  373.  386.  418.  394.  461.  449.  515.  588.
 404.  333.  396.  351.  365.  381.  359.  375.  399.  420.  419.  429.
 510.  445.  473.  546.  552.  665.  673.  768.  700.  798.  765.  795.
 573.  551.  672.  920.  416.  550.  612.  591.  628.  677.  632.  701.
 693.  408.  506.  400.  496.  541.  516.  649.  576.  556.  571.  678.
 636.  601.  585.  555.  507.  456.2 430.7 475.8 491.5 420.9 503.3 500.3
 479.7 369.8 486.8 453.8 553.3 478.5 561.1 420.8 387.5 630.8 605.3 540.5
 562.1 483.6 536.6 487.6 453.2 455.2 519.9 390.1 388.  383.  371.  389.
 517.  554.  747.  352.  349.  350.  376.  353.  689.  503.  380.  441.
 511.  438.  341.  405.  508.  529.  533.  495.  604.  454.  390.  448.
 501.  600.  661.  715.  690.  784.  641.  720.  740.  580.  630.  562.
 355.  330.  581.  593.  648.  613.  559.  631.  644.  663.  669.  432.
 457.  650.  625.  629.  647.  682.  728.  557.  598.  596.  597.  608.
 520.  537.  595.  776.  719.  646.  619.  594.  315.  379.  337.  356.
 428.  439.  378.  560.  528.  565.  477.  512.  637.  624.  706.  830.
 825.  734.  834.  822.  660.  832. ]
----------------------------------------
Column 'Ultimate tensile strength / MPa' has 307 unique values:
[ 466.     nan  456.   498.   490.   551.   529.   588.   576.   484.
  475.   522.   506.   568.   536.   618.   612.   497.   493.   541.
  521.   569.   557.   641.   538.   518.   567.   561.   635.   615.
  684.   665.   560.   605.   599.   682.   677.   753.   745.   563.
  578.   548.   566.   549.   586.   572.   593.   607.   647.   673.
  527.   542.   545.   540.   564.   570.   547.   514.   533.   555.
  535.   580.   591.   594.   583.   587.   604.   622.   616.   697.
  723.   778.   777.   705.   709.   743.   496.   532.   519.   575.
  559.   620.   510.   603.   600.   674.   650.   531.   592.   676.
  630.   671.   652.   619.   722.   683.   789.   731.   865.   757.
  500.   499.   504.   543.   528.   550.   494.   447.   513.   481.
  546.   526.   461.   534.   515.   554.   609.   590.   589.   638.
  642.   571.   602.   617.   626.   597.   681.   553.   539.   614.
  621.   655.   651.   685.   686.   627.   660.   661.   708.   716.
  512.   523.   508.   505.   524.   448.   476.   502.   525.   465.
  623.   679.   537.   579.   654.   450.   492.   457.   480.   516.
  470.   517.   488.   507.   544.   577.   565.   584.   573.   611.
  639.   581.   631.   715.   680.   807.   785.   858.   875.   895.
  596.   690.   762.   751.   866.  1151.   696.   672.   702.   698.
  738.   701.   556.   688.   737.   727.   664.   741.   748.   783.
  552.   582.   491.   694.   714.   810.   829.   761.   869.   529.8
  519.9  564.1  573.9  541.5  591.5  600.4  583.7  555.2  552.3  486.6
  569.3  536.3  626.9  643.5  577.5  504.2  482.7  725.9  694.5  645.5
  640.6  586.6  532.7  627.8  596.4  593.5  487.6  747.   459.   462.
  503.   689.   625.   486.   633.   501.   478.   453.   629.   657.
  452.   707.   670.   732.   692.   766.   704.   562.   735.   624.
  744.   740.   644.   718.   649.   598.   717.   712.   734.   756.
  817.   726.   767.   772.   610.   770.   658.   653.   678.   730.
  703.   700.   675.   901.   909.   811.   585.   713.   648.   693.
  666.   669.   736.   613.   530.   482.   477.   483.   487.   509.
  558.   636.   468.   699.   687.   720.   710. ]
----------------------------------------
Column 'Elongation / %' has 136 unique values:
[31.9  nan 35.2 31.2 31.  29.4 31.6 28.  27.4 32.6 34.2 29.6 28.6 28.2
 26.  26.8 30.6 33.6 31.8 28.4 30.2 26.4 32.2 29.1 23.6 26.6 23.5 30.4
 31.4 27.6 25.4 22.2 24.  29.8 24.2 24.6 25.2 24.4 26.2 29.2 27.2 30.7
 23.8 22.  23.2 22.6 18.8 17.1 16.8 15.7 20.8 17.4 16.9 30.  27.  29.
 28.8 25.8 23.  21.6 22.8 21.4 19.6 19.8 20.  18.6 18.2 33.4 32.5 32.8
 33.3 36.4 30.8 25.6 31.1 25.  24.8 27.1 21.8 22.4 20.2 20.6 19.  19.2
 17.2 33.  35.6 34.4 35.  34.  32.4 30.5 32.  27.8 24.9 16.6 18.  21.
 18.4 13.6 10.6 21.9 23.7 18.9 18.7 17.3 20.7 27.5 29.5 24.5 22.7 22.1
 20.5 25.5 37.  36.  15.  16.  17.  34.8 34.6 14.  25.3 24.3 24.7 21.7
 23.3 21.5 22.5 11.  32.3 23.4 20.4 19.4 17.8 18.5]
----------------------------------------
Column 'Reduction of Area / %' has 123 unique values:
[80.6  nan 78.7 78.8 76.8 76.9 79.3 77.8 79.7 74.9 72.9 77.9 76.  74.
 72.7 73.  73.9 70.7 76.6 48.8 70.8 69.7 67.5 77.  78.  78.9 80.7 79.8
 81.6 81.4 71.9 75.  65.3 59.1 59.8 60.2 64.5 62.7 61.9 58.8 70.2 68.7
 70.9 72.  67.  65.2 77.5 80.5 80.3 79.6 77.4 75.9 76.4 78.2 78.1 78.4
 68.6 81.5 82.4 82.3 83.  79.9 69.8 78.6 74.5 69.  66.  65.  62.  61.2
 56.8 47.6 64.4 66.7 59.3 59.  49.6 58.1 63.7 58.  53.  54.  49.  46.
 48.  41.  51.  44.  42.  28.  73.5 70.5 73.7 71.5 71.  70.4 72.4 64.2
 68.5 66.5 68.  64.  56.  70.  63.  60.  61.  50.  55.  52.  32.  40.
 73.2 69.1 69.9 68.8 24.  41.8 43.  44.6 17.  80.  47. ]
----------------------------------------
Column 'Charpy temperature / °C' has 139 unique values:
[  nan  -28.  -38.  -48.  -44.  -53.  -58.  -40.  -55.  -51.  -20.  -39.
    1.  -50.  -41.  -59.  -30.  -26.  -63.  -18.   56.   24.  -19.  -15.
  -56.  -25.  -62.  -76.  -29.  -99.  -72.  -77.  -86.  -88.  -90.  -74.
  -52.  -57.  -31.  -68.  -61.  -70.  -54.  -67.  -35.  -64.  -47.  -42.
  -78.  -60.  -69.  -65.  -49.  -43.  -24.  -13.   12.  -17.   10.   53.
    0.   21.   59.  -14.   31.  -22.   -9.   -1.   38.    8.   32.  -45.
   -2.  -12.  -10.   28.    9.   -3.   16. -100.  -95.  -94.  -75.  -89.
  -91.  -92.  -84.  -80.  -81.  -66.  -36.  -71.  -33.  -27.   -7.   -4.
   13.   18.  -11.   14.  -23.    7.   -6.    4.   20.  -85.  -82.  -46.
   -5.  -32.  -73.   11.   30.   33.   37.   51.   55.   34.  -37.   40.
   22.   27.    2.  -79.   60.   70.   50.  188.  -98.  -87.   26.  -83.
 -113. -114.   -8.    6.   23. -102.  -93.]
----------------------------------------
Column 'Charpy impact toughness / J' has 168 unique values:
[ nan 100.  28.  50.   9.  15.  53. 117. 220. 222.  21.  38.  74. 182.
  81. 129. 172.  36.  76. 153. 203.  13.  27.  78. 178.  45. 155. 201.
  30.  72. 119. 165. 206.  55.  89. 121. 161. 188.  23.  95. 157.  11.
  34. 110. 106. 133. 208. 114. 151.  64. 131.  17.  63.  98. 150. 197.
  57.  80. 104. 184.  32.  42. 160.   5.  12.  48. 136. 212.  10. 152.
 195.  29.  71. 143. 186.  88. 167. 183.  43. 190. 200.  86. 124. 176.
 181.  20. 171. 179. 174.  39. 148. 198.  60. 162. 126. 140. 138. 145.
  52. 107.  35.  14.  61. 105.  40.  49.  99. 111.  25.  51.  79. 102.
  16.  37.  67.  92.  41. 139. 134. 168. 180.  22.  59. 128. 144.  91.
 122. 135. 113.  70.   8.  44.  83. 193. 164. 147.  96.  68. 270. 238.
 127.  18. 149.  24. 118.  19. 204. 210.   6. 120.   3.  65. 123.  46.
 154.  31.  93.  56.  62. 231. 170. 224. 227. 175. 221. 141. 233. 199.]
----------------------------------------
Column 'Hardness / kg mm^{-2}' has 81 unique values:
[ nan 257. 227. 224. 226. 234. 217. 213. 209. 259. 239. 223. 230. 252.
 241. 231. 229. 180. 174. 220. 184. 193. 189. 181. 183. 194. 216. 191.
 164. 154. 265. 225. 196. 202. 197. 172. 158. 155. 153. 161. 168. 203.
 157. 144. 143. 170. 459. 405. 451. 432. 264. 251. 233. 208. 373. 210.
 212. 204. 201. 398. 249. 219. 467. 277. 254. 263. 237. 362. 291. 262.
 266. 253. 246. 269. 222. 205. 182. 199. 240. 244. 247.]
----------------------------------------
Column '50% FATT' has 21 unique values:
[  nan    6.  -10.  -40.  -60. -126. -106.    7.  -15.  -73.  -64.  -68.
    5.    0.   15.   30.   10.   25.  -51.  -34.  -35.]
----------------------------------------
Column 'Weld ID' has 1490 unique values:
['Evans-Ni/CMn-1990/1991-0Aaw' 'Evans-Ni/CMn-1990/1991-0Aawch'
 'Evans-Ni/CMn-1990/1991-0Aht' ... 'Birmingham-MAX37' 'Birmingham-MAX38'
 'Birmingham-MAX39']
----------------------------------------
Column 'Nitrogen residual concentration' has 6 unique values:
[nan 33. 34. 24. 18. 17.]
----------------------------------------
Column 'Hardness scale' has 4 unique values:
[nan 30. 10.  5.]
----------------------------------------
```

## Variables qualitatives

### Weld ID

### Type of weld

### AC or DC

Outre les 13 % de valeurs manquantes, cette colonne contient uniquement deux catégories : AC et DC. Pour rendre ces données plus exploitables, nous avons décidé de convertir les valeurs en format binaire : 0 pour le mode AC et 1 pour le mode DC.

Les valeurs manquantes semblent être des MAR (Missing At Random), liées au type de WeldID. En effet, les valeurs manquantes apparaissent pour des types de WeldID tels que p..-RR82011, RC81033, EvansLetter, et Birmingham. Nous pouvons imputer ces valeurs de manière fiable : lorsque la polarité de l'électrode est explicitement indiquée par un signe + ou -, il s'agit très probablement du mode DC, puisque le mode AC (courant alternatif) n'a pas de polarité fixe. Ainsi, lorsqu'une polarité d'électrode est spécifiée, nous imputons le mode DC.

Cependant, il arrive parfois que des valeurs soient également manquantes dans la colonne indiquant la polarité de l'électrode. Dans ces cas, nous examinons les autres colonnes. Nous constatons que les dernières valeurs manquantes dans la colonne AC/DC apparaissent principalement lorsque le type de soudure est MMA (Manual Metal Arc), un procédé qui est souvent plus stable et efficace en mode DC, surtout dans des conditions exigeant une grande stabilité de l'arc. Bien que le mode AC soit parfois utilisé en MMA, DC est généralement préféré pour éviter les problèmes de stabilité et améliorer la performance du soudage. Il parait donc plus probable que les valeurs manquantes soient des valeurs DC. De plus, 97 % des valeurs de la colonne sont déjà en mode DC. L'imputation des valeurs manquantes en 1 (ie mode DC) est donc en accord avec la distribution générale des données.

### Electrode positive or negative

Nous avons identifié quatre types de valeurs possibles dans cette colonne : +, -, ou 0, et les valeurs manquantes. Les 0 sont liés à l'utilisation du mode AC. 

Nous devons transformer les valeurs présentes afin qu'elles soient interprétables par les algorithmes de ML. Plutôt que d'effectuer un one-hot encoding en créant trois colonnes binaires distinctes, ce qui pourrait entraîner de la multicollinéarité et poser des problèmes pour certains algorithmes de ML, nous choisissons de diviser la colonne en seulement deux colonnes binaires : la première indiquera si l'électrode est positive (+), et la seconde si elle est négative (-). Si la valeur est 0 (par exemple dû à un mode AC) ou s'il y a une valeur manquante, les deux colonnes afficheront 0.

## Variables quantitatives



### Ferrite with carbide aggregate / %

### Martensite / %

### Acicular ferrite / %

### Ferrite with second phase / %

### Primary ferrite in microstructure / %

### 50% FATT

### Hardness / kg mm^{-2}

### Charpy impact toughness / J

### Charpy temperature / °C

### Reduction of Area / %

### Elongation / %

### Ultimate tensile strength / MPa

### Yield strength / MPa







### Post weld heat treatment time / hours

### Post weld heat treatment temperature / °C

### Interpass temperature / °C

### Heat input / kJ mm^{-1}

### Voltage / V

### Current / A

### Antimony concentration / parts per million by weight

### Arsenic concentration / parts per million by weight

### Tin concentration / parts per million by weight

### Niobium concentration / parts per million by weight

### Boron concentration / parts per million by weight

### Aluminium concentration / parts per million by weight

### Nitrogen concentration / parts per million by weight

### Titanium concentration / parts per million by weight

### Oxygen concentration / parts per million by weight

### Carbon concentration / weight %

### Silicon concentration / weight %

### Manganese concentration / weight %

### Sulphur concentration / weight %

### Phosphorus concentration / weight %

### Nickel concentration / weight %

### Chromium concentration / weight %

### Molybdenum concentration / weight %

### Vanadium concentration / weight %

### Copper concentration / weight %

### Cobalt concentration / weight %

### Tungsten concentration / weight %
