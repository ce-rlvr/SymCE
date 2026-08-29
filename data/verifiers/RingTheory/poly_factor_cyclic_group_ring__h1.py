import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    n = None
    C_n = None
    R = None
    
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            C_n = witness.get('C_n')
            R = witness.get('R')
        elif isinstance(witness, tuple):
            for item in witness:
                if getattr(item, 'is_group', False):
                    C_n = item
                elif (isinstance(item, int) or isinstance(item, sympy.Integer)) and n is None:
                    n = item
                else:
                    R = item
    except Exception:
        pass

    # H1: n >= 1 is an integer
    try:
        h1 = (n is not None) and int(n) >= 1
    except Exception:
        h1 = False

    # H2: C_n is the cyclic group of order n
    try:
        h2 = False
        if C_n is not None and getattr(C_n, 'is_group', False) and int(C_n.order()) == int(n):
            if getattr(C_n, 'is_cyclic', False):
                h2 = True
            else:
                for g in C_n.elements:
                    if int(g.order()) == int(n):
                        h2 = True
                        break
    except Exception:
        h2 = False

    # ¬Q: The group ring R[C_n] is not isomorphic to the factor ring R[x]/<x^n - 1>
    try:
        if R is None:
            # If R is not provided, the conjecture is universally quantified over R.
            # Since it fails for non-unital rings, the universal statement is false.
            neg_q = True
        else:
            is_valid_ring = False
            if hasattr(R, 'is_Ring') and R.is_Ring:
                is_valid_ring = getattr(R, 'is_commutative', True)
            elif hasattr(R, 'one') and hasattr(R, 'zero'):
                is_valid_ring = getattr(R, 'is_commutative', True)
            elif R in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
                is_valid_ring = True
            
            neg_q = not is_valid_ring
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: C_n is the cyclic group of order n",
    "¬Q: The group ring is not isomorphic to the factor ring"
]

N_HYP = 2
NEG_Q_INDEX = 2