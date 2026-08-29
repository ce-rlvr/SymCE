import sympy
from sympy import Poly, ZZ, QQ, Rational, Integer
from sympy.abc import x, y, z

# Top-level setup
# (No specific named objects required for RingTheory beyond standard symbols)

def conditions(witness) -> list[bool]:
    try:
        f, a = witness
    except Exception:
        return [False, False, False]
    
    # H1: f is a non-zero polynomial
    try:
        if not isinstance(f, Poly):
            f_poly = Poly(f)
        else:
            f_poly = f
        h1 = not f_poly.is_zero
    except Exception:
        h1 = False

    # H2: a is a non-zero element of R
    try:
        domain = f_poly.domain
        if isinstance(a, Poly):
            if a.domain != domain:
                h2 = False
            elif not a.is_ground:
                h2 = False
            else:
                h2 = not a.is_zero
        else:
            try:
                val = domain.from_sympy(sympy.sympify(a))
                if hasattr(domain, 'm'):
                    h2 = (int(val) % domain.m) != 0
                else:
                    h2 = val != domain.zero
            except Exception:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: primitive part of a*f is NOT associate to primitive part of f
    try:
        domain = f_poly.domain
        if isinstance(a, Poly):
            val = a.coeffs()[0]
        else:
            val = domain.from_sympy(sympy.sympify(a))
            
        af = f_poly.mul_ground(val)
        
        def get_primitive(p):
            dom = p.domain
            if hasattr(dom, 'm'):
                m = dom.m
                if p.is_zero:
                    return p
                from sympy import gcd
                from functools import reduce
                ints = [int(c) for c in p.coeffs()]
                c = reduce(gcd, ints + [m])
                prim_ints = [i // c for i in ints]
                return Poly(dict(zip(p.monoms(), prim_ints)), *p.gens, domain=dom)
            else:
                return p.primitive()[1]
                
        prim_f = get_primitive(f_poly)
        prim_af = get_primitive(af)
        
        def are_associate(p1, p2):
            if p1.is_zero and p2.is_zero: return True
            if p1.is_zero or p2.is_zero: return False
            dom = p1.domain
            if hasattr(dom, 'm'):
                m = dom.m
                from sympy import gcd
                units = [u for u in range(1, m) if gcd(u, m) == 1]
                for u in units:
                    if p1 == p2 * u:
                        return True
                return False
            else:
                try:
                    q1 = p1.exquo(p2)
                    q2 = p2.exquo(p1)
                    return q1.is_ground and q2.is_ground
                except Exception:
                    return p1 == p2 or p1 == -p2
                    
        neg_q = not are_associate(prim_f, prim_af)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: f is a non-zero polynomial",
    "H_2: a is a non-zero element",
    "¬Q: The primitive part of a*f is not associate to the primitive part of f"
]

N_HYP = 2
NEG_Q_INDEX = 2