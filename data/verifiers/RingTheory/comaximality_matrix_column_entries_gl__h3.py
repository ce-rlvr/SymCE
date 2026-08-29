import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix, eye, zeros, ZZ, QQ
import math
from functools import reduce

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
    try:
        if len(witness) == 4:
            R, n, j, A = witness
        elif len(witness) == 3:
            n, j, A = witness
            R = ZZ
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring
    try:
        h1 = hasattr(R, 'is_commutative') or R in [sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes, ZZ, QQ]
    except Exception:
        h1 = False

    # H2: n is an integer strictly greater than 1
    try:
        h2 = isinstance(n, (int, sympy.Integer)) and n > 1
    except Exception:
        h2 = False

    # H3: j is a fixed column index such that 1 <= j <= n
    try:
        h3 = isinstance(j, (int, sympy.Integer)) and 1 <= j <= n
    except Exception:
        h3 = False

    # Check if A is an n x n matrix
    try:
        if not hasattr(A, 'shape'):
            A = Matrix(A)
        is_valid_matrix = A.shape == (n, n)
    except Exception:
        is_valid_matrix = False

    # neg_Q: The sum of the principal ideals is NOT equal to R
    try:
        if not is_valid_matrix:
            neg_q = False
        else:
            col_idx = int(j) - 1
            elements = [A[i, col_idx] for i in range(int(n))]
            
            is_poly = False
            for e in elements:
                if hasattr(e, 'free_symbols') and e.free_symbols:
                    is_poly = True
                    break
            
            if is_poly:
                try:
                    gb = sympy.groebner(elements)
                    gb_list = list(gb)
                    is_R = (len(gb_list) == 1 and gb_list[0] == 1)
                except Exception:
                    g = reduce(sympy.gcd, elements)
                    is_R = getattr(g, 'is_number', False) and g != 0
            else:
                g = reduce(sympy.gcd, elements)
                try:
                    if hasattr(R, 'from_sympy') and hasattr(R, 'is_unit'):
                        g_R = R.from_sympy(sympy.sympify(g))
                        is_R = R.is_unit(g_R)
                    elif R == sympy.S.Integers or R == ZZ:
                        is_R = (abs(g) == 1)
                    elif R in [sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes, QQ]:
                        is_R = (g != 0)
                    else:
                        is_R = getattr(g, 'is_number', False) and g != 0
                except Exception:
                    is_R = getattr(g, 'is_number', False) and g != 0
                    
            neg_q = not is_R
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is an integer strictly greater than 1",
    "H_3: j is a fixed column index such that 1 <= j <= n",
    "¬Q: The sum of the principal ideals is not equal to R"
]

N_HYP = 3
NEG_Q_INDEX = 3