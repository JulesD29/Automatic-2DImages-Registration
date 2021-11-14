# Automatic-2DImages-Registration

![Intro image](https://www.researchgate.net/profile/Ahmed-Kharrat-2/publication/215469453/figure/fig4/AS:393945428316166@1470935317478/Recalage-de-limage-cible-sur-limage-reference-Cependant-linspection-visuelle-nest.png)


*This is a project within our school curriculum. Topic proposed by ISEN Yncréa Ouest.*


## Content of the repertory
This folder contains everything needed to run the different versions of the algorithms presented in the report.
To operate these algorithms, several specifications are required: 
Python3 or higher, and the following modules:
numpy
nibabel
matplotlib
scipy
LIP

### PROGRAMMES

-**_Recalage.py_**: This program is the basic version of the registration algorithm. It allows the registration of modality images 
identical or different, but identical in size. This is done according to translations.
[Go to this project](Recalage.py)


-**_Recalage_ModaliteDiff.py_**: This evrsion makes it possible to check the correct operation of the program on 2 different modalities,
by superimposing the 2 final images obtained at 50% of their intensity.
[Go to this project](docs/_Recalage_ModaliteDiff.py)


-**_Recalage_Flou.py_**: This version of the algorhitme works in 2 steps, using Gaussian blur. It is used with
the same conditions as the first two.
[Go to this project](docs/_Recalage_Flou.py)


-**_Recalage_InfoMutuelle.py_**: This version of the algorithm performs a registration using the mutual information calculation,
to recalculate multimodal images. It uses the functions present in the MI.py file
[Go to this project](docs/_Recalage_InfoMutuelle.py)


### FOLDERS

-**_FilesStudents_**: Contains the different images used to run the algorithms
[Go to this folder](docs/FilesStudents)


-**_Images_**: Contains the images obtained at each iteration of the algorithm loop, is automatically cleaned at each
launch of the program.
[Go to this folder](docs/Images)


-**_Results_**: Contains the image obtained at the last iteration of the algorithm, saved in NIfTI format.
[Go to this folder](docs/Results)





## Results

Une porposition d'utilisation est disponible dans les dossiers ci-dessus.
Images en entrée utilisées (File in FilesStudents used) :
  --> Visualisation des résultats à chaque itération dans le dossier Images
  --> Visualisation du résultat final dans le dossier Résults

