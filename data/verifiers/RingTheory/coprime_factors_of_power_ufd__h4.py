import sympy
from sympy.abc import x, y, z

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 4:
            return [False] * 5
        a, b, c, n = witness
    except Exception:
        return [False] * 5

    # H1: R is a unique factorization domain
    # We support Z, Z[x, y, ...], and Q[x, y, ...] as valid UFDs.
    try:
        is_int = all(isinstance(val, (int, sympy.Integer)) for val in (a, b, c))
        if is_int:
            h1 = True
            ring = 'Z'
        else:
            polys = [sympy.Poly(val) for val in (a, b, c)]
            h1 = True
            # If all coefficients of all polynomials are integers, we treat it as Z[X]
            if all(all(isinstance(coeff, (int, sympy.Integer)) for coeff in p.coeffs()) for p in polys):
                ring = 'Z[x]'
            else:
                ring = 'Q[x]'
    except Exception:
        h1 = False
        ring = None

    # H2: a, b, c are non-zero elements of R
    try:
        if ring == 'Z':
            h2 = h1 and a != 0 and b != 0 and c != 0
        elif ring in ('Z[x]', 'Q[x]'):
            h2 = h1 and all(not p.is_zero for p in polys)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: n is a positive integer
    try:
        h3 = isinstance(n, (int, sympy.Integer)) and n > 0
    except Exception:
        h3 = False

    # H4: ab = c^n
    try:
        if ring == 'Z':
            h4 = (a * b == c ** n)
        elif ring in ('Z[x]', 'Q[x]'):
            diff = sympy.expand(a * b - c ** n)
            h4 = (diff == 0)
        else:
            h4 = False
    except Exception:
        h4 = False

    # neg_Q: a is not of the form u*x^n OR b is not of the form v*y^n for units u, v
    try:
        def is_nth_power_up_to_unit(val, power, r):
            if r == 'Z':
                if val == 0:
                    return False
                factors = sympy.factorint(abs(int(val)))
                return all(m % power == 0 for p, m in factors.items())
            elif r == 'Z[x]':
                val_expr = sympy.sympify(val)
                coeff, factors = sympy.factor_list(val_expr)
                if coeff == 0:
                    return False
                coeff_factors = sympy.factorint(abs(int(coeff)))
                coeff_ok = all(m % power == 0 for p, m in coeff_factors.items())
                poly_ok = all(m % power == 0 for f, m in factors)
                return coeff_ok and poly_ok
            elif r == 'Q[x]':
                val_expr = sympy.sympify(val)
                coeff, factors = sympy.factor_list(val_expr)
                if coeff == 0:
                    return False
                poly_ok = all(m % power == 0 for f, m in factors)
                return poly_ok
            return False

        if ring and h3:
            a_is_power = is_nth_power_up_to_unit(a, n, ring)
            b_is_power = is_nth_power_up_to_unit(b, n, ring)
            neg_q = not (a_is_power and b_is_power)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: a, b, and c are non-zero elements of R",
    "H_3: n is a positive integer",
    "H_4: ab = c^n",
    "¬Q: a is not of the form u*x^n or b is not of the form v*y^n for units u,v"
]

N_HYP = 4
NEG_Q_INDEX = 4