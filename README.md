# Welding Quality Prediction

Le but de ce projet est de prédire la qualité de soudures sur des aciers. Il s’agit d’une problématique d’intérêt pour de nombreux industriels dont le secteur pèse plusieurs milliards d’euros (exemple : soudure de pipe d’éoliennes). De nos jours, la connaissance liée à la qualité des soudures se transmet principalement d’expert à expert soudeur dont les industriels sont dépendants. Il y a un gros enjeu à acquérir de la connaissance via les données pour à la fois extraire et homogénéiser la connaissance experte mais également explorer de nouvelles connaissances via des patterns que l’on pourrait découvrir par l’exploration de la donnée.

## Instructions for Running the Flask App

### To run the app

1. Install the required packages by running:

```bash
pip install -r app/requirements.txt
```

2. From the root directory of the project, run:

```bash
python app/app.py
```

3. Once the app is running, open a web browser and go to the following URL:

```
http://localhost:5123/
```

### How to use

- **Manual input**: You can enter values directly into the input fields on the webpage. Missing values will be automatically imputed where necessary, and predictions will be provided based on your inputs.
- **Upload a full file** (e.g. `data/welddb_data.csv`) through the provided file upload section in the UI. The app will generate predictions and allow you to download a CSV file with these predictions.

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

