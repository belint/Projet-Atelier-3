from PIL import Image 
import math
import os
import sys
def mosaique(chemin_im_source):
	new_size = 25
	tab_nom_image = os.listdir("base_dimage")
	tab = [0]*len(tab_nom_image)
	im_source_HSV = Image.open(chemin_im_source).convert("HSV")
	im_source_HSV = im_source_HSV.resize(((im_source_HSV.size[0]//new_size)*new_size,(im_source_HSV.size[1]//new_size)*new_size))
	cop = im_source_HSV.copy()
	pix_copy = cop.load()
		
	tab_non_convert = [0]*len(tab_nom_image)
	
	for i in range(len(tab_nom_image)):
		tab[i] = Image.open(tab_nom_image[i]).convert("RGB").convert("HSV")
		tab_non_convert[i] = Image.open(tab_nom_image[i]).convert("RGB")

	#New_size est definit plus haut et UNE fois
	redimentionne(tab,new_size)
	
	# prepa du Calcul des couleurs dominante
	tab_histo = []
	Couleur_Dominante(tab,tab_histo)
	

	Moyenne_Image_Source(im_source_HSV,new_size,tab_histo,tab,tab_non_convert,pix_copy)
	cop.show()
	return cop
 

#Redimentionnement des images    
def redimentionne(tab,new_size):
	for i in range(len(tab)):
		tab[i] = tab[i].resize((new_size,new_size))
    
#Recherche de la meilleur image
def Best_Comp(tab_histo,histo_source):
	difference_min_h,difference_min_s,difference_min_v = (10**100,)*3# pixels are in queueleuleu in histo (list)
	indice = 0
	diff_min=10**10000
	histo_source_nor = norme3(histo_source)
	for i in range(len(tab_histo)):
		histo_tempo = tab_histo[i][1]
		histo_tempo = [histo_tempo[:256],histo_tempo[256:512],histo_tempo[512:]]
		histo_tempo_nor = norme3(histo_tempo)
		difference_h,difference_s,difference_v = 0,0,0# pixels are in queueleuleu in histo (list)
		for k in range(len(histo_tempo_nor[0])): # pixels are in queueleuleu in histo (list)
			difference_h += abs(histo_tempo_nor[0][k] - histo_source_nor[0][k])**2
			difference_s += abs(histo_tempo_nor[1][k] - histo_source_nor[1][k])
			difference_v += abs(histo_tempo_nor[2][k] - histo_source_nor[2][k])

		diff = ((difference_h+1)+(difference_s+1)+(difference_v+1))**0.5

		if diff < diff_min:
			diff_min = diff
			indice = i
	return indice

#Remplacement des 25x25 pixel par la meilleur image
def Remplacement(new_size,pix_copy,pix_tempo,x,y,taille_source_x,taille_source_y):
	for y_3 in range(new_size):
		for x_3 in range(new_size):
			if (new_size*x)+x_3 < taille_source_x and (new_size*y)+y_3 < taille_source_y :
				pix_copy[(new_size*x)+x_3,(new_size*y)+y_3] = pix_tempo[x_3,y_3]
			
			
#Calcul des couleurs dominante
def Couleur_Dominante(tab,tab_histo):
	for i in range(len(tab)):
		im = tab[i]		
		histo = im.histogram()
		tab_histo.append((i,histo))


#Moyenne des 25x25 de l'image source
def Moyenne_Image_Source(im_source_HSV,new_size,tab_histo,tab,tab_non_convert,pix_copy):
	pic_source_25 = Image.new("HSV",(new_size,new_size)) #new_sizenew_sizenew_sizenew_size
	pix_source_25 = pic_source_25.load()
	pix_source_HSV = im_source_HSV.load()
	for y in range(im_source_HSV.size[1]//new_size):
		for x in range(im_source_HSV.size[0]//new_size):	
			for y_2 in range(new_size):
				for x_2 in range(new_size):
					h,s,v = pix_source_HSV[(new_size*x)+x_2,(new_size*y)+y_2]
					pix_source_25[x_2,y_2] = h,s,v	
			histo_source = pic_source_25.histogram()
			histo_source = [histo_source[:256],histo_source[256:512],histo_source[512:]]	
			indice = Best_Comp(tab_histo,histo_source)
			
			#pix_tempo = tab_non_convert[indice].load()
			pix_tempo = tab[indice].load()			
			Remplacement(new_size,pix_copy,pix_tempo,x,y,im_source_HSV.size[0],im_source_HSV.size[1])
			
def norme(histo):
	s = sum(histo)
	return [x*(1000/s) for x in histo]
		
def norme3(histo):
	return [norme(x) for x in histo]		

def main():
    if sys.argv[1] == None:
        print("Vous n'avez pas rentrer d'image")
    else :
        mosaique(sys.argv[1])
if __name__ == "__main__":
    
    main()

