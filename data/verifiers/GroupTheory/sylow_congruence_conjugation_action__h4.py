import sympy
from sympy.combinatorics import Permutation, PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import isprime
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture.
    Witness is expected to be a tuple: (G, p, P, S)
    """
    try:
        if len(witness) != 4:
            return [False] * 4 + [False]
        G, p, P, S = witness
    except Exception:
        return [False] * 4 + [False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False
        
    # H2: p is a prime dividing the order of G
    try:
        h2 = isprime(p) and G.order() % p == 0
    except Exception:
        h2 = False
        
    # H3: P is a Sylow p-subgroup of G
    try:
        def is_subgroup(H, G_grp):
            if hasattr(H, 'is_subgroup'):
                return H.is_subgroup(G_grp)
            return all(g in G_grp for g in H.generators)
            
        if isinstance(P, PermutationGroup) and is_subgroup(P, G):
            order_G = G.order()
            order_P = P.order()
            k = 0
            temp = order_G
            while temp % p == 0:
                k += 1
                temp //= p
            h3 = (order_P == p**k)
        else:
            h3 = False
    except Exception:
        h3 = False
        
    # H4: P acts on S by conjugation
    try:
        def acts_by_conjugation(P_grp, S_col):
            if not isinstance(S_col, (list, tuple, set, frozenset)):
                return False
            if len(S_col) == 0:
                return True
                
            gens = P_grp.generators
            S_list = list(S_col)
            
            # Case 1: S is a collection of Permutations
            if all(isinstance(s, Permutation) for s in S_list):
                S_set = set(S_list)
                for g in gens:
                    for s in S_set:
                        if g * s * ~g not in S_set:
                            return False
                return True
                
            # Case 2: S is a collection of PermutationGroups
            if all(isinstance(s, PermutationGroup) for s in S_list):
                S_elements = [set(s.elements) for s in S_list]
                for g in gens:
                    for s_elems in S_elements:
                        conj_elems = set(g * x * ~g for x in s_elems)
                        if conj_elems not in S_elements:
                            return False
                return True
                
            # Case 3: S is a collection of sets/lists of Permutations
            if all(isinstance(s, (set, frozenset, list, tuple)) for s in S_list):
                S_sets = [set(s) for s in S_list]
                for g in gens:
                    for s_set in S_sets:
                        conj_set = set(g * x * ~g for x in s_set)
                        if conj_set not in S_sets:
                            return False
                return True
                
            return False
            
        h4 = acts_by_conjugation(P, S)
    except Exception:
        h4 = False
        
    # neg_Q: The number of Sylow p-subgroups of G (the cardinality of S) is NOT congruent to 1 modulo p
    try:
        neg_q = (len(S) % p != 1)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: p is a prime dividing the order of G",
    "H_3: P is a Sylow p-subgroup of G",
    "H_4: P acts on S by conjugation",
    "¬Q: The cardinality of S is not congruent to 1 modulo p"
]

N_HYP = 4
NEG_Q_INDEX = 4