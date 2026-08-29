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

def conditions(witness) -> list[bool]:
    try:
        if not isinstance(witness, tuple) or len(witness) != 4:
            return [False, False, False]
        G, x, y, g = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(x, (int, sympy.Integer)) and x >= 0 and 
              isinstance(y, (int, sympy.Integer)) and y >= 0 and 
              isinstance(g, Permutation) and 
              g in G)
    except Exception:
        h1 = False

    try:
        if h1:
            h2 = y in G.orbit(x)
        else:
            h2 = False
    except Exception:
        h2 = False

    try:
        if h1:
            stab_x = G.stabilizer(x)
            stab_y = G.stabilizer(y)
            
            if not stab_x.generators:
                conj_stab = PermutationGroup([g * ~g])
            else:
                conj_gens = [g * h * ~g for h in stab_x.generators]
                conj_stab = PermutationGroup(conj_gens)
            
            is_equal = stab_y.is_subgroup(conj_stab) and conj_stab.is_subgroup(stab_y)
            neg_q = not is_equal
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group acting on a set X, x and y are in X, and g is in G",
    "H_2: x and y are elements of X in the same orbit",
    "¬Q: Stab_G(y) is not equal to g * Stab_G(x) * g^{-1}"
]

N_HYP = 2
NEG_Q_INDEX = 2