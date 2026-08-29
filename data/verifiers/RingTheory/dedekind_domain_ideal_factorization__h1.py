import sympy
from sympy import gcd
from sympy.ntheory import factorint
from sympy.abc import x, y, z

class IdealInZn:
    """
    Represents the principal ideal (a) in the ring Z/nZ.
    Use this to construct counterexamples.
    Example: IdealInZn(12, 3) represents the ideal (3) in Z/12Z.
    """
    def __init__(self, n, a):
        self.n = int(n)
        self.a = int(a) % self.n

def conditions(witness):
    try:
        # 1. Check if the witness is an instance of IdealInZn
        if isinstance(witness, IdealInZn):
            n = witness.n
            a = witness.a
            if n > 1:
                g = gcd(a, n)
                # H1: I is a non-zero proper ideal of R
                h1 = bool((g > 1) and (g < n))
                
                # neg_Q: I cannot be written uniquely as a product of prime ideals
                # In Z/nZ, factorization into prime ideals is not unique iff 
                # there is some prime factor p of n such that v_p(g) == v_p(n).
                factors_n = factorint(n)
                factors_g = factorint(g)
                not_unique = any(factors_g.get(p, 0) == v_n for p, v_n in factors_n.items())
                
                return [h1, bool(not_unique)]
                
        # 2. Check if the witness is a tuple or list (e.g., (n, a) or (x**2, 2))
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            # Try Z[x] counterexample first (e.g., the ideal (x^2, 2) in Z[x])
            try:
                p1, p2 = witness
                if isinstance(p1, (int, sympy.Integer)):
                    p1, p2 = p2, p1
                if isinstance(p2, (int, sympy.Integer)) and abs(p2) >= 2:
                    if p1 == x**2 or p1 == y**2 or p1 == z**2 or \
                       (isinstance(p1, sympy.Pow) and isinstance(p1.base, sympy.Symbol) and isinstance(p1.exp, (int, sympy.Integer)) and p1.exp >= 2):
                        # (x^k, m) for k >= 2 and |m| >= 2 is a proper non-zero ideal in Z[x]
                        # and cannot be written as a product of prime ideals.
                        return [True, True]
            except Exception:
                pass
                
            # Try Z/nZ counterexample (e.g., (12, 3))
            try:
                n = int(witness[0])
                a = int(witness[1])
                if n > 1:
                    g = gcd(a, n)
                    h1 = bool((g > 1) and (g < n))
                    factors_n = factorint(n)
                    factors_g = factorint(g)
                    not_unique = any(factors_g.get(p, 0) == v_n for p, v_n in factors_n.items())
                    return [h1, bool(not_unique)]
            except Exception:
                pass

        return [False, False]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a non-zero proper ideal of R",
    "¬Q: I cannot be written uniquely (up to the order of factors) as a product of prime ideals of R"
]

N_HYP = 1
NEG_Q_INDEX = 1