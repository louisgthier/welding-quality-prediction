import pandas as pd
from sklearn.utils import all_estimators
from sklearn.multioutput import MultiOutputRegressor
from tqdm import tqdm
from sklearn.datasets import make_regression
from sklearn.model_selection import train_test_split

class ModelInfo:
    def __init__(self, external_models=None):
        self.models = all_estimators(type_filter='regressor')  # On filtre les modèles de régression
        # modèles externes, s'il y en a
        if external_models is not None:
            self.models.extend(external_models)
        self.model_data = []  

    def initialize_dataframe(self):
        """Initialiser un DataFrame vide pour stocker les informations des modèles."""
        columns = [
            'sk_learn_model',
            'module',
            'model_name',
            'estimator',
            'description',
            'requires_additional_parameters',
            'multi_output_native',
            'multi_output'
        ]
        return pd.DataFrame(columns=columns)

    def check_sk_learn_model(self, estimator_class):
        """Vérifier si le modèle est un modèle scikit-learn."""
        return 'sklearn' in estimator_class.__module__

    def requires_additional_parameters(self, estimator_class):
        """Déterminer si le modèle nécessite des paramètres supplémentaires."""
        try: 
            # si le modèle peut être instancié sans paramètres
            estimator_class()  
            return False  
        except TypeError: 
            # si le modèle nécessite des paramètres pour l'instanciation
            return True 

    def check_multi_output_native(self, estimator_class):
        """Tester si le modèle peut être entraîné sur des données multi-sorties."""
        # Jeu de données de régression multi-output
        X, y = make_regression(n_samples=100, n_features=4, n_targets=2, noise=0.1)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
        
        try:
            model_instance = estimator_class()
            model_instance.fit(X_train, y_train)
            # Si l'entraînement réussit, on considère que le modèle supporte le multi-output natif
            return True
        except (TypeError, ValueError):
            # Si des arguments sont nécessaires ou si le modèle ne supporte pas le multi-output
            return False

    def is_compatible_with_multioutput(self, estimator_class):
        """Tester si le modèle peut être utilisé avec MultiOutputRegressor."""
        try:
            multi_output_model = MultiOutputRegressor(estimator_class())
            return True
        except Exception:
            return False

    def add_model_info(self, name, estimator_class):
        """Ajouter les informations d'un modèle à la liste."""
        sk_learn = self.check_sk_learn_model(estimator_class)
        requires_additional = self.requires_additional_parameters(estimator_class)
        multi_output_native = self.check_multi_output_native(estimator_class)
        multi_output_via_sklearn = self.is_compatible_with_multioutput(estimator_class)

        # module du modèle
        module = estimator_class.__module__.split('.')[1] if sk_learn else "external"

        description = estimator_class.__doc__.split("\n")[0] if estimator_class.__doc__ else "No description"

        # ajout du modèle
        self.model_data.append({
            'sk_learn_model': sk_learn,
            'module': module, 
            'model_name': name,
            'estimator': estimator_class,  # Référence à l'estimator (classe du modèle)
            'description': description,
            'requires_additional_parameters': requires_additional,
            'multi_output_native': multi_output_native,
            'multi_output': multi_output_via_sklearn
        })

    def fill_dataframe(self):
        """Remplir le DataFrame en itérant sur les modèles."""
        for name, estimator_class in tqdm(self.models, desc="Filling DataFrame", leave=True):
            self.add_model_info(name, estimator_class)

        self.df_models = pd.DataFrame(self.model_data)