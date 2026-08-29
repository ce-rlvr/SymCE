import sympy

# Top-level setup: named object bindings that the witness expression may reference.
x, y = sympy.symbols('x y')

def conditions(witness) -> list[bool]:
    # H_1: Let F be a field of characteristic not equal to 2 or 3.
    try:
        if isinstance(witness, (list, tuple, set)) and len(witness) == 1:
            witness = list(witness)[0]

        if isinstance(witness, sympy.Poly):
            poly = witness
        elif isinstance(witness, sympy.Eq):
            poly = sympy.Poly(witness.lhs - witness.rhs, x, y)
        else:
            expr = sympy.sympify(witness)
            poly = sympy.Poly(expr, x, y)
            
        h1 = (poly.domain.characteristic not in (2, 3))
    except Exception:
        h1 = False

    # ¬Q: The factor ring is NOT an integrally closed domain.
    try:
        if isinstance(witness, (list, tuple, set)) and len(witness) == 1:
            witness = list(witness)[0]

        if isinstance(witness, sympy.Poly):
            poly = witness
        elif isinstance(witness, sympy.Eq):
            poly = sympy.Poly(witness.lhs - witness.rhs, x, y)
        else:
            expr = sympy.sympify(witness)
            poly = sympy.Poly(expr, x, y)
            
        if poly.is_zero:
            neg_q = False
        elif poly.is_constant():
            neg_q = True
        else:
            domain = poly.domain
            if hasattr(domain, 'get_field'):
                field_domain = domain.get_field()
            else:
                field_domain = domain
                
            poly_field = poly.set_domain(field_domain)
            
            factors = sympy.factor_list(poly_field)
            is_reducible = sum(power for _, power in factors[1]) > 1
            
            fx = poly_field.diff(x)
            fy = poly_field.diff(y)
            gb = sympy.groebner([poly_field, fx, fy], x, y, domain=field_domain)
            
            has_singular_point = True
            for p in gb:
                if isinstance(p, sympy.Poly):
                    if p.is_constant() and not p.is_zero:
                        has_singular_point = False
                        break
                else:
                    if not p.has(x) and not p.has(y) and p != 0:
                        has_singular_point = False
                        break
            
            neg_q = bool(is_reducible or has_singular_point)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2 or 3",
    "¬Q: The factor ring is not an integrally closed domain"
]

N_HYP = 1
NEG_Q_INDEX = 1