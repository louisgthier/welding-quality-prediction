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
	Faire une analyse descriptive de la base de données pour bien la maîtriser et identifier les tâches de preprocessing pertinentes à réaliser. Toute action de preprocessing devra être explicitée, décrite et justifiée. Réfléchir aux unités de mesures des variables, à la nécessité de normaliser ou non les données, appliquer une ACP pour développer de l’intuition sur la problématique, etc. 
	Identifier quelles sont les variables représentatives de la qualité de soudure et bien les comprendre. Réfléchir à la façon de prédire la qualité de soudure à partir de ces variables identifiées. Cela implique de réfléchir à une stratégie et il est attendu de bien l’expliciter et la justifier.
	Appliquer différentes approches de ML vues en cours et en TD sur ce dataset pour prédire la qualité de soudure. Pensez à réaliser un protocole de validation croisée rigoureux. Enfin, le dataset n’étant pas complétement labélisé, nous vous invitons à effectuer un travail bibliographique sur des méthodes de ML avancées de type semi-supervisées. Vous êtes invités à en appliquer au minimum une en justifiant votre choix et la pertinence de celle-ci. 
	Faire une analyse comparative des performances des différents modèles et méthodes appliqués. Il est donc nécessaire de réfléchir aux choix des métriques pertinentes. 
	Conclure sur l’approche la plus appropriée pour prédire la qualité de soudure. 
	Après cette étude : quelles sont vos recommandations pour obtenir une bonne qualité de soudure ?
	Écrire un rapport d’environ 5 pages synthétisant le travail effectué et les résultats obtenus. Pensez à indiquer vos noms, le numéro de votre équipe, la date, vos mails et le titre sur la première page. Pensez aussi à mettre quelques figures illustratives. Il sera attendu un plan, une section rappelant la problématique du projet et votre traduction de celle-ci en problème/tâche de ML. Une section décrivant la base de données est aussi attendue (résultat d’ACP etc.), votre compréhension des variables cibles pour prédire la qualité de soudure et comment est-ce que vous proposez de vous y prendre. Une section sur les méthodes ML que vous choisissez d’appliquer avec vos justifications (pensez à les présenter synthétiquement, surtout si elles n’ont pas été vues en cours). Une section sur les résultats numériques sera à réaliser avec une étude comparative des performances. Les formules et/ou description des métriques utilisées devront être présentées. Enfin, pensez à ajouter une dernière section de discussion et conclusion avec un diagramme de GANNT contenant le partage en tâches, le temps que chaque tâche a pris et quel membre de l’équipe s’en est chargée. Bien entendu, une section sur les références bibliographiques clôturera le rapport. Pensez à bien citer vos références dans le corps de rapport. 
	Remarques générales : un rapport doit être paginé, les figures et tableaux doivent avoir un titre et être cités dans le corps du rapport quand on y fait référence. 


# MAP DATA LIBRARY

## Database MAP_DATA_WELD

### 1. Provenance of Data

Tracey Cool\* and H. K. D. H. Bhadeshia, Phase Transformations Group, Department of Materials Science and Metallurgy, University of Cambridge, Cambridge, U.K.

*Tracey Cool (TC) is now with the Materials Engineering Department, Parsons Power Generation Systems Ltd, Heaton Works, Shields Road, Newcastle Upon Tyne, NE6 2YL*

### 2. Purpose

Provides chemical composition and mechanical property data for a collection of all weld metal deposits.

### 3. Description

The tar file contains data for the chemical composition of the steels studied, and their room temperature mechanical properties. These data have been collated from available literature. The presence of an "N" indicates that the value was not reported in the publication. This is *not* meant to be an indication that the value is zero. Although many columns are presented here, those which only have a small amount of data have been removed for the analysis described in [1] and [2]. This enabled more input lines to be used for neural network analysis.

#### Column Descriptions:
- **Column 1:** Carbon concentration / weight %
- **Column 2:** Silicon concentration / weight %
- **Column 3:** Manganese concentration / weight %
- **Column 4:** Sulphur concentration / weight %
- **Column 5:** Phosphorus concentration / weight %
- **Column 6:** Nickel concentration / weight %
- **Column 7:** Chromium concentration / weight %
- **Column 8:** Molybdenum concentration / weight %
- **Column 9:** Vanadium concentration / weight %
- **Column 10:** Copper concentration / weight %
- **Column 11:** Cobalt concentration / weight %
- **Column 12:** Tungsten concentration / weight %
- **Column 13:** Oxygen concentration / parts per million by weight
- **Column 14:** Titanium concentration / parts per million by weight
- **Column 15:** Nitrogen concentration / parts per million by weight
- **Column 16:** Aluminium concentration / parts per million by weight
- **Column 17:** Boron concentration / parts per million by weight
- **Column 18:** Niobium concentration / parts per million by weight
- **Column 19:** Tin concentration / parts per million by weight
- **Column 20:** Arsenic concentration / parts per million by weight
- **Column 21:** Antimony concentration / parts per million by weight
- **Column 22:** Current / A
- **Column 23:** Voltage / V
- **Column 24:** AC or DC
- **Column 25:** Electrode positive or negative
- **Column 26:** Heat input / kJ mm⁻¹
- **Column 27:** Interpass temperature / °C
- **Column 28:** Type of weld (ShMA = MMA = manual metal arc, SA = SMA = submerged arc, FCA = flux cored arc, GTAA gas tungsten arc automatic, GMAA gas metal arc automatic, SAW-NG = submerged arc narrow gap, GMA-NG = gas metal arc narrow gap, ES = electroslag, TSA = tandem submerged arc)
- **Column 29:** Post weld heat treatment temperature / °C
- **Column 30:** Post weld heat treatment time / hours
- **Column 31:** Yield strength / MPa
- **Column 32:** Ultimate tensile strength / MPa
- **Column 33:** Elongation / %
- **Column 34:** Reduction of Area / %
- **Column 35:** Charpy temperature / °C
- **Column 36:** Charpy impact toughness / J
- **Column 37:** Hardness / kg mm⁻²
- **Column 38:** 50% FATT
- **Column 39:** Primary ferrite in microstructure / %
- **Column 40:** Ferrite with second phase / %
- **Column 41:** Acicular ferrite / %
- **Column 42:** Martens

