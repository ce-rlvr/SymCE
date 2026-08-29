import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, free_group
from sympy.matrices import eye, zeros

# Top-level setup
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

F2 = free_group('x, y')[0]
F3 = free_group('x, y, z')[0]

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, N, M) where F is a free group, and N, M 
    are lists of generators for the normal subgroups.
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, N, M = witness
    except Exception:
        return [False, False, False]

    # H1: F is a free group
    try:
        h1_ok = type(F).__name__ == 'FreeGroup'
    except Exception:
        h1_ok = False

    # H2: The rank of F is strictly greater than 1
    try:
        rank = getattr(F, 'rank', len(getattr(F, 'generators', [])))
        h2_ok = rank > 1
    except Exception:
        h2_ok = False

    # neg_Q: The intersection N \cap M is trivial
    # In a free group, the intersection of two normal subgroups is trivial 
    # if and only if at least one of the normal subgroups is trivial.
    try:
        def is_trivial(gens):
            if hasattr(gens, 'is_identity'):
                return gens.is_identity
            if not gens:
                return True
            
            try:
                iterator = iter(gens)
            except TypeError:
                iterator = [gens]
                
            for g in iterator:
                if hasattr(g, 'is_identity'):
                    if not g.is_identity:
                        return False
                elif hasattr(F, 'identity') and g != F.identity:
                    return False
                elif g != 1:
                    return False
            return True

        neg_q_ok = is_trivial(N) or is_trivial(M)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "H_2: The rank of F is strictly greater than 1",
    "¬Q: The intersection N \\cap M is trivial"
]

N_HYP = 2
NEG_Q_INDEX = 2