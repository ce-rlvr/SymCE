import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, free_group
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
        if len(witness) == 3:
            F, g, N = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: F is a free group of rank at least 2
    try:
        h1 = (type(F).__name__ == 'FreeGroup' and 
              hasattr(F, 'rank') and F.rank >= 2)
    except Exception:
        h1 = False
        
    # H2: N is the normal closure of g in F
    # For a free group of rank >= 2, the normal closure of an element g 
    # is finitely generated if and only if g is the identity (so N is trivial).
    # Since the witness must provide a finitely generated N (to satisfy neg_Q),
    # N can only be the normal closure of g if g is the identity and N generates the trivial group.
    try:
        if h1 and getattr(g, 'group', None) == F:
            if g == F.identity:
                if isinstance(N, (list, tuple, set)):
                    h2 = all(getattr(x, 'group', None) == F and x == F.identity for x in N)
                else:
                    h2 = False
            else:
                # If g != identity, its normal closure is not finitely generated,
                # so a finite list N cannot equal the normal closure.
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # neg_Q: N is finitely generated
    # Represented by N being a finite collection of generators
    try:
        neg_q = isinstance(N, (list, tuple, set))
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group of rank at least 2",
    "H_2: N is the normal closure of g in F",
    "¬Q: N is finitely generated"
]

N_HYP = 2
NEG_Q_INDEX = 2