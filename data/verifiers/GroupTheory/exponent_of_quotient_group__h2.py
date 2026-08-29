import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup, AbelianGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False, False]
        G, N = witness
    except Exception:
        return [False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: G has a finite exponent e
    try:
        # All PermutationGroups in sympy are finite, hence have a finite exponent
        h2 = isinstance(G, PermutationGroup)
    except Exception:
        h2 = False
        
    # neg_Q: The exponent of the quotient group G/N divides e
    # This conclusion fails if G/N is not a valid quotient group (i.e., N is not a normal subgroup)
    try:
        if not h1:
            neg_q = False
        else:
            if isinstance(N, list):
                try:
                    N = PermutationGroup(N)
                except Exception:
                    pass
            
            if not isinstance(N, PermutationGroup):
                neg_q = True
            elif not N.is_subgroup(G):
                neg_q = True
            else:
                is_norm = False
                try:
                    is_norm = N.is_normal(G)
                except AttributeError:
                    try:
                        is_norm = G.is_normal(N)
                    except AttributeError:
                        pass
                neg_q = not is_norm
    except Exception:
        neg_q = True
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: G has a finite exponent e",
    "¬Q: G/N is not a quotient group (N is not normal in G), or its exponent does not divide e"
]

N_HYP = 2
NEG_Q_INDEX = 2