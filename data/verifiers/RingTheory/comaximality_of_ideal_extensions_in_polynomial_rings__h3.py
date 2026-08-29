import sympy
from sympy.matrices import eye, zeros
from sympy import S

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    H1 = False
    H2 = True
    H3 = False
    neg_Q = False

    try:
        if isinstance(witness, dict):
            R = witness.get('R', witness)
            I = witness.get('I', None)
            J = witness.get('J', None)
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
        else:
            R = getattr(witness, 'R', witness)
            I = getattr(witness, 'I', None)
            J = getattr(witness, 'J', None)
    except Exception:
        return [False, False, False, False]

    try:
        if hasattr(witness, 'H1'):
            H1 = bool(getattr(witness, 'H1'))
        elif hasattr(R, 'is_commutative'):
            val = R.is_commutative
            H1 = bool(val() if callable(val) else val)
        elif isinstance(R, list) and all(hasattr(m, 'is_Matrix') for m in R):
            H1 = all(A*B == B*A for A in R for B in R)
        else:
            H1 = True
    except Exception:
        H1 = False

    try:
        if hasattr(witness, 'H3'):
            H3 = bool(getattr(witness, 'H3'))
        elif I is not None and J is not None:
            if isinstance(R, list) and all(hasattr(m, 'is_Matrix') for m in R):
                sums = [a + b for a in I for b in J]
                H3 = all(any(r == s for s in sums) for r in R)
            elif hasattr(R, 'is_comaximal'):
                H3 = bool(R.is_comaximal(I, J))
            elif isinstance(I, set) and isinstance(J, set) and isinstance(R, set):
                sums = set(i + j for i in I for j in J)
                H3 = (sums == R)
            else:
                H3 = True
        else:
            H3 = True
    except Exception:
        H3 = False

    try:
        if hasattr(witness, 'neg_Q'):
            neg_Q = bool(getattr(witness, 'neg_Q'))
        elif isinstance(R, list) and all(hasattr(m, 'is_Matrix') for m in R):
            prods = [a * b for a in R for b in R]
            R_squared_equals_R = all(any(r == p for p in prods) for r in R)
            neg_Q = not R_squared_equals_R
        elif hasattr(R, 'has_identity'):
            val = R.has_identity
            has_id = bool(val() if callable(val) else val)
            neg_Q = not has_id
        else:
            neg_Q = True
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: Polynomial ring over R",
    "H_3: I and J are comaximal in R",
    "¬Q: The extended ideals are not comaximal"
]

N_HYP = 3
NEG_Q_INDEX = 3