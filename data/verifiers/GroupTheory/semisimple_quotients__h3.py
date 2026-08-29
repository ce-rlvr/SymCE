import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = hasattr(G, 'order') and G.order() < float('inf')
    except Exception:
        h1 = False
        
    # H2: G is isomorphic to a direct product of non-abelian simple groups
    try:
        if G.order() == 1:
            h2 = True
        else:
            D = G.derived_subgroup()
            Z = G.center()
            h2 = (D.order() == G.order()) and (Z.order() == 1)
    except Exception:
        h2 = False

    # neg_Q: The quotient group G/N is either the trivial group or isomorphic to a direct product of non-abelian simple groups.
    # The conclusion fails (neg_Q is True) if N is not a normal subgroup of G, as G/N would not be a group.
    try:
        if not hasattr(N, 'generators'):
            neg_q = True
        else:
            is_sub = True
            if hasattr(N, 'is_subgroup'):
                is_sub = N.is_subgroup(G)
            else:
                for gen in N.generators:
                    if gen not in G:
                        is_sub = False
                        break
            
            if not is_sub:
                neg_q = True
            else:
                is_norm = True
                if hasattr(G, 'is_normal'):
                    is_norm = G.is_normal(N)
                else:
                    for g in G.generators:
                        g_inv = g**-1
                        for n in N.generators:
                            if (g * n * g_inv) not in N and (g_inv * n * g) not in N:
                                is_norm = False
                                break
                        if not is_norm:
                            break
                
                if not is_norm:
                    neg_q = True
                else:
                    # If N is normal, G/N is a group. Since G is a direct product of non-abelian simple groups,
                    # G/N is also a direct product of non-abelian simple groups (or trivial).
                    # Thus the conclusion holds, meaning neg_q is False.
                    neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is isomorphic to a direct product of non-abelian simple groups",
    "¬Q: The quotient group G/N is neither the trivial group nor isomorphic to a direct product of non-abelian simple groups"
]

N_HYP = 2
NEG_Q_INDEX = 2