# -*- coding: utf-8 -*-
##################################################################
#IMPORTS
import math
import numpy as np
import nibabel as nib
import matplotlib
import matplotlib.pyplot as plt
import os
from scipy import ndimage as ndi
from MI import mutual_information_2d

##################################################################
#FONCTIONS


#Calcul de la mesure de dissimilarité
def float_Dissim(array_ImgFixe, array_ImgMobi):
    float_C = 0
    for x in range(array_ImgFixe.shape[0]) :
        for y in range(array_ImgFixe.shape[1]) :
            float_C += math.pow((array_ImgFixe[x,y] - array_ImgMobi[x, y]), 2)
    float_C = float_C/(array_ImgFixe.shape[0]*array_ImgFixe.shape[1])
    return float_C


#Calcul du gradient de dissimilarité
def listFl_GradDissim(array_ImgFixe, array_ImgMobi):
    float_GradCx = 0
    float_GradCy = 0
    array_GradMobyX = np.gradient(array_ImgMobi, axis=0)
    array_GradMobyY = np.gradient(array_ImgMobi, axis=1)
    
    for x in range(array_ImgFixe.shape[0]) :
        for y in range(array_ImgFixe.shape[1]) :
            float_GradCx += (array_ImgFixe[x,y] - array_ImgMobi[x, y])*array_GradMobyX[x,y]
            float_GradCy += (array_ImgFixe[x,y] - array_ImgMobi[x, y])*array_GradMobyY[x,y]
    float_GradCx = - 2*float_GradCx/(array_ImgFixe.shape[0]*array_ImgFixe.shape[1])
    float_GradCy = - 2*float_GradCy/(array_ImgFixe.shape[0]*array_ImgFixe.shape[1])
    return [float_GradCx, float_GradCy]

##################################################################
#MAIN
    
#Nettoyage du dossier images
for filename in os.listdir(r'Images') :
    os.remove(r'Images' + '/' + filename)

#Ouverture des différents fichiers nifty
cwd = os.getcwd()


str_FixeFilename = r'fichiersEtudiants\image1.nii'
nii_FixeImg = nib.load(str_FixeFilename)
image_FixeData = nii_FixeImg.get_fdata()
array_ImgFixe = np.array(image_FixeData)

#Sauvegarde de l'image au format png
matplotlib.image.imsave(cwd + r'.\Images\Objectif.png', array_ImgFixe)

str_MobileFilename = r'fichiersEtudiants\image2.nii'
nii_MobileImg = nib.load(str_MobileFilename)
image_MobiData = nii_MobileImg.get_fdata()
array_ImgMobi = np.array(image_MobiData)


#Initialisations
list_Trans = [0,0]
int_NbIterations = 200
int_PasIteration = 0.0005
int_ItCounter = 0

list_DissimSSD = []
list_DissimMI = []
list_Iteration = []
list_ListTrans = []

while int_ItCounter < int_NbIterations :
    
    #Interpolation de l'image
    array_ImgInterpol = ndi.interpolation.shift(array_ImgMobi, list_Trans, order = 3)
    
    #Calcul de la mesure de dissimilarité par SSD
    float_C = float_Dissim(array_ImgFixe, array_ImgInterpol)
    #Calcul de la mesure de dissimilarité par l'information mutuelle
    float_C_MI = mutual_information_2d(array_ImgFixe[:,:].ravel(), array_ImgInterpol[:,:].ravel())


    #Calcul du gradient de dissimilarité
    liste = listFl_GradDissim(array_ImgFixe, array_ImgInterpol)
    float_GradCx = liste[0]
    float_GradCy = liste[1]
    
    #Sauvegarde de la valeur de dissimilarité, à l'indice correspondant au nombre d'iterations
    list_DissimSSD.append(float_C)
    list_DissimMI.append(float_C_MI)
    list_ListTrans.append(list_Trans)
    list_Iteration.append(int_ItCounter)
    
    #Calcul du nouveau vecteur de transformation, et mise à jour
    list_Trans[0] = list_Trans[0] + (int_PasIteration * float_GradCx)
    list_Trans[1] = list_Trans[1] + (int_PasIteration * float_GradCy)
    
    #Affichage du num d'itération, de la valeur de dissimilarité et des composantes de la transformation
    print("Num. itération =" + str(int_ItCounter) + " , Mesure Dissimilarité SSD =" + str(round(float_C,2)) + " / MI =" + str(round(float_C_MI,2)) + " , Transformation T: x=" + str(round(list_Trans[0],2)) + " y=" + str(round(list_Trans[1],2)))
    
    #Sauvegarde de l'image
    matplotlib.image.imsave(cwd + r'.\Images\Iteration' + str(int_ItCounter) + '.png', array_ImgInterpol)    
    
    #Mise à jour du compteur
    int_ItCounter += 1;

nii_Save = nib.Nifti1Image(ndi.interpolation.shift(array_ImgMobi, list_Trans, order = 3), nii_FixeImg.affine, header = nii_FixeImg.header)
nib.save(nii_Save, os.path.join('Resultats', 'Resultat_Pas=' + str(int_PasIteration) + '_NbIterations=' +str(int_NbIterations) + '.nii'))

#Affichage de l'évolution de la dissimilarité au fil des itérations
plt.plot(list_Iteration, list_DissimSSD, label = 'SSD' + str(int_PasIteration))
#plt.plot(list_Iteration, list_DissimMI, label = 'MI' + str(int_PasIteration))
# + ', NbIté :' + str(int_NbIterations)) #A rajouter si besoin de comparer le nb de pas
plt.title("Evolution de la dissimilarité")
plt.xlabel("Itération")
plt.ylabel("Mesure de Dissimilarité")
plt.legend()