import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def check_H1(witness):
    try:
        G, P_or_p = witness
        if hasattr(P_or_p, 'generators'):
            P = P_or_p
            for gen in P.generators:
                if gen not in G.elements:
                    return False
            order_P = P.order()
            factors = sympy.ntheory.factorint(order_P)
            if len(factors) != 1: 
                return False
            p = list(factors.keys())[0]
            if (G.order() // order_P) % p == 0: 
                return False
            return True
        else:
            p = P_or_p
            if not sympy.ntheory.isprime(p): 
                return False
            if G.order() % p != 0: 
                return False
            return True
    except Exception:
        return False

def check_H2(witness):
    return check_H1(witness)

def check_neg_Q(witness):
    try:
        G, P_or_p = witness
        if hasattr(P_or_p, 'generators'):
            P = P_or_p
        else:
            p = P_or_p
            P = G.sylow_subgroup(p)
            
        commutators = []
        P_elems = list(P.elements)
        for h1 in P_elems:
            for h2 in P_elems:
                c = h1 * h2 * (h1**-1) * (h2**-1)
                commutators.append(c)
                
        P_prime = PermutationGroup(*commutators)
        P_prime_elems = set(P_prime.elements)
        
        reps = []
        seen = set()
        G_elems = list(G.elements)
        
        for g in G_elems:
            if g not in seen:
                reps.append(g)
                for h in P_elems:
                    seen.add(h * g)
                    
        element_to_rep = {}
        for r in reps:
            for h in P_elems:
                element_to_rep[h * r] = r
                
        id_elem = G_elems[0]**-1 * G_elems[0]
        
        for g in G_elems:
            v_g = id_elem
            for r in reps:
                rg = r * g
                r_prime = element_to_rep[rg]
                h = rg * (r_prime**-1)
                v_g = v_g * h
            
            if v_g not in P_prime_elems:
                return True
                
        return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    return [check_H1(witness), check_H2(witness), check_neg_Q(witness)]

CONDITION_LABELS = [
    "H_1: P is a Sylow p-subgroup of G",
    "H_2: V is the transfer homomorphism from G to P mod commutator of P",
    "not_Q: The image of V is not the trivial subgroup"
]

N_HYP = 2
NEG_Q_INDEX = 2