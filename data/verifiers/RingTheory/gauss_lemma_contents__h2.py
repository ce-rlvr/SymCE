import sympy as sp
from sympy import eye, zeros
from sympy.abc import x, y, z
from sympy.polys.constructor import construct_domain

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a Unique Factorization Domain",
    "¬Q: The content of the product fg is not associate to the product of the contents of f and g"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 4:
                R, gens, f, g = witness
            elif len(witness) == 3:
                R, f, g = witness
                gens = None
            elif len(witness) == 2:
                f, g = witness
                R = None
                gens = None
            else:
                return [False, False]
        else:
            return [False, False]
            
        if not isinstance(f, (sp.MatrixBase, sp.Poly)):
            f = sp.sympify(f)
        if not isinstance(g, (sp.MatrixBase, sp.Poly)):
            g = sp.sympify(g)
            
        if R is not None:
            if R == sp.S.Integers:
                R = sp.ZZ
            elif R == sp.S.Rationals:
                R = sp.QQ
            elif R == sp.S.Reals:
                R = sp.RR
            elif R == sp.S.Complexes:
                R = sp.CC
                
        if R is None:
            if isinstance(f, sp.MatrixBase):
                elements = list(f) + list(g)
            elif isinstance(f, (list, tuple)):
                elements = list(f) + list(g)
            else:
                elements = [f, g]
                
            elements = [sp.sympify(e) for e in elements]
            try:
                R, _ = construct_domain(elements)
            except Exception:
                R = sp.ZZ
                
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        def get_content(obj):
            if isinstance(obj, sp.MatrixBase):
                elements = list(obj)
                if not elements:
                    return sp.S.Zero
                c = elements[0]
                for e in elements[1:]:
                    c = sp.gcd(c, e)
                return c
            elif isinstance(obj, sp.Poly):
                return obj.content()
            else:
                try:
                    if gens is not None:
                        poly = sp.Poly(obj, *gens, domain=R)
                    else:
                        poly = sp.Poly(obj, domain=R)
                    return poly.content()
                except Exception:
                    return obj

        cf = get_content(f)
        cg = get_content(g)
        
        fg = f * g
        cfg = get_content(fg)
        
        prod = cf * cg
        
        def are_associate(a, b, domain):
            if a == b:
                return True
            if a == 0 or b == 0:
                return False
            if domain is not None and hasattr(domain, 'rem'):
                try:
                    a_d = domain.convert(a)
                    b_d = domain.convert(b)
                    return domain.rem(a_d, b_d) == domain.zero and domain.rem(b_d, a_d) == domain.zero
                except Exception:
                    pass
            try:
                rem1 = sp.rem(a, b)
                rem2 = sp.rem(b, a)
                return rem1 == 0 and rem2 == 0
            except Exception:
                return False

        q_holds = are_associate(cfg, prod, R)
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]