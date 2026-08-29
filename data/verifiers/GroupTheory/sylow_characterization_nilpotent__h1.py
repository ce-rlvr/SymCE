import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G = witness
        
        # Evaluate LHS: G is nilpotent
        if callable(getattr(G, 'is_nilpotent', None)):
            lhs = bool(G.is_nilpotent())
        else:
            lhs = bool(G.is_nilpotent)
            
        # Evaluate RHS: for every prime p dividing |G|, the Sylow p-subgroup is normal
        if callable(getattr(G, 'order', None)):
            order = G.order()
        else:
            order = G.order
            
        if order == sympy.oo or order == math.inf:
            primes = []
        else:
            from sympy.ntheory import factorint
            primes = list(factorint(order).keys())
            
        rhs = True
        for p in primes:
            P = G.sylow_subgroup(p)
            is_norm = True
            for g in G.generators:
                for h in P.generators:
                    element = g * h * g**-1
                    if hasattr(P, 'contains'):
                        in_P = P.contains(element)
                    else:
                        in_P = element in P
                    
                    if not in_P:
                        is_norm = False
                        break
                if not is_norm:
                    break
            
            if not is_norm:
                rhs = False
                break
                
        # The conclusion is LHS <-> RHS. We want the negation of the conclusion.
        neg_q = not (lhs == rhs)
        
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: G is nilpotent is not equivalent to all its Sylow p-subgroups being normal"
]

N_HYP = 0
NEG_Q_INDEX = 0