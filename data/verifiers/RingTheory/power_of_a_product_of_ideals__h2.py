import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If R is a commutative ring and n is a positive integer, then (IJ)^n = I^n J^n."
    
    The dropped hypothesis was likely "I and J are ideals of R" or "I and J are elements of R".
    Without it, I and J can be objects that do not commute (e.g., matrices over R),
    making the conclusion false.
    """
    # Unpack witness. It could be (R, I, J, n) or just (I, J, n) with R implicit.
    try:
        if len(witness) == 4:
            R, I, J, n = witness
        elif len(witness) == 3:
            I, J, n = witness
            R = sympy.ZZ  # Default to the commutative ring of integers
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    try:
        if hasattr(R, 'is_commutative') and R.is_commutative is False:
            h1 = False
        elif hasattr(R, 'is_commutative_ring') and R.is_commutative_ring is False:
            h1 = False
        elif isinstance(R, str) and 'non' in R.lower() and 'comm' in R.lower():
            h1 = False
        elif isinstance(R, Matrix):
            h1 = False
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: n is a positive integer
    try:
        h2 = False
        if isinstance(n, (int, sympy.Integer)):
            h2 = bool(n > 0)
    except Exception:
        h2 = False

    # ¬Q: (IJ)^n != I^n J^n
    try:
        IJ = I * J
        left = IJ ** n
        right = (I ** n) * (J ** n)
        
        if isinstance(left, Matrix) and isinstance(right, Matrix):
            neg_q = bool(left != right)
        else:
            diff = left - right
            if hasattr(diff, 'simplify'):
                diff = diff.simplify()
            
            if hasattr(diff, 'is_zero') and diff.is_zero is not None:
                neg_q = not bool(diff.is_zero)
            else:
                if hasattr(left, 'expand') and hasattr(right, 'expand'):
                    neg_q = bool(left.expand() != right.expand())
                else:
                    neg_q = bool(left != right)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is a positive integer",
    "¬Q: (IJ)^n != I^n J^n"
]

N_HYP = 2
NEG_Q_INDEX = 2