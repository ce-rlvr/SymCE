import sympy
from sympy import Symbol, Poly, factor_list
from sympy.polys.rootoftools import RootOf
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
x = Symbol('x')

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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If L/K is a field extension, then L is a normal extension of K."
    
    The witness is expected to be an irreducible polynomial over Q, 
    representing the field extension Q(alpha)/Q where alpha is a root.
    """
    try:
        # Determine the variable used in the witness polynomial
        if hasattr(witness, 'free_symbols') and len(witness.free_symbols) == 1:
            var = list(witness.free_symbols)[0]
        else:
            var = x
            
        poly = Poly(witness, var, domain='QQ')
        # H_1: L/K is a field extension (witness must be an irreducible polynomial over Q)
        h1 = poly.is_irreducible and poly.degree() >= 1
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            # ¬Q: L is NOT a normal extension of K
            # An extension Q(alpha)/Q is normal iff the minimal polynomial splits 
            # completely into linear factors over Q(alpha).
            alpha = RootOf(witness, var, 0)
            factors = factor_list(witness, var, extension=alpha)
            
            all_linear = True
            for f, m in factors[1]:
                if Poly(f, var).degree() > 1:
                    all_linear = False
                    break
            
            neg_q = not all_linear
    except Exception:
        neg_q = False

    return [bool(h1), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "¬Q: L is not a normal extension of K"
]

N_HYP = 1
NEG_Q_INDEX = 1