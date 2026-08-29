import sympy
from sympy import degree, roots, Poly, Symbol, simplify
from sympy import QQ, ZZ, GF, RR, CC

# Top-level setup
x, y, z = sympy.symbols('x y z')

def conditions(witness):
    try:
        if len(witness) == 3:
            F, f_in, gen = witness
        elif len(witness) == 2:
            F, f_in = witness
            if hasattr(f_in, 'free_symbols') and f_in.free_symbols:
                if x in f_in.free_symbols:
                    gen = x
                elif y in f_in.free_symbols:
                    gen = y
                elif z in f_in.free_symbols:
                    gen = z
                else:
                    gen = list(f_in.free_symbols)[0]
            else:
                gen = x
        else:
            return [False, False, False, False]
            
        if isinstance(f_in, Poly):
            f = f_in.as_expr()
        else:
            f = f_in
    except Exception:
        return [False, False, False, False]

    # H1: F is a field
    try:
        h1 = bool(F.is_Field)
    except Exception:
        h1 = False

    # H2: The degree of f(x) is either 2 or 3
    try:
        deg = degree(f, gen)
        h2 = deg in (2, 3)
    except Exception:
        h2 = False

    # H3: f(x) has no roots in F
    try:
        has_root = False
        if hasattr(F, 'is_FiniteField') and F.is_FiniteField:
            for i in range(F.order):
                val = simplify(f.subs(gen, i))
                if val == 0:
                    has_root = True
                    break
                try:
                    if val % F.char == 0:
                        has_root = True
                        break
                except Exception:
                    pass
        else:
            rts = roots(f, gen)
            for r in rts:
                try:
                    if r in F:
                        has_root = True
                        break
                except Exception:
                    pass
        h3 = not has_root
    except Exception:
        h3 = False

    # neg_Q: f(x) is NOT irreducible over F
    try:
        try:
            p = Poly(f, gen, domain=F)
            is_in_Fx = True
        except Exception:
            is_in_Fx = False

        if is_in_Fx:
            irreducible = p.is_irreducible
        else:
            irreducible = False

        neg_q = not irreducible
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: The degree of f(x) is either 2 or 3",
    "H_3: f(x) has no roots in F",
    "¬Q: f(x) is not irreducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3