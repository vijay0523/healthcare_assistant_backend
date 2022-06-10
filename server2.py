from explainerdashboard.custom import *
from explainerdashboard import ClassifierExplainer, ExplainerDashboard
from explainerdashboard.custom import *

# db = ExplainerDashboard(explainer, mode='external',
#                         title="Heart Disease Explainer", # defaults to "Model Explainer"
#                         shap_interaction=False, # you can switch off tabs with bools
#                         )
# db.to_yaml("dashboard.yaml", explainerfile="explainer.dill", dump_explainer=True)
db = ExplainerDashboard.from_config("./dashboard.yaml", title="Awesomer Title", simple=True)
db.run()