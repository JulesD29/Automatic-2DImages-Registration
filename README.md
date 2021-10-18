# Automatic-2DImages-Registration


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

-**_Registration.py_**: This program is the basic version of the registration algorithm. It allows the registration of modality images 
identical or different, but identical in size. This is done according to translations.

-**_Recalage_ModaliteDiff.py_**: This evrsion makes it possible to check the correct operation of the program on 2 different modalities,
by superimposing the 2 final images obtained at 50% of their intensity.

-**_Recalage_Flou.py_**: This version of the algorhitme performs a 2-step registration, using Gaussian blur....

-**_Recalage_Flou.py_**: This version of the algorhitme works in 2 steps, using Gaussian blur. It is used with
the same conditions as the first two.

-**_Recalage_InfoMutuelle.py_**: This version of the algorithm performs a registration using the mutual information calculation,
to recalculate multimodal images. It uses the functions present in the MI.py file

### FOLDERS

-**_FilesStudents_**: Contains the different images used to run the algorithms

-**_Images_**: Contains the images obtained at each iteration of the algorithm loop, is automatically cleaned at each
launch of the program.

-**_Results_**: Contains the image obtained at the last iteration of the algorithm, saved in NIfTI format.

