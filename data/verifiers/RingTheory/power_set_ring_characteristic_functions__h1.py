import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        # Parse witness
        # The witness can provide both X and the Boolean ring of subsets P(X).
        # If only X is provided, P(X) is implicitly the full power set.
        if hasattr(witness, 'X') and hasattr(witness, 'P'):
            X = list(witness.X)
            P = [set(a) for a in witness.P]
        elif isinstance(witness, tuple) and len(witness) == 2:
            X = list(witness[0])
            P = [set(a) for a in witness[1]]
        elif isinstance(witness, list) and len(witness) > 0 and all(isinstance(x, (set, frozenset, list)) for x in witness):
            P = [set(a) for a in witness]
            X = list(set().union(*P))
        else:
            # Witness is just X. P is implicitly the full power set.
            # For the full power set, phi is always a ring isomorphism.
            # So neg_Q is False.
            X = list(witness)
            return [True, True, True, False]
            
        X_set = set(X)
        
        # H1: P(X) is a Boolean ring of subsets of X
        h1 = True
        for a in P:
            if not a.issubset(X_set):
                h1 = False
                break
                
        P_frozen = set(frozenset(a) for a in P)
        if h1:
            # Check closure under symmetric difference (addition) and intersection (multiplication)
            for a in P_frozen:
                for b in P_frozen:
                    if (a ^ b) not in P_frozen:
                        h1 = False
                        break
                    if (a & b) not in P_frozen:
                        h1 = False
                        break
                if not h1:
                    break
            # Must contain the empty set (additive identity)
            if frozenset() not in P_frozen:
                h1 = False
                
        # H2: F(X, Z_2) is the Boolean ring of functions from X to Z_2
        # This is a definitional hypothesis, always true for a valid set X.
        h2 = True
        
        # H3: phi maps P(X) to F(X, Z_2) via characteristic functions
        # This is a definitional hypothesis, always true.
        h3 = True
        
        # neg_Q: phi is NOT a ring isomorphism
        # Since phi is always an injective ring homomorphism, it is an isomorphism
        # if and only if it is surjective. It is surjective iff P(X) is the full power set.
        neg_q = len(P_frozen) != (1 << len(X_set))
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: P(X) is a Boolean ring of subsets of X with symmetric difference and intersection",
    "H_2: F(X, Z_2) is the Boolean ring of functions from X to Z_2",
    "H_3: phi maps P(X) to F(X, Z_2) via characteristic functions",
    "¬Q: phi is not a ring isomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3