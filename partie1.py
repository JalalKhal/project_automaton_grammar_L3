#---------------------------------------------#
## Exemple tests avec differentes Grammaires :
# S → A1 | A2 | A3
# A1 → aA1A1 | aA2A4 | aA3A7 | A4
# A2 → aA1A2 | aA2A5 | aA3A8 | A5
# A3 → aA1A3 | aA2A6 | aA3A9 | A6
# A4 → bA4
# A5 → bA5
# A6 → bA6 | ε
# A9 → c
#---------------------------------------------#Pas regu

g1_variables = ["S","A1","A2","A3","A4","A5","A6","A7","A8","A9"]
g1_alphabet = ["a","b","c"]
g1_regles = [("S",[["A1"],["A2"],["A3"]]),\
("A1",[["a","A1","A1"],["a","A2","A4"],["a","A3","A7"],["A4"]]),\
("A2",[["a","A1","A2"],["a","A2","A5"],["a","A3","A8"],["A5"]]),\
("A3",[["a","A1","A3"],["a","A2","A6"],["a","A3","A9"],["A6"]]),\
("A4",[["b","A4"]]),\
("A5",[["b","A5"]]),\
("A6",[["b","A6"],[None]]),\
("A9",[["c"]])]
g1_axiome = "S"
#---------------------------------------------#Regu droite
# s -> A1 | A2 | A3
#A1 -> abA1 | A2 | epslione |A3
# A2 -> abc
#A3 -> epsilone
g2_variables=["S","A1","A2"] #elle regu droite
g2_alphabet = ["a","b","c"]
g2_regles = [("S",[["A1"],["A2"],["A3"]]),\
("A1",[["a","b","A1"],["A2"],[None],["A3"]]),\
("A2",[["a","b","c"]]),\
("A3",[[None]])]
g2_axiome = "S"
#--------------------------------------------#Regu gauche
# s -> A1 | A2 | A3
#A1 -> A1ab | A2 | epsilone |A3
# A2 -> epsilone
g3_variables=["S","A1","A2"] #elle regu droite
g3_alphabet = ["a","b","c"]
g3_regles = [("S",[["A1"],["A2"],["A3"]]),\
("A1",[["A1","a","b"],["A2"],[None],["A3"]]),\
("A2",[["a","b","c"]]),\
("A3",[[None]])]
g3_axiome = "S"
#--------------------------------------------# #Pas regu
# s -> A1A2 | A2 | A3
#A1 -> A1ab | A2 | epsilone |A3
# A2 -> epsilone
g4_variables=["S","A1","A2"] #elle regu droite
g4_alphabet = ["a","b","c"]
g4_regles = [("S",[["A1","A2"],["A2"],["A3"]]),\
("A1",[["A1","a","b"],["A2"],[None],["A3"]]),\
("A2",[["a","b","c"]]),\
("A3",[[None]])]
g4_axiome = "S"
#--------------------------------------------#
g1_g = [g1_alphabet,g1_variables,g1_regles,g1_axiome]
g2 = [g2_alphabet,g2_variables,g2_regles,g2_axiome]
g3 = [g3_alphabet,g3_variables,g3_regles,g3_axiome]
g4 = [g4_alphabet,g4_variables,g4_regles,g4_axiome]
#--------------------------------------------#
def que_des_lettres_de_alphabet(alphabet,liste):
    #return false si un element n'est pas dans l'alphabet dans liste.
    for element in liste:
        if(element not in alphabet):
            return False
    return True

def qu_une_variable(variables,liste):
    #return false si on moins 2 elements appartenant aux symboles de variables dans liste.
    compteur=0
    for element in liste:
        if(element in variables):
            compteur=compteur+1
    if(compteur==1 or compteur==0): #pas de variable ou une variable
        return True
    return False
        
#---------------------------------------------#
def est_regu_droite(grammaire):
    # du type V × (Σ^{∗}V ∪ Σ^{*})
    alphabet=grammaire[0]
    variables=grammaire[1]
    regles=grammaire[2]
    for regle in regles: #(s,[les regles])
        liste_regle = regle[1] #les regles list de list
        for une_regle in liste_regle: #une regle du type ["a","A1","A1"] pour désigner -> aA1A1
            if(len(une_regle)==1): #pour pas avoir de probleme avec l'epsilon transition.
                continue
            if(qu_une_variable(variables,une_regle)==False): #on a plusieurs variables du types aaBaaC donc c'est déjà faux.
                return False
            if(une_regle[-1] not in variables and que_des_lettres_de_alphabet(alphabet,une_regle)==False):# Ce n'est pas que des lettres de l'alphabet du type aaa et la dernier élement n'est pas une variable du type aAa ou Aaa c'est donc faux.
                return False #déjà on a un problèmes
            #l'on continue tout est bon
    return True
#---------------------------------------------#
def est_regu_gauche(grammaire):
    # du type V × (VΣ{∗} ∪ Σ^{*})
    alphabet=grammaire[0]
    variables=grammaire[1]
    regles=grammaire[2]
    for regle in regles: #(s,[les regles])
        liste_regle = regle[1] #les regles list de list
        for une_regle in liste_regle: #une regle du type ["a","A1","A1"] pour désigner -> aA1A1
            if(len(une_regle)==1): #pour pas avoir de probleme avec l'epsilon transition.
                continue
            if(qu_une_variable(variables,une_regle)==False): #on a plusieurs variables du types aaBaaC donc c'est déjà faux.
                return False
            if(une_regle[0] not in variables and que_des_lettres_de_alphabet(alphabet,une_regle)==False):# Ce n'est pas que des lettres de l'alphabet du type aaa et la premier élement n'est pas une variable du type aAa ou abA c'est donc faux.
                return False #déjà on a un problèmes
            #l'on continue tout est bon
    return True
    
def est_regu(grammaire):
    if(est_regu_droite(grammaire)==True):
        print("G est regu droite ! \n")
    if(est_regu_gauche(grammaire)==True):
        print("G est regu gauche ! \n")
    return
#------------------------#
print("Jeux de tests:\n")
est_regu(g1_g)
est_regu(g2)
est_regu(g3)
est_regu(g4)
#Résultat attendu : Rien \ regu droite \regu gauche \ Rien !
