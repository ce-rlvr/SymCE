import sympy
from sympy import Matrix, eye, zeros, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    x_sym = sympy.Symbol('x')
    
    # H1: K is a field
    try:
        h1 = isinstance(witness, sympy.MatrixBase)
        if h1:
            for elem in witness:
                # Check for non-commutative elements
                if not getattr(elem, 'is_commutative', True):
                    h1 = False
                    break
                # If elements are modulo arithmetic, the modulus must be prime for it to be a field
                if isinstance(elem, sympy.Mod):
                    if not sympy.isprime(elem.args[1]):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: A is an n x n matrix over K
    try:
        h2 = isinstance(witness, sympy.MatrixBase) and witness.is_square
    except Exception:
        h2 = False

    # H3: A is a nilpotent matrix
    try:
        h3 = bool(witness.is_nilpotent())
    except Exception:
        h3 = False

    # neg_Q: The characteristic polynomial of A is not x^n
    try:
        n = witness.shape[0]
        cp = witness.charpoly(x_sym).as_expr()
        diff = sympy.expand(cp - x_sym**n)
        neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: A is an n x n matrix over K",
    "H_3: A is a nilpotent matrix",
    "¬Q: The characteristic polynomial of A is not x^n"
]

N_HYP = 3
NEG_Q_INDEX = 3