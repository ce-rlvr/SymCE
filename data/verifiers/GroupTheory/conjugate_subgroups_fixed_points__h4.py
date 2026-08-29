import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
from sympy.matrices import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Unpack witness
        if isinstance(witness, tuple):
            if len(witness) == 5:
                G, X, action, H, g = witness
            elif len(witness) == 4:
                G, X, H, g = witness
                action = lambda p, x: p(x)
            elif len(witness) == 3:
                G, H, g = witness
                X = list(range(G.degree))
                action = lambda p, x: p(x)
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        # H1: G is a group acting on a set X
        h1 = hasattr(G, 'is_group') and G.is_group and isinstance(X, (list, set, tuple))
        
        # H2: H is a subgroup of G
        h2 = hasattr(H, 'is_subgroup') and H.is_subgroup(G)
        
        # H3: g is an element of G
        h3 = g in G
        
        # Conclusion: X^H and X^{gHg^{-1}} have the same cardinality
        h_gens = H.generators if hasattr(H, 'generators') else H.elements
        
        X_H = []
        for x in X:
            if all(action(h, x) == x for h in h_gens):
                X_H.append(x)
                
        try:
            g_inv = g**-1
        except Exception:
            g_inv = ~g
            
        K_gens = [g * h * g_inv for h in h_gens]
        
        X_K = []
        for x in X:
            if all(action(k, x) == x for k in K_gens):
                X_K.append(x)
                
        neg_q = len(X_H) != len(X_K)
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X",
    "H_2: H is a subgroup of G",
    "H_3: g is an element of G",
    "¬Q: X^H and X^{gHg^{-1}} do not have the same cardinality"
]

N_HYP = 3
NEG_Q_INDEX = 3