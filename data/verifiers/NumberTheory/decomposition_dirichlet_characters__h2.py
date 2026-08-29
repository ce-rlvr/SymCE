import math
import sympy

def check_equal(x, y):
    if x == y:
        return True
    try:
        return abs(complex(x) - complex(y)) < 1e-9
    except Exception:
        pass
    try:
        return bool(sympy.simplify(x - y) == 0)
    except Exception:
        return False

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness is expected to be a tuple (n, chi), where n is a positive integer
    and chi is a list, tuple, dict, or callable representing the function \chi(a).
    """
    try:
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], int):
            n, chi = witness
        elif isinstance(witness, (list, tuple, dict)):
            chi = witness
            n = len(chi)
        elif callable(witness):
            return [False, False]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: n is a positive integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n >= 1
    except Exception:
        h1 = False
        
    # ¬Q: chi cannot be uniquely decomposed into Dirichlet characters modulo prime powers of n.
    # This is mathematically equivalent to checking that chi is NOT a Dirichlet character modulo n.
    try:
        neg_q = False
        if h1:
            def eval_chi(a):
                if callable(chi):
                    return chi(a)
                else:
                    return chi[a % len(chi)]
            
            is_dirichlet = True
            
            # Condition 1: chi(1) == 1
            if not check_equal(eval_chi(1), 1):
                is_dirichlet = False
                
            # Condition 2: chi(a) == 0 iff gcd(a, n) > 1
            if is_dirichlet:
                for a in range(n):
                    val = eval_chi(a)
                    if math.gcd(a, n) > 1:
                        if not check_equal(val, 0):
                            is_dirichlet = False
                            break
                    else:
                        if check_equal(val, 0):
                            is_dirichlet = False
                            break
                            
            # Condition 3: Completely multiplicative, chi(ab) == chi(a)chi(b)
            if is_dirichlet:
                for a in range(n):
                    for b in range(n):
                        if not check_equal(eval_chi(a * b), eval_chi(a) * eval_chi(b)):
                            is_dirichlet = False
                            break
                    if not is_dirichlet:
                        break
                        
            # Condition 4: Periodic modulo n, chi(a + n) == chi(a)
            if is_dirichlet:
                for a in range(n):
                    if not check_equal(eval_chi(a + n), eval_chi(a)):
                        is_dirichlet = False
                        break
                        
            neg_q = not is_dirichlet
    except Exception:
        # If evaluation fails, it's not a valid Dirichlet character, so the conclusion fails.
        # However, to avoid false positives on malformed witnesses, we return False.
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: chi cannot be uniquely decomposed into Dirichlet characters modulo prime powers of n"
]

N_HYP = 1
NEG_Q_INDEX = 1