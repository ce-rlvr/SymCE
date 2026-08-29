import sympy
from sympy.ntheory import jacobi_symbol

# No specific top-level bindings needed for this number theory conjecture.

def is_int(x):
    return isinstance(x, (int, sympy.Integer)) and not isinstance(x, bool)

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the given witness.
    The witness is expected to be a tuple (a, b, c, p) or a dictionary with these keys.
    """
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            p = witness.get('p')
        else:
            a, b, c, p = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_int(a) and is_int(b) and is_int(c)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_int(p) and p != 0 and (a % p != 0)
    except Exception:
        h2_ok = False
        
    try:
        if not is_int(p) or p <= 0:
            # If p is not a positive integer, the standard Legendre/Jacobi symbol is undefined,
            # so the conclusion formula is invalid (hence the conclusion fails).
            neg_q_ok = True
        else:
            p_int = int(p)
            a_int = int(a)
            b_int = int(b)
            c_int = int(c)
            
            # Count distinct solutions modulo p
            solutions = sum(1 for x in range(p_int) if (a_int * x**2 + b_int * x + c_int) % p_int == 0)
            
            # Calculate expected number of solutions: 1 + (D/p)
            D = b_int**2 - 4 * a_int * c_int
            expected = 1 + jacobi_symbol(D, p_int)
            
            # The conclusion fails if the actual number of solutions does not match the expected formula
            neg_q_ok = (solutions != expected)
    except Exception:
        # If jacobi_symbol raises an error (e.g., p is even), the formula is undefined,
        # meaning the conclusion fails.
        neg_q_ok = True
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: a, b, and c are integers",
    "H_2: p does not divide a",
    "¬Q: The congruence ax^2 + bx + c ≡ 0 (mod p) does not have exactly 1 + ((b^2 - 4ac)/p) distinct solutions modulo p"
]

N_HYP = 2
NEG_Q_INDEX = 2