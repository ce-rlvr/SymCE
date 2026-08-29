import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "H is contained in the normalizer N_G(K) if and only if commutator(H, K) subset K."
    """
    try:
        G, K, H = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a group
    try:
        h1 = hasattr(G, 'generators') and (hasattr(G, 'contains') or hasattr(G, '__contains__'))
    except Exception:
        h1 = False
        
    # H_2: K is a subgroup of G
    try:
        h2 = False
        if hasattr(K, 'is_subgroup'):
            try:
                h2 = K.is_subgroup(G)
            except Exception:
                pass
        if not h2 and hasattr(K, 'generators'):
            in_G = True
            for g in K.generators:
                if hasattr(G, 'contains'):
                    if not G.contains(g):
                        in_G = False
                        break
                else:
                    if g not in G:
                        in_G = False
                        break
            if in_G:
                h2 = True
    except Exception:
        h2 = False

    # ¬Q: The conclusion fails
    try:
        A = True
        B = True
        
        try:
            iter(H)
            H_iter = H
        except TypeError:
            H_iter = [H]
            
        def in_K(x):
            if hasattr(K, 'contains'):
                return K.contains(x)
            return x in K

        if hasattr(K, 'generators'):
            K_gens = K.generators
        else:
            K_gens = K

        for h in H_iter:
            h_in_N = True
            h_comm_in_K = True
            
            for g in K_gens:
                if not in_K(h * g * (h**-1)):
                    h_comm_in_K = False
                    h_in_N = False
                    break
            
            if h_comm_in_K:
                for g in K_gens:
                    if not in_K((h**-1) * g * h):
                        h_in_N = False
                        break
                        
            if not h_in_N:
                A = False
            if not h_comm_in_K:
                B = False
                
        neg_q = (A != B)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: K is a subgroup of G",
    "¬Q: H is contained in N_G(K) iff commutator(H, K) subset K fails"
]

N_HYP = 2
NEG_Q_INDEX = 2