import sympy
from sympy import Matrix, symbols

S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        R, n = witness
    except Exception:
        return [False, False, False, False]

    try:
        h1_ok = hasattr(R, 'is_UFD') and bool(R.is_UFD)
    except Exception:
        h1_ok = False

    try:
        h2_ok = isinstance(n, int) and n >= 2
    except Exception:
        h2_ok = False

    try:
        h3_ok = h2_ok
    except Exception:
        h3_ok = False

    try:
        if h2_ok and h3_ok:
            X = symbols(f'X1:{n+1}1:{n+1}')
            M = Matrix(n, n, X)
            det_poly = M.det()
            coeff, factors = sympy.factor_list(det_poly, domain=R)
            # Since det(M) is primitive (coefficients are +/- 1), 
            # it is irreducible iff there is exactly one factor with multiplicity 1.
            is_irred = (len(factors) == 1 and factors[0][1] == 1)
            neg_q_ok = not is_irred
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: n is an integer such that n >= 2",
    "H_3: X_ij are algebraically independent variables over R",
    "¬Q: The determinant polynomial det(M) is reducible"
]

N_HYP = 3
NEG_Q_INDEX = 3