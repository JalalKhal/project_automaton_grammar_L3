from ensembles import*
from automates_finis import*
import copy
#grammaire de travail de base
gbase_nt = ["S","B","l","dd","e","f","fkfkf"]
gbase_t = ["a","b","c"]
gbase_r = [("S",[["aaaa","B"],[None,"B"]]),("B",[["abbbcc","B"],[None,"S"]])]        
gbase_s = "S"
gbase_g = (gbase_nt,gbase_t,gbase_r,gbase_s)
#Automate de travail de base
S2=[0,1]
T2=[(0,"a",1),(0,"b",0),(0,"b",1),(1,"c",0)]
I2=[0]
F2=[1]
Abase =make_det(eq_atom,(S2,T2,I2,F2))

#Affichage--------------------------------------------------------------------------------------------------#
def print_automate(A):
	(S,T,I,F)=A
	print("état initial et final:")
	print("I:",I," et F:",F)
	print("États:")
	print(S)
	print("Transitions par ordre d'états")
	if isinstance(T,dict)==True:
		for cle in T.keys():
			if len(T[cle]):
				print("successeur de",cle,":",T[cle])
	else:
		print(T)
			
def print_grammaire(g_g):
	(g_nt,g_t,g_r,g_s)=g_g
	print("États:")
	print(g_nt)
	print("Axiome:")
	print(g_s)
	print("Alphabet:")
	print(g_t)
	print("Règles de dérivations:")
	print(g_r)
#Implementation--------------------------------------------------------------------------------------------------#



def id(s):
	"""
	Prend un entier s et le retourne ou prend une liste s=[a0,...,a_n-1] et retourne la 
	somme pour i allant de 0 à n-1 de a_i*10**i
	"""
	if isinstance(s,list)==True:
		somme=0
		for i in range(len(s)):
			somme=somme+s[i]*10**i
		return somme
	return s


def build_grammaire(eq,A):
	"""
	Prend un automate fini A DÉTERMINISTE et retourne une grammaire qui reconnait le language de A
	(quitte à le déterminiser avec la fonction du 1er TME, on peut supposer A déterministe)
	"""
	(S,T,I,F)=A
	g1_nt =[]
	g1_r=dict()
	for s in S:
		g1_nt.append(id(s))#insertion des états de l'automate
		g1_r[id(s)]=list() #list() est une liste qui contiendra les dérivations pour id(s)
		if s in F:
			g1_r[id(s)].append([chr(0),None])#chr(0) (symbole fictif) symbolise le faite que comme s est final on peut le dériver avec epsilon (None)
	g1_t =label_from_set(eq,S,T) #récupération de l'alphabet
	g1_s =[id(S[0])]#unique état initial de A qui correspond a l'axiome
	for (s1,x,s2) in T:
		g1_r[id(s1)].append([x,id(s2)]) #insertion des dérivations en fonction des transitions de A
	for liste in g1_r.values():
		if len(liste)==0:
			g1_r.remove(liste)#suppression des dérivations inéxistantes
	return (g1_nt,g1_t,g1_r,g1_s)
	

def build_automate(g_g):
	"""
	Prend une grammaire régulière G en paramètre et retourne un automate fini qui reconnait le language de G
	Pour faciliter la compréhension, il est utile de d'abord regarder la fiche explicative transmis
	"""
	(g_nt,g_t,g_r,g_s)=g_g
	S=[]#états de l'automate
	T=dict()#dictionnaire qui code la liste de transitions
	for i in range(len(g_nt)):
		S.insert(i,g_nt[i])#insertion des états de la grammaire
		T[S[i]]=list()
	S.insert(len(g_nt),"qf")
	I=g_s
	F="qf"
	for i in range(len(g_r)):
		symb=g_r[i][0] #symbole de la grammaire courante
		l=g_r[i][1]#récupération de la liste des dérivations issue de symb
		compteur=0
		for j in range(len(l)):
			tmp=l[j]#récupération de la jème dérivation associée a symb
			if l[j][1]==None:#(None=symbole fictif)
								#dérivation du type symb->a, a une lettre de l'alphabet ou epsilon
				etatf=F
			else:
				etatf=l[j][1]
			if l[j][0]==None:#dérivation du type symb->etatf(None=epsilon)
				T[symb].append((None,etatf))
			else:
				if len(l[j][0])==1:#cas pour une lettre
					T[symb].append((l[j][0],etatf))
				else:#cas pour plusieurs lettres
					taille=len(S)
					S.insert(taille,str(taille)) #création 1er état intermédiaire
					T[symb].append((l[j][0][0],str(S[taille])))#ajout de la transition
					k=0
					while k<len(l[j][0])-1: #créations des états intermédiaires suivants
						if k>0:
							S.insert(taille+k,str(k+taille))
						T[taille+k]=list()

						k=k+1
					k=0
					while k+1<len(l[j][0])-1:	
						T[taille+k].append((l[j][0][k+1],str(taille+k+1))) #ajout des transitions intermédiaires
						k=k+1
					T[taille+len(l[j][0])-2].append((l[j][0][len(l[j][0])-1],etatf))					
	return (S,T,I,F)
#Tests-----------------------------------------------------------------------------------------------------------#

print("Automate de départ(déterministe):")
print_automate(Abase)
g_g=build_grammaire(eq_atom,Abase)
print("Grammaire construite")
print_grammaire(g_g)

print("#############################################################################################")
print("Grammaire initiale:")
print_grammaire(gbase_g)
print("Automate construit")
print_automate(build_automate(gbase_g))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	


