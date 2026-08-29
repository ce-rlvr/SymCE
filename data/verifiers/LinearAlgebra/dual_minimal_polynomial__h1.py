import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

CONDITION_LABELS = [
    "H_1: T is a linear operator",
    "¬Q: The minimal polynomial of T is NOT identical to the minimal polynomial of the dual operator T*"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    # H_1: T is a linear operator
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('is_linear_operator', True))
        elif hasattr(witness, 'is_linear_operator'):
            val = witness.is_linear_operator
            h1 = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_linear'):
            val = witness.is_linear
            h1 = bool(val() if callable(val) else val)
        else:
            from sympy import MatrixBase
            h1 = isinstance(witness, MatrixBase)
    except Exception:
        h1 = False

    # ¬Q: The minimal polynomial of T is NOT identical to the minimal polynomial of T*
    try:
        if isinstance(witness, dict):
            mp_T = witness.get('minpoly')
            mp_T_star = witness.get('dual_minpoly')
        else:
            # Get minimal polynomial of T
            if hasattr(witness, 'minpoly'):
                val = witness.minpoly
                mp_T = val() if callable(val) else val
            else:
                from sympy import minpoly
                from sympy.abc import x
                mp_T = minpoly(witness, x)

            # Get minimal polynomial of T*
            if hasattr(witness, 'dual_minpoly'):
                val = witness.dual_minpoly
                mp_T_star = val() if callable(val) else val
            elif hasattr(witness, 'dual'):
                dual_T = witness.dual() if callable(witness.dual) else witness.dual
                if hasattr(dual_T, 'minpoly'):
                    val = dual_T.minpoly
                    mp_T_star = val() if callable(val) else val
                else:
                    from sympy import minpoly
                    from sympy.abc import x
                    mp_T_star = minpoly(dual_T, x)
            elif hasattr(witness, 'transpose'):
                from sympy import minpoly
                from sympy.abc import x
                mp_T_star = minpoly(witness.transpose(), x)
            else:
                mp_T_star = mp_T  # Fallback: will cause neg_q to be False

        # Compare the minimal polynomials
        if mp_T is None and mp_T_star is None:
            neg_q = False
        elif mp_T is None or mp_T_star is None:
            neg_q = True
        elif mp_T == mp_T_star:
            neg_q = False
        else:
            try:
                from sympy import simplify
                diff = simplify(mp_T - mp_T_star)
                neg_q = bool(diff != 0)
            except Exception:
                # If they cannot be simplified/subtracted but are not equal, they are not identical
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, neg_q]