import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup
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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: N is a normal subgroup of G",
    "H_2: The quotient group G/N is a free group",
    "¬Q: G is not isomorphic to the semidirect product N \\rtimes (G/N) or the sequence does not split"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # Dictionary witness
        if isinstance(witness, dict):
            h1 = bool(witness.get('H1', witness.get('is_normal_subgroup', False)))
            h2 = bool(witness.get('H2', witness.get('quotient_is_free', False)))
            neg_q = bool(witness.get('neg_Q', witness.get('neg_q', False)))
            return [h1, h2, neg_q]
            
        # Object with properties/methods
        if hasattr(witness, 'H1'):
            h1 = bool(witness.H1() if callable(witness.H1) else witness.H1)
        elif hasattr(witness, 'is_normal_subgroup'):
            h1 = bool(witness.is_normal_subgroup() if callable(witness.is_normal_subgroup) else witness.is_normal_subgroup)
            
        if hasattr(witness, 'H2'):
            h2 = bool(witness.H2() if callable(witness.H2) else witness.H2)
        elif hasattr(witness, 'quotient_is_free'):
            h2 = bool(witness.quotient_is_free() if callable(witness.quotient_is_free) else witness.quotient_is_free)
            
        if hasattr(witness, 'neg_Q'):
            neg_q = bool(witness.neg_Q() if callable(witness.neg_Q) else witness.neg_Q)
        elif hasattr(witness, 'neg_q'):
            neg_q = bool(witness.neg_q() if callable(witness.neg_q) else witness.neg_q)
        elif hasattr(witness, 'splits') and hasattr(witness, 'is_semidirect_product'):
            splits = bool(witness.splits() if callable(witness.splits) else witness.splits)
            is_semi = bool(witness.is_semidirect_product() if callable(witness.is_semidirect_product) else witness.is_semidirect_product)
            neg_q = not (splits and is_semi)
            
        # Tuple witness (G, N)
        if isinstance(witness, tuple) and len(witness) == 2:
            G, N = witness
            
            # Check H1
            if not h1:
                try:
                    if hasattr(N, 'is_normal'):
                        h1 = bool(N.is_normal(G))
                    elif hasattr(G, 'is_normal'):
                        h1 = bool(G.is_normal(N))
                except Exception:
                    pass
                    
            # Check H2 and neg_Q
            if not h2:
                try:
                    if hasattr(G, 'order') and hasattr(N, 'order'):
                        oG = G.order()
                        oN = N.order()
                        if oG != sympy.oo and oN != sympy.oo:
                            # For finite groups, G/N is free iff it is trivial (order 1)
                            if oG == oN:
                                h2 = True
                                if not hasattr(witness, 'neg_Q') and not hasattr(witness, 'neg_q'):
                                    # If G/N is trivial, G is isomorphic to N \rtimes 1, sequence splits
                                    neg_q = False
                            else:
                                h2 = False
                except Exception:
                    pass
                    
    except Exception:
        pass
        
    return [h1, h2, neg_q]