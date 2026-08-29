import sympy
from sympy import ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
Z = ZZ
Q = QQ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness can be a tuple (M, M_prime, M_double_prime) assuming R=ZZ,
    or a tuple (R, M, M_prime, M_double_prime).
    Modules can be represented by their rank (a non-negative integer) 
    or a list of invariant factors (where 0 represents a free component of rank 1).
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R', ZZ)
            M = witness.get('M')
            M_prime = witness.get('M_prime')
            M_double_prime = witness.get('M_double_prime')
            if M is None or M_prime is None or M_double_prime is None:
                return [False, False, False]
        elif isinstance(witness, tuple):
            if len(witness) == 4:
                R, M, M_prime, M_double_prime = witness
            elif len(witness) == 3:
                M, M_prime, M_double_prime = witness
                R = ZZ
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: R is a principal ideal domain
    try:
        if hasattr(R, 'is_PID') and R.is_PID:
            h1 = True
        elif R in [ZZ, QQ]:
            h1 = True
        elif hasattr(R, 'is_Field') and R.is_Field:
            h1 = True
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: M, M', and M'' are finitely generated R-modules
    try:
        def is_fg_module(mod):
            if isinstance(mod, (int, sympy.Integer)) and mod >= 0:
                return True
            if isinstance(mod, (list, tuple)):
                return all(isinstance(elem, (int, sympy.Expr, sympy.core.numbers.Number)) for elem in mod)
            return False
        
        h2 = is_fg_module(M) and is_fg_module(M_prime) and is_fg_module(M_double_prime)
    except Exception:
        h2 = False

    # ¬Q: The rank of M does not equal the rank of M' plus the rank of M''
    try:
        def get_rank(mod):
            if isinstance(mod, (int, sympy.Integer)):
                return int(mod)
            # For a list of invariant factors, the rank is the number of zeros
            return sum(1 for elem in mod if elem == 0)
        
        neg_q = get_rank(M) != get_rank(M_prime) + get_rank(M_double_prime)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M, M', and M'' are finitely generated R-modules",
    "¬Q: The rank of M does not equal the rank of M' plus the rank of M''"
]

N_HYP = 2
NEG_Q_INDEX = 2