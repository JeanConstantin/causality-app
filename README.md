Web-App de détection automatique des arguments causaux en Français.

Une application Flask (python) capable de détecter automatiquement les relations discursives à caractère causal.

L'application reçoit un texte, et le découpe automatiquement en phrases verbales (un argument contenant un sujet et un verbe conjugué). Un modèle BERT français (CamemBERT) analyse l'ensemble des paires d'arguments consécutifs et les classifie en arguments de raisons ou de résultat. Un argument de résultat suit le schéma suivant: Arg1 cause Arg2, à l'inverse l'argument de raison correspond à Arg1 est causé par Arg2.

Le texte est ensuite retranscrit par l'application et les pairs d'arguments causaux (raison ou résultat) sont surlignés.
