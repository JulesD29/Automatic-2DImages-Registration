Ce dossier contient tout le nécessaire pour faire fonctionner les différentes versions des algorithmes présentés dans le rapport.
Pour faire fonctionner ces algorithmes, plusieures spécifications sont requises : 
Python3 ou supérieur, et les modules suivants :
numpy
nibabel
matplotlib
scipy
PIL
############################PROGRAMMES
-Recalage.py : Ce programme est la version de base de l'algorithme de recalage. Il permet le recalage d'images de modalité 
identiques ou différentes, mais de taille identique. Ce recalage s'effectue selon des translations.

-Recalage_ModaliteDiff.py : Cette evrsion permet de vérifier le bon fonctionnement du programme sur 2 modalités différentes,
en effectuant une superposition des 2 images finales obtenus à 50% de leur intensité.

-Recalage_Flou.py : Cette version de l'algorhitme opère un recalage en 2 temps, en utilisant le flou gaussien. Il s'utilise avec
les mêmes conditions que les 2 premiers.

-Recalage_InfoMutuelle.py : Cette version de l'algorithme opère un recalage en utilisant le calcul de l'information mutuelle,
permettant de recaller des images multimodales. Il utilise les fonctions présentes dans le fichier MI.py

#############################DOSSIERS
-fichiersEtudiants : Contient les différentes images utilisées pour faire tourner les algorithmes

-Images : Contient les images obtenues à chaque itération de la boucle de l'algorithme, est nettoyé automatiquement à chaque
lancement du programme.

-Résultats : Contient l'image obtenue à la dernière itération de l'algorithme, enregistrée au format NIfTI.