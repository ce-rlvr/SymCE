import sympy
from sympy.combinatorics import free_group
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (F, g, N) where:
      - F is a FreeGroup
      - g is an element of F
      - N is the normal closure of g in F
    """
    try:
        if len(witness) != 3:
            return [False, False, False]
        F, g, N = witness
    except Exception:
        return [False, False, False]
    
    # H_1: g is a non-identity element of F
    try:
        h1_ok = type(F).__name__ == 'FreeGroup' and hasattr(F, 'identity') and (g in F) and (g != F.identity)
    except Exception:
        h1_ok = False
        
    # H_2: N is the normal closure of g in F
    # In SymPy, proper subgroups of FreeGroups are not natively represented.
    # However, for a free group of rank 1, the normal closure of a generator is the group itself.
    # We verify if N is exactly F and if g normally generates F.
    try:
        h2_ok = False
        if type(F).__name__ == 'FreeGroup' and N == F and hasattr(F, 'rank') and F.rank == 1:
            gens = list(F.generators)
            # In a rank 1 free group, only the generators normally generate the whole group
            if g == gens[0] or g == gens[0]**-1:
                h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: N is finitely generated (Conclusion was: N is not finitely generated)
    # A FreeGroup of rank 1 is finitely generated.
    try:
        neg_q_ok = False
        if type(N).__name__ == 'FreeGroup' and hasattr(N, 'rank') and N.rank == 1:
            neg_q_ok = True
    except Exception:
        neg_q_ok = False
        
    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: g is a non-identity element of F",
    "H_2: N is the normal closure of g in F",
    "¬Q: N is finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2