import sympy
from sympy import cyclotomic_poly
from sympy.abc import x
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup for standard algebra objects
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
    Checks whether the given witness satisfies the remaining hypotheses
    and falsifies the conclusion of the conjecture.
    """
    # Check H_1: n > 1 is an odd integer
    try:
        if isinstance(witness, str):
            val = sympy.sympify(witness)
        else:
            val = witness
            
        if hasattr(val, 'is_integer') and val.is_integer:
            n = int(val)
            h1_ok = (n > 1) and (n % 2 == 1)
        elif isinstance(val, int):
            n = val
            h1_ok = (n > 1) and (n % 2 == 1)
        else:
            n_float = float(val)
            n = int(n_float)
            h1_ok = (n == n_float) and (n > 1) and (n % 2 == 1)
    except Exception:
        h1_ok = False

    # Check ¬Q: \Phi_{2n}(x) != \Phi_n(-x)
    try:
        if isinstance(witness, str):
            val = sympy.sympify(witness)
        else:
            val = witness
            
        n = int(val)
        poly_2n = cyclotomic_poly(2 * n, x)
        poly_n_neg = cyclotomic_poly(n, -x)
        
        # The conclusion fails if the polynomials are not equal
        neg_q_ok = bool(sympy.expand(poly_2n - poly_n_neg) != 0)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n > 1 is an odd integer",
    "¬Q: \\Phi_{2n}(x) != \\Phi_n(-x)"
]

N_HYP = 1
NEG_Q_INDEX = 1