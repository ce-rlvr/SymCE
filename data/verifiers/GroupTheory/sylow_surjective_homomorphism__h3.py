import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation
from sympy import isprime
import math
import itertools
import functools

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # H1: G and H are finite groups
    try:
        G = witness['G']
        H = witness['H']
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: phi is a surjective group homomorphism
    try:
        G = witness['G']
        H = witness['H']
        phi = witness['phi']
        
        G_elements = list(G.elements)
        H_elements = list(H.elements)
        
        if callable(phi):
            phi_dict = {g: phi(g) for g in G_elements}
        else:
            phi_dict = phi
            
        if not all(g in phi_dict for g in G_elements):
            h2 = False
        elif not all(phi_dict[g] in H_elements for g in G_elements):
            h2 = False
        else:
            is_hom = True
            for g1 in G_elements:
                for g2 in G_elements:
                    if phi_dict[g1 * g2] != phi_dict[g1] * phi_dict[g2]:
                        is_hom = False
                        break
                if not is_hom:
                    break
            
            if is_hom:
                image = set(phi_dict[g] for g in G_elements)
                h2 = (len(image) == len(H_elements))
            else:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: phi(P) is NOT a Sylow p-subgroup of H
    try:
        H = witness['H']
        phi = witness['phi']
        P = witness['P']
        p = witness['p']
        
        if hasattr(P, 'elements'):
            P_elements = list(P.elements)
        else:
            P_elements = list(P)
            
        if callable(phi):
            phi_P = set(phi(x) for x in P_elements)
        else:
            phi_P = set(phi[x] for x in P_elements)
            
        def is_sylow(subset, grp, prime):
            if not isprime(prime):
                return False
            if not subset:
                return False
            if grp.identity not in subset:
                return False
            for a in subset:
                for b in subset:
                    if a * b not in subset:
                        return False
            order = grp.order()
            k = 0
            if order > 0:
                while order % (prime ** (k + 1)) == 0:
                    k += 1
            return len(subset) == (prime ** k)

        neg_q = not is_sylow(phi_P, H, p)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are finite groups",
    "H_2: phi is a surjective group homomorphism from G to H",
    "¬Q: phi(P) is not a Sylow p-subgroup of H"
]

N_HYP = 2
NEG_Q_INDEX = 2