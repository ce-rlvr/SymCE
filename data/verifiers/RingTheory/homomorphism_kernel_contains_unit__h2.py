import sympy
from sympy import ZZ, QQ
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            S = witness.get('S')
            f = witness.get('f')
            u = witness.get('u')
            u_inv = witness.get('u_inv')
        else:
            R = getattr(witness, 'R', None)
            S = getattr(witness, 'S', None)
            f = getattr(witness, 'f', None)
            u = getattr(witness, 'u', None)
            u_inv = getattr(witness, 'u_inv', None)

        # H_1: R and S are rings with identity
        h1 = False
        try:
            if R is not None and S is not None:
                R_has_zero = hasattr(R, 'zero')
                R_has_one = hasattr(R, 'one') or hasattr(R, 'identity')
                S_has_zero = hasattr(S, 'zero')
                S_has_one = hasattr(S, 'one') or hasattr(S, 'identity')
                if R_has_zero and R_has_one and S_has_zero and S_has_one:
                    h1 = True
        except Exception:
            h1 = False

        # H_2: There exists a unit u in R such that u in ker(f)
        h2 = False
        try:
            is_unit = False
            if hasattr(R, 'is_unit'):
                is_unit = bool(R.is_unit(u))
            elif u_inv is not None:
                R_one = getattr(R, 'one', getattr(R, 'identity', 1))
                if hasattr(R, 'mul'):
                    if R.mul(u, u_inv) == R_one and R.mul(u_inv, u) == R_one:
                        is_unit = True
                else:
                    if u * u_inv == R_one and u_inv * u == R_one:
                        is_unit = True
            elif isinstance(u, (int, sympy.Integer)) and u in [1, -1]:
                is_unit = True

            in_ker = False
            if is_unit and f is not None:
                if callable(f):
                    val = f(u)
                elif isinstance(f, dict):
                    val = f.get(u)
                elif hasattr(f, 'is_Matrix') and f.is_Matrix:
                    val = f * u
                else:
                    val = None
                
                if val is not None:
                    if hasattr(S, 'zero'):
                        if val == S.zero:
                            in_ker = True
                    else:
                        if val == 0:
                            in_ker = True
            
            h2 = is_unit and in_ker
        except Exception:
            h2 = False

        # neg_Q: S is not the zero ring
        neg_q = False
        try:
            if hasattr(S, 'zero') and (hasattr(S, 'one') or hasattr(S, 'identity')):
                S_one = getattr(S, 'one', getattr(S, 'identity', None))
                neg_q = (S.zero != S_one)
            else:
                if hasattr(S, '__len__'):
                    neg_q = len(S) > 1
                else:
                    neg_q = True
        except Exception:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are rings with identity",
    "H_2: There exists a unit u in R such that u in ker(f)",
    "¬Q: S is not the zero ring"
]

N_HYP = 2
NEG_Q_INDEX = 2