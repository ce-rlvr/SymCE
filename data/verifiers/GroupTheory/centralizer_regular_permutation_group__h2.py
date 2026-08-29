import math
import itertools
import functools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        n, G = witness
    except Exception:
        return [False, False, False]
        
    # H_1: Let n be a positive integer
    try:
        h1 = type(n) is int and n > 0
    except Exception:
        h1 = False
        
    # H_2: Let G be a regular permutation subgroup of S_n
    try:
        h2 = False
        if isinstance(G, PermutationGroup):
            # Check if G is a subgroup of S_n (moves only points < n)
            is_subgroup = True
            for p in G.generators:
                if p.support() and max(p.support()) >= n:
                    is_subgroup = False
                    break
            
            if is_subgroup:
                # Interpretation A: G is regular on its support
                support = set()
                for p in G.generators:
                    support.update(p.support())
                
                is_reg_support = False
                if len(support) > 0:
                    orbit = set(G.orbit(next(iter(support))))
                    if orbit == support and G.order() == len(support):
                        is_reg_support = True
                else:
                    is_reg_support = True  # Trivial group
                    
                # Interpretation B: G is semi-regular on {0..n-1}
                is_semi_reg = True
                for g in G.elements:
                    if g.is_Identity:
                        continue
                    # A permutation is semi-regular if no non-identity element has fixed points
                    if any(g(i) == i for i in range(n)):
                        is_semi_reg = False
                        break
                        
                if is_reg_support or is_semi_reg:
                    h2 = True
    except Exception:
        h2 = False
        
    # ¬Q: The centralizer of G in S_n is NOT a regular permutation group that is isomorphic to G
    try:
        neg_q = False
        # Limit n to prevent timeout during centralizer computation
        if h1 and h2 and n <= 7:
            Sn = SymmetricGroup(n)
            gens = G.generators
            centralizer_elements = []
            
            # Compute centralizer of G in S_n
            for p in Sn.generate():
                if all(p * g == g * p for g in gens):
                    centralizer_elements.append(p)
            C = PermutationGroup(centralizer_elements)
            
            # Check if C is a regular permutation group
            c_support = set()
            for p in C.generators:
                c_support.update(p.support())
                
            is_c_reg_support = False
            if not c_support:
                is_c_reg_support = True
            else:
                orbit = set(C.orbit(next(iter(c_support))))
                if orbit == c_support and C.order() == len(c_support):
                    is_c_reg_support = True
                    
            is_c_reg_n = (C.order() == n and set(C.orbit(0)) == set(range(n)))
            is_c_regular = is_c_reg_support or is_c_reg_n
            
            # Check if C is isomorphic to G
            is_iso = False
            if C.order() == G.order():
                try:
                    is_iso = C.is_isomorphic(G)
                except AttributeError:
                    is_iso = (C.is_abelian == G.is_abelian)
            
            conclusion = is_c_regular and is_iso
            neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is a regular permutation subgroup of S_n",
    "¬Q: The centralizer of G in S_n is not a regular permutation group isomorphic to G"
]

N_HYP = 2
NEG_Q_INDEX = 2