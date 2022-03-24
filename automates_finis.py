# UE Calculabilite
#====================

from copy import deepcopy
from ensembles import *





# Quelques fonctions sur les automates finis
#-------------------------------------------

# Liste des transitions de T dont l'origine est l'etat s

def lt_from_s(eq,s,T):
    return [(s1,l,s2) for (s1,l,s2) in T if eq(s1,s)]

# >>> lt_from_s(eq_atom,3,ex_T)
# [(3, 'a', 1), (3, 'b', 1), (3, None, 2)]

# Epsilon-fermeture d'un etat
def add_state_list(liste,l2):
	for k in l2:
		if k not in liste:
			liste.append(k)
	return liste
def state_access_epsilon(eq,s,T):
	liste=lt_from_s(eq,s,T)
	l1=[]
	for (s1,l,s2) in liste:
		if l==None:
			l1.append(s2)
	return l1



def eps_cl(eq,s,T):
    # A COMPLETER 
    done=[]
    to_do=[s]
    visite={}

    while len(to_do)!=0:
    	add_state_list(done,to_do)
    	for p in to_do:
    		visite[p]=True
    		tmp=state_access_epsilon(eq,p,T)
    		to_do=to_do+tmp
    		list(set(to_do))
    	for j in visite:
    		if visite[j]==True and j in to_do:
    			to_do.remove(j)
    return done


    	
#print(eps_cl(eq_atom,0,ex_T))
#[2, 3, 0]
#print(eps_cl(eq_atom,1,ex_T))
# [1]
#print(eps_cl(eq_atom,4,ex_T))
# [2, 3, 0, 4]

# Epsilon-fermeture d'un ensemble d'etats

def eps_cl_set(eq,S,T):
    R=[]
    for s in S:
        R=union(eq,eps_cl(eq,s,T),R)
    return R

# >>> eps_cl_set(eq_atom,[0,1],ex_T)
# [1, 0, 3, 2]

# Liste des labels presents sur les transitions issues d'un etat s

def label_from(eq,s,T):
    R = []
    for (si,l,sf) in T:
        if eq(si,s) and l != None:
            R = ajout(eq_atom,l,R)
    return R

# >>> label_from(eq_atom,0,ex_T)
# []
# >>> label_from(eq_atom,3,ex_T)
# ['b', 'a']
# >>> label_from(eq_atom,4,ex_T)
# ['a']

# Liste des labels presents sur les transitions issues d'un ensemble d'etats

def label_from_set(eq,S,T):
    R = []
    for s in S:
        R = union(eq_atom,label_from(eq,s,T),R)
    return R

# >>> label_from_set(eq_atom,[0,4],ex_T)
# ['a']

# Liste des etats accessibles a partir d'un etat s et d'une lettre x

def reach_from(eq,s,x,T):
    s_sl = eps_cl(eq,s,T)
    trans_x = []
    for (s1,l,s2) in T:
        if l==x and is_in(eq,s1,s_sl):
            trans_x = ajout(eq,s2,trans_x)
    return eps_cl_set(eq,trans_x,T)
def reach_from_set(eq,S,x,T):
	l=[]
	for s in S:
		l=union(eq,reach_from(eq,s,x,T),l)
	return l

#print(reach_from_set(eq_atom, [2],'a',ex_T))
# [1, 4, 0, 3, 2]
# >>> reach_from(eq_atom,4,'a',ex_T)
# [1, 0, 3, 2]


# Acceptation d'un mot
#---------------------

def accept_word_finite_aut(eq,A,w):
    (S,T,I,F)=A
    def _aux(sa,wa):
        if wa==[]:
            return intersection(eq,eps_cl(eq,sa,T),F) !=[]
        else:
            trans = reach_from(eq,sa,wa[0],T)
            for st in trans:
                if _aux(st,wa[1:]):
                    return True
            return False
    for si in I:
        if _aux(si,w):
            return True
    return False



# >>> accept_word_finite_aut(eq_atom,ex_A,[])
# True
# >>> accept_word_finite_aut(eq_atom,ex_A,['a','b','b'])
# True
# >>> accept_word_finite_aut(eq_atom,ex_A,['a','a','b'])
# False


# Automates finis deterministes
#------------------------------

# determine si la relation de transition a partir d'un etat s est
# fonctionnelle et ne contient aucune epsilon-transition

def lt_from_s_deterministic(T):
    def _aux(L):
        if len(L)==0:
            return True
        else:
            if L[0] == None or L[0] in L[1:]:
                return False
            else:
                return _aux(L[1:])
    return _aux([l for (_,l,_) in T])

# >>> lt_from_s_deterministic(lt_from_s(eq_atom,3,ex_T))
# False
# >>> lt_from_s_deterministic([(3, 'a', 1), (3, 'b', 1)])
# True

# determine si un automate est deterministe

def is_deterministic(eq,A):
    (S,T,I,F) = A
    if len(I)>1:
        return False
    else:
        for s in S:
            if not lt_from_s_deterministic(lt_from_s(eq,s,T)):
                return False
        return True

# >>> is_deterministic(eq_atom,ex_A)
# False

# Determinisation
#----------------



# Egalite entre transitions d'un automate

def eq_trans(eq,t1,t2):
    (si1,l1,sf1) = t1
    (si2,l2,sf2) = t2
    return l1==l2 and eq(si1,si2) and eq(sf1,sf2)

def make_eq_trans(eq):
    def _eq_trans(t1,t2):
        return eq_trans(eq,t1,t2)
    return _eq_trans

# eq_set_atom = make_eq_set(eq_atom)
# >>> eq_trans_atom = make_eq_trans(eq_set_atom)
# >>> eq_trans_atom(([1,2,3],'a',[4,2]),([2,1,3],'a',[2,4]))
# True



# Determinisation d'un automate fini avec epsilon-transitions
def visite_bool(eq,save,access):
	for E in save:
		if eq_set(eq,E,access):
			return True
	return False



def make_det(eq,A):
	(S,T,I,F) = A
	save=[]
	SDET=[]
	TDET=[]
	FDET=[]
	init=sorted(eps_cl_set(eq,I,T))
	SDET.append(init)
	alph=label_from_set(eq,S,T)
	liste_wait=[init]
	while len(liste_wait)!=0:
		tmp=liste_wait[0]
		save.append(tmp)
		for x in alph:
			access=reach_from_set(eq,tmp,x,T)
			if eq_listState(access,SDET)==False and len(access)>0: 
				SDET.append(sorted(access))
			if len(access)>0:
				if (sorted(tmp),x,sorted(access)) not in TDET:
					TDET.append((sorted(tmp),x,sorted(access)))
			if visite_bool(eq,save,access)==False:
				liste_wait.append(access)
		liste_wait.remove(tmp)
	for s in SDET:
		if(len(intersection(eq,s,F))!=0):
			FDET.append(s)
	Adet=(SDET,TDET,init,sorted(FDET))

	return Adet

