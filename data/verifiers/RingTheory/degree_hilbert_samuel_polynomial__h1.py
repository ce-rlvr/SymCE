import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import n

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
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    "The degree of the Hilbert-Samuel polynomial P_I(n) is exactly d."
    
    The witness is expected to be a dictionary with keys 'd', 'I', 'P_I'
    or a tuple (d, I, P_I).
    """
    # H_1: d is the Krull dimension of R
    try:
        if isinstance(witness, dict):
            d = witness['d']
        else:
            d = witness[0]
        h1 = (isinstance(d, (int, sp.Integer)) and d >= 0) or d == sp.oo
    except Exception:
        h1 = False

    # H_2: I is an \mathfrak{m}-primary ideal of R
    try:
        if isinstance(witness, dict):
            I = witness['I']
        else:
            I = witness[1]
        h2 = I is not None
    except Exception:
        h2 = False

    # H_3: P_I(n) is the Hilbert-Samuel polynomial associated to the I-adic filtration of R
    try:
        if isinstance(witness, dict):
            P_I = witness['P_I']
        else:
            P_I = witness[2]
        P_I_expr = sp.sympify(P_I)
        if not P_I_expr.free_symbols.issubset({n}):
            h3 = False
        else:
            # Verify it is a valid polynomial in n
            sp.Poly(P_I_expr, n)
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: The degree of the polynomial P_I(n) is not exactly d
    try:
        if isinstance(witness, dict):
            d = witness['d']
            P_I = witness['P_I']
        else:
            d = witness[0]
            P_I = witness[2]
        P_I_expr = sp.sympify(P_I)
        
        if P_I_expr == 0:
            deg = -sp.oo
        else:
            deg = sp.degree(P_I_expr, n)
            
        neg_q = bool(deg != d)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: d is the Krull dimension of R",
    "H_2: I is an m-primary ideal of R",
    "H_3: P_I(n) is the Hilbert-Samuel polynomial associated to the I-adic filtration of R",
    "¬Q: The degree of the polynomial P_I(n) is not exactly d"
]

N_HYP = 3
NEG_Q_INDEX = 3