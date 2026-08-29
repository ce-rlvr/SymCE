import sympy
from sympy import symbols, poly, gcd, roots

x, y = symbols('x y')

def conditions(witness) -> list[bool]:
    try:
        g, n = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: K is an algebraically closed field
    h1 = True
    
    # H2: g(x) is a non-constant polynomial
    try:
        if not g.free_symbols.issubset({x}):
            h2 = False
        else:
            g_poly = poly(g, x)
            h2 = g_poly.degree() > 0
    except Exception:
        h2 = False
        
    # H3: There exists a root of g(x) with multiplicity coprime to n
    try:
        if int(n) != n:
            h3 = False
        else:
            n_int = int(n)
            rts = roots(g, x)
            h3 = False
            for r, mult in rts.items():
                if gcd(mult, n_int) == 1:
                    h3 = True
                    break
    except Exception:
        h3 = False
        
    # neg_Q: y^n - g(x) is reducible over K
    try:
        if int(n) != n:
            neg_q = False
        else:
            n_int = int(n)
            if n_int < 0:
                neg_q = False
            elif n_int == 0:
                # For n = 0, y^0 - g(x) = 1 - g(x).
                # Over an algebraically closed field, any polynomial of degree >= 2 is reducible.
                deg = poly(1 - g, x).degree()
                neg_q = deg >= 2
            else:
                # For n >= 1, by Capelli's theorem over an algebraically closed field,
                # y^n - g(x) is reducible iff g(x) is a p-th power for some prime p dividing n.
                # This is equivalent to all root multiplicities being divisible by p.
                is_reducible = False
                g_poly = poly(g, x)
                rts = roots(g, x)
                if sum(rts.values()) == g_poly.degree() and g_poly.degree() > 0:
                    for p in sympy.primefactors(n_int):
                        if all(mult % p == 0 for mult in rts.values()):
                            is_reducible = True
                            break
                neg_q = is_reducible
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: g(x) is a non-constant polynomial over K",
    "H_3: There exists a root of g(x) with multiplicity coprime to n",
    "¬Q: y^n - g(x) is reducible over K"
]

N_HYP = 3
NEG_Q_INDEX = 3