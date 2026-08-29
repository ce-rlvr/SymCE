import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample.
    The witness should be a tuple: (G, p, S_list)
    where G is a PermutationGroup, p is a prime, and S_list is a list/tuple of PermutationGroups.
    """
    try:
        G, p, S_list = witness
    except Exception:
        return [False, False, False]
    
    # H_1: p is a prime dividing the order of G
    try:
        h1 = sympy.isprime(p) and (G.order() % p == 0)
    except Exception:
        h1 = False
        
    # H_2: n_p(X) denotes the number of Sylow p-subgroups of a finite group X
    # We verify that G and all elements in S_list are valid finite groups.
    try:
        h2 = (isinstance(G, PermutationGroup) and 
              isinstance(S_list, (list, tuple)) and 
              all(isinstance(S, PermutationGroup) for S in S_list))
    except Exception:
        h2 = False
        
    # ¬Q: The number of Sylow p-subgroups of G is NOT given by the product of n_p(S_i)
    try:
        def sylow_p_count(grp, prime):
            if grp.order() % prime != 0:
                return 1
            P = grp.sylow_subgroup(prime)
            P_elements = list(P.generate())
            conjugates = set()
            for g in grp.generate():
                # Conjugate the elements of the Sylow subgroup by g
                conj = frozenset([~g * x * g for x in P_elements])
                conjugates.add(conj)
            return len(conjugates)
        
        np_G = sylow_p_count(G, p)
        
        np_S = 1
        for S in S_list:
            np_S *= sylow_p_count(S, p)
            
        neg_q = (np_G != np_S)
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: p is a prime dividing the order of G",
    "H_2: n_p(X) denotes the number of Sylow p-subgroups of a finite group X",
    "¬Q: n_p(G) != prod_{i=1}^k n_p(S_i)"
]

N_HYP = 2
NEG_Q_INDEX = 2