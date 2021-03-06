# -*- coding: utf-8 -*-
##################################################################
#IMPORTS
import math
import numpy as np
import nibabel as nib
import matplotlib
import matplotlib.pyplot as plt
import os
import scipy
from scipy import ndimage as ndi

##################################################################
#FONCTIONS


#Calcul de la mesure de dissimilarit√©
def float_Dissim(array_ImgFixe, array_ImgMobi):
    float_C = 0
    for x in range(array_ImgFixe.shape[0]) :
        for y in range(array_ImgFixe.shape[1]) :
            float_C += math.pow((array_ImgFixe[x,y] - array_ImgMobi[x, y]), 2)
    float_C = float_C/(array_ImgFixe.shape[0]*array_ImgFixe.shape[1])
    return float_C

#Calcul du gradient de dissimilarit√©
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

def list_BoucleRecalage(array_ImgMobi, array_ImgFixe, list_Trans, int_NbIterations, float_PasIteration, str_Flou):
    #Initialisations
    int_ItCounter = 0
    
    list_Dissim = []
    list_Iteration = []
    list_ListTrans = []
    
    while int_ItCounter < int_NbIterations :
        
        #Interpolation de l'image
        array_ImgInterpol = ndi.interpolation.shift(array_ImgMobi, list_Trans, order = 3)
        
        #Calcul de la mesure de dissimilarit√©
        float_C = float_Dissim(array_ImgFixe, array_ImgInterpol)
        
        #Calcul du gradient de dissimilarit√©
        liste = listFl_GradDissim(array_ImgFixe, array_ImgInterpol)
        float_GradCx = liste[0]
        float_GradCy = liste[1]
        
        #Sauvegarde de la valeur de dissimilarit√©, √† l'indice correspondant au nombre d'iterations
        list_Dissim.append(float_C)
        list_ListTrans.append(list_Trans)
        list_Iteration.append(int_ItCounter)
        
        #Calcul du nouveau vecteur de transformation, et mise √† jour
        list_Trans[0] = list_Trans[0] + (float_PasIteration * float_GradCx)
        list_Trans[1] = list_Trans[1] + (float_PasIteration * float_GradCy)
        
        #Affichage du num d'it√©ration, de la valeur de dissimilarit√© et des composantes de la transformation
        print("Num. it√©ration =" + str(int_ItCounter) + " , Mesure Dissimilarit√© =" + str(round(float_C,2)) + " , Transformation T: x=" + str(round(list_Trans[0],2)) + " y=" + str(round(list_Trans[1],2)))
        
        #Sauvegarde de l'image
        matplotlib.image.imsave(cwd + '\Images\ ' + str_Flou + '_Iteration' + str(int_ItCounter) + '.png', array_ImgInterpol)    
        
        #Mise √† jour du compteur
        int_ItCounter += 1;
        
    return list_Trans

##################################################################
#MAIN
    
#Nettoyage du dossier images
for filename in os.listdir(r'Images') :
    os.remove(r'Images' + '/' + filename)

#Ouverture des diff√©rents fichiers nifty
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

list_Trans = [0,0]

#Floutage des images √† l'aide d'un filtre gaussien
img_FlouFixe = scipy.ndimage.filters.gaussian_filter(image_FixeData, sigma=5.0)
array_FlouFixe = np.array(img_FlouFixe)
img_FlouMobi = scipy.ndimage.filters.gaussian_filter(image_MobiData, sigma=5.0)
array_FlouMobi = np.array(img_FlouMobi)

#Premi√®re it√©ration de l'algorithme avec les images flout√©es
list_Trans = list_BoucleRecalage(array_FlouMobi, array_FlouFixe, list_Trans, 100, 0.00075, 'Flou')
#Seconde it√©ration de l'algorithme avec les images non flout√©es, et partant du m√™me vecteur de transformation
#que celui obtenu au terme de l'it√©ration pr√©c√©dente. Le pas est descendu pour permettre des translations plus fines,
#et ce car les plus gros mouvements ont d√©j√† √©t√©s r√©alis√©s par la premi√®re it√©ration
list_Trans = list_BoucleRecalage(array_ImgMobi, array_ImgFixe, list_Trans, 100, 0.000075, 'Net')

#Sauvegarde au format NIfTI de la derni√®re image obtenue
nii_Save = nib.Nifti1Image(ndi.interpolation.shift(array_ImgMobi, list_Trans, order = 3), nii_FixeImg.affine, header = nii_FixeImg.header)
nib.save(nii_Save, os.path.join('Resultats', 'Resultat_Flou.nii'))

