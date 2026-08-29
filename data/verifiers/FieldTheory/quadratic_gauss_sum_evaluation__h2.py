import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the Quadratic Gauss Sum Evaluation conjecture.
    The witness can be a tuple (p, zeta, g) or a dict with these keys.
    If zeta is omitted, it is inferred from the free symbols of g, or defaults to a new symbol.
    """
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                p, zeta, g = witness
            elif len(witness) == 2:
                p, g = witness
                free = getattr(g, "free_symbols", set())
                if len(free) == 1:
                    zeta = list(free)[0]
                else:
                    zeta = sympy.Symbol('zeta')
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            p = witness.get('p')
            g = witness.get('g')
            zeta = witness.get('zeta')
            if zeta is None:
                free = getattr(g, "free_symbols", set())
                if len(free) == 1:
                    zeta = list(free)[0]
                else:
                    zeta = sympy.Symbol('zeta')
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: p is an odd prime number
    try:
        h1 = bool(sympy.isprime(p) and p % 2 == 1)
    except Exception:
        h1 = False

    # H_2: g = sum_{a=1}^{p-1} (a/p) zeta_p^a
    try:
        if not h1:
            h2 = False
        else:
            expected_g = 0
            for a in range(1, int(p)):
                expected_g += sympy.jacobi_symbol(a, int(p)) * (zeta ** a)
            
            diff = sympy.simplify(g - expected_g)
            if hasattr(diff, 'is_zero_matrix'):
                is_zm = diff.is_zero_matrix
                if callable(is_zm):
                    h2 = bool(is_zm())
                else:
                    h2 = bool(is_zm)
            else:
                h2 = bool(diff == 0)
    except Exception:
        h2 = False

    # ¬Q: g^2 != (-1)^{(p-1)/2} p
    try:
        if not h1:
            neg_q = False
        else:
            rhs = ((-1) ** ((int(p) - 1) // 2)) * int(p)
            try:
                diff_q = sympy.simplify(g**2 - rhs)
                if hasattr(diff_q, 'is_zero_matrix'):
                    is_zm = diff_q.is_zero_matrix
                    if callable(is_zm):
                        neg_q = not bool(is_zm())
                    else:
                        neg_q = not bool(is_zm)
                else:
                    neg_q = bool(diff_q != 0)
            except Exception:
                # If subtraction fails (e.g., matrix minus scalar), they are not equal
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: p is an odd prime number",
    "H_2: g = sum_{a=1}^{p-1} (a/p) zeta_p^a where (a/p) is the Legendre symbol",
    "¬Q: g^2 != (-1)^{(p-1)/2} p"
]

N_HYP = 2
NEG_Q_INDEX = 2