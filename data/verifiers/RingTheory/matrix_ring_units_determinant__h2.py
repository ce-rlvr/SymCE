import sympy
from sympy import MatrixBase, eye, zeros
import math
from sympy.polys.constructor import construct_domain

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: A is a matrix in M_n(R)",
    "¬Q: It is NOT the case that (A is a unit in M_n(R) iff det(A) is a unit in R)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    R_domain = None
    if isinstance(witness, tuple) and len(witness) == 2:
        R_domain, A = witness
    else:
        A = witness

    # H1: R is a commutative ring with identity
    try:
        if R_domain is not None:
            if isinstance(R_domain, int) and R_domain > 1:
                h1 = True
            else:
                h1 = getattr(R_domain, 'is_Ring', False) or getattr(R_domain, 'is_Field', False)
        else:
            h1 = all(getattr(x, 'is_commutative', True) for x in A)
    except Exception:
        h1 = False

    # H2: A is a matrix in M_n(R)
    try:
        h2 = hasattr(A, 'shape') and len(A.shape) == 2 and A.shape[0] == A.shape[1]
    except Exception:
        h2 = False

    # neg_Q: A is a unit in M_n(R) iff det(A) is a unit in R
    try:
        if R_domain is not None:
            if isinstance(R_domain, int) and R_domain > 1:
                det_A = int(A.det()) % R_domain
                det_is_unit = math.gcd(det_A, R_domain) == 1
                try:
                    A.inv_mod(R_domain)
                    A_is_unit = True
                except Exception:
                    A_is_unit = False
            else:
                det_A = A.det()
                try:
                    det_val = R_domain.from_sympy(det_A)
                    det_is_unit = R_domain.is_unit(det_val)
                except Exception:
                    det_is_unit = False
                
                try:
                    A_inv = A.inv()
                    A_is_unit = True
                    for x in A_inv:
                        try:
                            R_domain.from_sympy(x)
                        except Exception:
                            A_is_unit = False
                            break
                except Exception:
                    A_is_unit = False
        else:
            try:
                domain, _ = construct_domain(list(A))
                det_A = A.det()
                det_val = domain.from_sympy(det_A)
                det_is_unit = domain.is_unit(det_val)
                
                try:
                    A_inv = A.inv()
                    A_is_unit = True
                    for x in A_inv:
                        try:
                            domain.from_sympy(x)
                        except Exception:
                            A_is_unit = False
                            break
                except Exception:
                    A_is_unit = False
            except Exception:
                # Fallback for cases where construct_domain fails
                free_symbols = getattr(A, 'free_symbols', set())
                if not free_symbols:
                    if all(getattr(x, 'is_integer', False) for x in A):
                        det_A = A.det()
                        det_is_unit = (abs(det_A) == 1)
                        try:
                            A_inv = A.inv()
                            A_is_unit = all(getattr(x, 'is_integer', False) for x in A_inv)
                        except Exception:
                            A_is_unit = False
                    else:
                        det_A = A.det()
                        det_is_unit = (det_A != 0)
                        try:
                            A.inv()
                            A_is_unit = True
                        except Exception:
                            A_is_unit = False
                else:
                    det_A = A.det()
                    det_is_unit = getattr(det_A, 'is_constant', lambda: False)() and det_A != 0
                    try:
                        A_inv = A.inv()
                        from sympy import fraction
                        A_is_unit = all(fraction(x.cancel())[1] == 1 for x in A_inv)
                    except Exception:
                        A_is_unit = False
                        
        q = (A_is_unit == det_is_unit)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]