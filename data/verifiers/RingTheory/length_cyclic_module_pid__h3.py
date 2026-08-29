import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
from sympy import factor_list, Mul, Pow, Expr, S, prod
from sympy.abc import x, y, z

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
    R = S.Integers
    a = None
    k_list = None

    # Extract R, a, and k_list from the witness
    try:
        if isinstance(witness, Expr) and not witness.is_Integer:
            a = witness.doit()
            k_list = []
            if isinstance(witness, Mul):
                for arg in witness.args:
                    if isinstance(arg, Pow):
                        k_list.append(arg.exp)
                    else:
                        k_list.append(1)
            elif isinstance(witness, Pow):
                k_list = [witness.exp]
            else:
                return [False, False, False]
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                a, second = witness
            elif len(witness) == 3:
                R, a, second = witness
            else:
                return [False, False, False]
            
            if isinstance(second, list):
                if len(second) > 0 and isinstance(second[0], tuple):
                    k_list = [k for b, k in second]
                else:
                    try:
                        if prod(second) == a:
                            k_list = [1] * len(second)
                        else:
                            k_list = second
                    except Exception:
                        k_list = second
            elif isinstance(second, dict):
                k_list = list(second.values())
            elif isinstance(second, (int, sympy.Integer)):
                k_list = [second]
            else:
                return [False, False, False]
        elif isinstance(witness, list):
            if len(witness) > 0 and isinstance(witness[0], tuple):
                a = prod([b**k for b, k in witness])
                k_list = [k for b, k in witness]
            else:
                a = prod(witness)
                k_list = [1] * len(witness)
        elif isinstance(witness, dict):
            a = prod([b**k for b, k in witness.items()])
            k_list = list(witness.values())
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    try:
        if R in (S.Integers, int):
            h1 = True
        elif hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif type(R).__name__ == 'PolynomialRing' and len(R.gens) == 1 and R.domain.is_Field:
            h1 = True
        elif type(R).__name__ in ('IntegerRing', 'RationalField'):
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: a is a non-zero non-unit element of R
    try:
        if a == 0:
            h2 = False
        elif R in (S.Integers, int) or type(R).__name__ == 'IntegerRing':
            h2 = (abs(int(a)) != 1)
        elif type(R).__name__ == 'RationalField':
            h2 = False
        else:
            if hasattr(a, 'is_zero') and a.is_zero:
                h2 = False
            elif hasattr(a, 'is_unit') and a.is_unit:
                h2 = False
            elif hasattr(a, 'degree'):
                h2 = a.degree() > 0
            else:
                h2 = (a not in (0, 1, -1))
    except Exception:
        h2 = False

    # ¬Q: The R-module R/<a> does not have finite length equal to sum(k_i)
    try:
        if R in (S.Integers, int) or type(R).__name__ == 'IntegerRing':
            actual_length = sum(factorint(abs(int(a))).values())
        else:
            f = factor_list(a)
            actual_length = sum(exp for factor, exp in f[1])
        
        expected_length = sum(k_list)
        neg_q = bool(actual_length != expected_length)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: a is a non-zero non-unit element of R",
    "¬Q: The R-module R/<a> does not have finite length equal to sum(k_i)"
]

N_HYP = 2
NEG_Q_INDEX = 2