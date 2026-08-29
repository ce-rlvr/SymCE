import sympy
from sympy import Poly, ZZ, QQ
from sympy.abc import x, y, z

# Top-level setup
Z2 = sympy.polys.domains.GF(2)
Z3 = sympy.polys.domains.GF(3)
Z5 = sympy.polys.domains.GF(5)

def conditions(witness):
    f = None
    domain = None
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            dom, expr = witness
            f = Poly(expr, domain=dom)
            domain = f.domain
        elif isinstance(witness, Poly):
            f = witness
            domain = f.domain
        else:
            f = Poly(witness)
            domain = f.domain
    except Exception:
        pass

    # H1: R is an integral domain
    h1_ok = False
    try:
        if domain is not None:
            if getattr(domain, 'is_Field', False):
                h1_ok = True
            elif domain == ZZ:
                h1_ok = True
            elif hasattr(domain, 'is_Poly') and domain.is_Poly:
                h1_ok = True
            elif hasattr(domain, 'is_FractionField') and domain.is_FractionField:
                h1_ok = True
    except Exception:
        pass

    # H2: f is a polynomial over R
    h2_ok = False
    try:
        if f is not None and isinstance(f, Poly):
            if len(f.gens) == 1:
                h2_ok = True
    except Exception:
        pass

    # neg_Q: f is NOT a constant polynomial OR its constant term is NOT a unit in R
    neg_q_ok = False
    try:
        if f is not None and domain is not None:
            is_const = False
            try:
                is_const = f.is_constant()
            except Exception:
                try:
                    is_const = (f.degree() <= 0)
                except Exception:
                    pass
            
            if not is_const:
                neg_q_ok = True
            else:
                c = f.TC()
                is_unit = False
                if c == domain.zero:
                    is_unit = False
                else:
                    if domain == ZZ:
                        is_unit = (c in [domain.one, -domain.one])
                    elif getattr(domain, 'is_Field', False):
                        is_unit = (c != domain.zero)
                    else:
                        try:
                            q = domain.exquo(domain.one, c)
                            if q * c == domain.one:
                                is_unit = True
                        except Exception:
                            try:
                                q = domain.quo(domain.one, c)
                                if q * c == domain.one:
                                    is_unit = True
                            except Exception:
                                pass
                
                if not is_unit:
                    neg_q_ok = True
    except Exception:
        pass

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: f is a polynomial over R",
    "¬Q: f is not a constant polynomial or its constant term is not a unit in R"
]

N_HYP = 2
NEG_Q_INDEX = 2