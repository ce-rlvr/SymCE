import sympy
import sympy.ntheory
import math

CONDITION_LABELS = [
    "H_1: c_n(m) denotes Ramanujan's sum",
    "¬Q: c_n(m) != sum_{d|gcd(m,n)} d * mu(n/d)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            m = witness.get('m')
        else:
            n, m = witness
        h1 = isinstance(n, (int, sympy.Integer)) and isinstance(m, (int, sympy.Integer))
        if h1:
            n = int(n)
            m = int(m)
    except Exception:
        h1 = False

    try:
        if not h1:
            return [False, False]
        
        # Evaluate LHS: Ramanujan's sum
        if n < 1:
            lhs = 0
        else:
            lhs = 0
            for k in range(1, n + 1):
                if math.gcd(k, n) == 1:
                    lhs += sympy.exp(2 * sympy.pi * sympy.I * k * m / n)
            lhs = sympy.simplify(lhs)
            
        # Evaluate RHS: sum_{d|gcd(m,n)} d * mu(n/d)
        g = math.gcd(m, n)
        if g == 0:
            rhs_val = None
        else:
            rhs_val = 0
            for d in range(1, g + 1):
                if g % d == 0:
                    if n % d != 0:
                        rhs_val = None
                        break
                    nd = n // d
                    # mobius is only defined for positive integers in sympy
                    if nd < 1:
                        rhs_val = None
                        break
                    rhs_val += d * sympy.ntheory.mobius(nd)
                    
        if rhs_val is None:
            neg_q = True
        else:
            diff = sympy.simplify(lhs - rhs_val)
            if diff == 0:
                neg_q = False
            else:
                neg_q = abs(complex(diff)) > 1e-7
    except Exception:
        # If RHS evaluation fails, the equality fails
        neg_q = True

    return [h1, neg_q]