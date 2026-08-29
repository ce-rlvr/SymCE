import sympy

# Top-level setup
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC
ZZ = sympy.ZZ
GF = sympy.GF

def conditions(witness):
    x, y, z = sympy.symbols('x y z')
    
    domain = None
    if isinstance(witness, int):
        try:
            if sympy.isprime(witness):
                domain = sympy.GF(witness)
        except Exception:
            pass
    else:
        domain = witness

    # H_1: K is a field
    h1 = False
    try:
        if domain is not None:
            h1 = bool(domain.is_Field)
    except Exception:
        pass

    # H_2: The characteristic of K is not 3
    h2 = False
    try:
        if domain is not None:
            h2 = bool(domain.characteristic != 3)
    except Exception:
        pass

    # H_3: There is no element a in K such that a^2 + 3 = 0
    h3 = False
    try:
        if domain is not None:
            poly_a = sympy.Poly(x**2 + 3, x, domain=domain)
            roots = sympy.roots(poly_a)
            h3 = bool(len(roots) == 0)
    except Exception:
        pass

    # ¬Q: The polynomial x^2 - xy + y^2 is reducible in K[x,y]
    neg_q = False
    try:
        if domain is not None:
            poly = x**2 - x*y + y**2
            try:
                # Try exact multivariate factorization over the domain
                factors = sympy.factor_list(poly, domain=domain)
                total_factors = sum(exp for f, exp in factors[1])
                neg_q = bool(total_factors > 1)
            except Exception:
                # Fallback: x^2 - xy + y^2 is a homogeneous polynomial of degree 2.
                # It factors into linear forms iff z^2 - z + 1 has a root in K.
                poly_z = sympy.Poly(z**2 - z + 1, z, domain=domain)
                roots = sympy.roots(poly_z)
                neg_q = bool(len(roots) > 0)
    except Exception:
        pass

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: The characteristic of K is not 3",
    "H_3: There is no element a in K such that a^2 + 3 = 0",
    "not Q: The polynomial x^2 - xy + y^2 is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3