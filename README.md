# welding-quality-prediction info

# PREPROCESS DATA
Ok les gars ce que j'ai fait pour le moment:
- définition des variables path dans variables.py
- Une fonction pour virer les doubles espaces et espaces de fin de ligne
- Changer les N en NaN

Ce qu'il y a en dessous c'est juste le .tex en markdown

Pour tester l'import, lancez juste data_import.py ça génèrera un fichier dans /data/

# A FAIRE POUR LE PROJET 
Les objectifs du projet sont les suivants :


-	Faire une analyse descriptive de la base de données pour bien la maîtriser et identifier les tâches de preprocessing pertinentes à réaliser. Toute action de preprocessing devra être explicitée, décrite et justifiée. Réfléchir aux unités de mesures des variables, à la nécessité de normaliser ou non les données, appliquer une ACP pour développer de l’intuition sur la problématique, etc. 

-	Identifier quelles sont les variables représentatives de la qualité de soudure et bien les comprendre. Réfléchir à la façon de prédire la qualité de soudure à partir de ces variables identifiées. Cela implique de réfléchir à une stratégie et il est attendu de bien l’expliciter et la justifier.

-	Appliquer différentes approches de ML vues en cours et en TD sur ce dataset pour prédire la qualité de soudure. Pensez à réaliser un protocole de validation croisée rigoureux. Enfin, le dataset n’étant pas complétement labélisé, nous vous invitons à effectuer un travail bibliographique sur des méthodes de ML avancées de type semi-supervisées. Vous êtes invités à en appliquer au minimum une en justifiant votre choix et la pertinence de celle-ci. 

-	Faire une analyse comparative des performances des différents modèles et méthodes appliqués. Il est donc nécessaire de réfléchir aux choix des métriques pertinentes. 

-	Conclure sur l’approche la plus appropriée pour prédire la qualité de soudure. 

-	Après cette étude : quelles sont vos recommandations pour obtenir une bonne qualité de soudure ?

-	Écrire un rapport d’environ 5 pages synthétisant le travail effectué et les résultats obtenus. Pensez à indiquer vos noms, le numéro de votre équipe, la date, vos mails et le titre sur la première page. Pensez aussi à mettre quelques figures illustratives. Il sera attendu un plan, une section rappelant la problématique du projet et votre traduction de celle-ci en problème/tâche de ML. Une section décrivant la base de données est aussi attendue (résultat d’ACP etc.), votre compréhension des variables cibles pour prédire la qualité de soudure et comment est-ce que vous proposez de vous y prendre. Une section sur les méthodes ML que vous choisissez d’appliquer avec vos justifications (pensez à les présenter synthétiquement, surtout si elles n’ont pas été vues en cours). Une section sur les résultats numériques sera à réaliser avec une étude comparative des performances. Les formules et/ou description des métriques utilisées devront être présentées. Enfin, pensez à ajouter une dernière section de discussion et conclusion avec un diagramme de GANNT contenant le partage en tâches, le temps que chaque tâche a pris et quel membre de l’équipe s’en est chargée. Bien entendu, une section sur les références bibliographiques clôturera le rapport. Pensez à bien citer vos références dans le corps de rapport. 

-	Remarques générales : un rapport doit être paginé, les figures et tableaux doivent avoir un titre et être cités dans le corps du rapport quand on y fait référence. 


# Objectif du projet

L'objectif est d'évaluer la qualité des soudures en fonction de divers paramètres mécaniques et physiques. À première vue, les colonnes pertinentes pour cette évaluation incluent : l'allongement *(Elongation / %)*, réduction de la zone *(Reduction of Area / %)*, résistance limite d'élasticité *(Yield strength / MPa)*, résistance à la traction *(Ultimate tensile strength / MPa)*, dureté *(Hardness / kg mm^{-2})*, ténacité Charpy *(Charpy impact toughness / J)*, et température de transition de fracture (*50% FATT*).

*// À compléter*

# Valeurs manquantes et non typées

Les valeurs manquantes sont traitées dans le fichier *missing_values.py*.  

## Section 1 de *missing_values.py* : calcul du nombre de valeurs manquantes dans chaque colonne

Le fichier *missing_percent.csv*, généré par *missing_values.py*, associe à chaque colonne son pourcentage de valeurs manquantes correspondant.

## Section 2 de *missing_values.py* : suppression de quelques colonnes

Nous constatons un très grand nombre de valeurs manquantes dans les colonnes *Primary ferrite in microstructure* (94,07 %), *Ferrite with second phase* (94,55 %), *Acicular ferrite* (94,55 %), *Martensite* (94,61 %), et *Ferrite with carbide aggregate* (94,61 %). Les valeurs manquantes de ces cinq colonnes sont des *MNAR (Missing Not At Random)*, car elles apparaissent systématiquement de manière conjointe.

Nous avons tenté de calculer le coefficient de corrélation entre chacune de ces colonnes et celles relatives à la qualité des soudures, mais il est extrêmement rare de disposer d'assez de données simultanément présentes dans deux colonnes pour effectuer ce calcul. Lors des quelques cas où cela est possible, l'une des colonnes présente généralement une variance nulle, ce qui rend la corrélation impossible ou nulle.

De ce fait, nous concluons que ces cinq colonnes ne sont pas pertinentes pour l'évaluation de la qualité des soudures et nous décidons de les supprimer du dataset. 

*S'agissant de la colonne 50% FATT qui comprend également un nombre important de valeurs manquantes, xxx*

*// À compléter*

## Section 3 de *missing_values.py* : reformattage des données

Ensuite, nous avons repéré les valeurs qui ne sont pas au bon format, avec pour exemple la concentration en Nitrogène :

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
Nous devions faire des recherches sur les significations de "tot" et "res", qui font penser à "total" et "résultat"/"résidus", des termes chimiques correspondants à la concentration.

"nd" signifierait un manque de données. Nous les remplaçons donc par des valeurs NaN. 

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

Ensuite, 

 Et nous devons faire des recherches sur l'éthimologie de Hv (Hardness Value?)



# Analyse des variables

## Variables qualitatives

### A COMPLETER 

//Mettre les variables et leurs descriptions

## Variables quantitatives
