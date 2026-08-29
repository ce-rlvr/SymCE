import sympy
from sympy.ntheory import factorint, isprime
from sympy import factor_list

# Top-level setup for potential polynomial witnesses
x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "H_2: The principal ideal (a) is strictly contained in the principal ideal (b)",
    "¬Q: L(a) <= L(b)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        a, b = witness
    except Exception:
        return [False, False, False]
        
    # H1: R is a UFD
    # We accept integers (Z) or sympy expressions (like polynomials in Q[x] or Z[x]),
    # which are standard Unique Factorization Domains.
    try:
        a = sympy.sympify(a)
        b = sympy.sympify(b)
        h1 = bool(isinstance(a, sympy.Expr) and isinstance(b, sympy.Expr))
    except Exception:
        h1 = False

    # H2: The principal ideal (a) is strictly contained in the principal ideal (b)
    try:
        if not h1:
            h2 = False
        elif b == 0:
            # The zero ideal (0) does not strictly contain any ideal
            h2 = False
        elif a == 0:
            # The zero ideal (0) is strictly contained in any non-zero ideal
            h2 = True
        else:
            if a.is_Integer and b.is_Integer:
                # In Z, (a) is strictly contained in (b) iff b divides a and they are not associates
                h2 = bool((a % b == 0) and (abs(a) != abs(b)))
            else:
                # For polynomials, check divisibility
                q, r = sympy.div(a, b)
                if r != 0:
                    h2 = False
                else:
                    # Strictly contained means they are not associates (q is not a unit).
                    # In Q[x], units are non-zero constants.
                    if q.is_number and q != 0:
                        h2 = False
                    else:
                        h2 = True
    except Exception:
        h2 = False

    # Negated Conclusion: L(a) <= L(b)
    try:
        def L(val):
            if val == 0:
                return 0
            if val.is_Integer:
                # Count prime factors with multiplicity for integers
                return sum(v for k, v in factorint(int(val)).items() if isprime(k))
            else:
                # Count irreducible factors with multiplicity for polynomials
                try:
                    factors = factor_list(val, domain='ZZ')
                except Exception:
                    factors = factor_list(val)
                return sum(mult for f, mult in factors[1])
                
        neg_q = bool(L(a) <= L(b))
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]