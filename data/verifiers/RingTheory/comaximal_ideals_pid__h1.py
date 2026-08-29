import sympy as sp
from sympy import symbols, QQ, ZZ

# Top-level setup: named object bindings that the witness expression may reference.
x, y, z = symbols('x y z')

CONDITION_LABELS = [
    "H_1: a and b are elements of R",
    "H_2: The greatest common divisor of a and b is a unit",
    "¬Q: The ideal sum <a> + <b> is not equal to the entire ring R"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    """
    Checks if the given witness is a valid counterexample.
    Expected witness formats:
      - (a, b)  -> Assumes domain is QQ, infers generators from free symbols.
      - (R, a, b) or (a, b, R) -> Uses domain and generators from the ring R.
      - (a, b, domain, gens) -> Explicitly specifies elements, domain, and generators.
    """
    try:
        def to_expr(expr):
            if isinstance(expr, sp.Poly):
                return expr.as_expr()
            return sp.sympify(expr)

        # Parse the witness
        if isinstance(witness, dict):
            a = witness.get('a')
            b = witness.get('b')
            domain = witness.get('domain', QQ)
            gens = witness.get('gens')
        elif isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
                domain = QQ
                gens = None
            elif len(witness) == 3:
                if hasattr(witness[0], 'from_sympy') and hasattr(witness[0], 'is_unit'):
                    R, a, b = witness
                elif hasattr(witness[2], 'from_sympy') and hasattr(witness[2], 'is_unit'):
                    a, b, R = witness
                else:
                    a, b, R = witness
                
                if hasattr(R, 'domain') and hasattr(R, 'gens'):
                    domain = R.domain
                    gens = R.gens
                elif hasattr(R, 'from_sympy') and hasattr(R, 'is_unit'):
                    domain = R
                    gens = None
                else:
                    domain = QQ
                    gens = None
            elif len(witness) == 4:
                a, b, domain, gens = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]

        a = to_expr(a)
        b = to_expr(b)

        if gens is None:
            gens = tuple(sorted(a.free_symbols | b.free_symbols, key=lambda s: s.name))
        else:
            gens = tuple(to_expr(g) for g in gens)

    except Exception:
        return [False, False, False]

    # H_1: a and b are elements of R
    try:
        if gens:
            sp.Poly(a, *gens, domain=domain)
            sp.Poly(b, *gens, domain=domain)
            h1_ok = True
        else:
            domain.from_sympy(a)
            domain.from_sympy(b)
            h1_ok = True
    except Exception:
        h1_ok = False

    # H_2: The greatest common divisor of a and b is a unit
    try:
        g = sp.gcd(a, b, domain=domain)
        g = to_expr(g)
        if gens and any(g.has(gen) for gen in gens):
            h2_ok = False
        else:
            g_val = domain.from_sympy(g)
            h2_ok = domain.is_unit(g_val)
    except Exception:
        h2_ok = False

    # ¬Q: The ideal sum <a> + <b> is not equal to the entire ring R
    try:
        if not gens:
            g = sp.gcd(a, b, domain=domain)
            g = to_expr(g)
            g_val = domain.from_sympy(g)
            is_whole_ring = domain.is_unit(g_val)
        else:
            gb = sp.groebner([a, b], *gens, domain=domain)
            gb_list = [to_expr(elem) for elem in gb]
            is_whole_ring = False
            if len(gb_list) == 1:
                elem = gb_list[0]
                # A polynomial is a unit iff it is a non-zero constant that is a unit in the coefficient domain
                if not any(elem.has(gen) for gen in gens):
                    val = domain.from_sympy(elem)
                    if domain.is_unit(val):
                        is_whole_ring = True
        neg_q_ok = not is_whole_ring
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]