import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

Z = sympy.S.Integers

try:
    from sympy.combinatorics.free_groups import free_group
    F, (a,) = free_group("a")
except ImportError:
    pass

CONDITION_LABELS = [
    "H_1: G is a torsion-free nilpotent group",
    "H_2: x and y are elements of G",
    "¬Q: x != y"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        G, x, y = witness
    except Exception:
        return [False, False, False]
    
    # H_1: G is a torsion-free nilpotent group
    h1 = False
    try:
        if G in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h1 = True
        elif G == "HeisenbergGroup":
            h1 = True
        elif hasattr(G, 'is_nilpotent') and callable(G.is_nilpotent):
            if G.is_nilpotent() and G.order() == 1:
                h1 = True
        else:
            try:
                from sympy.combinatorics.free_groups import FreeGroup
                if isinstance(G, FreeGroup) and len(G.generators) == 1:
                    h1 = True
            except ImportError:
                pass
    except Exception:
        h1 = False

    # H_2: x and y are elements of G
    h2 = False
    try:
        if G in (sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes):
            h2 = bool(G.contains(x) and G.contains(y))
        elif G == "HeisenbergGroup":
            from sympy.matrices import Matrix
            def is_H(M):
                if not isinstance(M, Matrix) or M.shape != (3, 3): 
                    return False
                if list(M.diagonal()) != [1, 1, 1]: 
                    return False
                if M[1, 0] != 0 or M[2, 0] != 0 or M[2, 1] != 0: 
                    return False
                return all(sympy.S.Integers.contains(M[i, j]) for i, j in [(0, 1), (0, 2), (1, 2)])
            h2 = bool(is_H(x) and is_H(y))
        else:
            h2 = bool(x in G and y in G)
    except Exception:
        h2 = False

    # neg_Q: x != y
    neg_q = False
    try:
        neg_q = bool(x != y)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]