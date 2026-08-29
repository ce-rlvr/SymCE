import sympy
from sympy import Poly
from sympy.abc import x, y, z

ZZ = sympy.ZZ
QQ = sympy.QQ
RR = sympy.RR
CC = sympy.CC

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: f is a polynomial over R",
    "not Q: f is irreducible iff shifted f is irreducible fails"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                domain, f, c = witness
                free = getattr(f, 'free_symbols', set())
                var = list(free)[0] if free else sympy.Symbol('x')
            elif len(witness) == 4:
                domain, f, c, var = witness
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            domain = witness.get('domain')
            f = witness.get('f')
            c = witness.get('c')
            if 'x' in witness:
                var = witness['x']
            else:
                free = getattr(f, 'free_symbols', set())
                var = list(free)[0] if free else sympy.Symbol('x')
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    try:
        is_id = False
        if domain in [sympy.ZZ, sympy.QQ, sympy.RR, sympy.CC]:
            is_id = True
        elif hasattr(domain, 'is_IntegralDomain') and domain.is_IntegralDomain:
            is_id = True
        elif hasattr(domain, 'is_Field') and domain.is_Field:
            is_id = True
        elif hasattr(domain, 'is_PID') and domain.is_PID:
            is_id = True
        elif hasattr(domain, 'is_UFD') and domain.is_UFD:
            is_id = True
        h1_ok = is_id
    except Exception:
        h1_ok = False

    try:
        poly_f = Poly(f, var, domain=domain)
        h2_ok = True
    except Exception:
        h2_ok = False

    try:
        def is_irred(expr):
            try:
                p = Poly(expr, var, domain=domain)
                res = p.is_irreducible
                if res is not None:
                    return res
                
                cont, factors = sympy.factor_list(expr, var, domain=domain)
                num_factors = 0
                if domain == sympy.ZZ:
                    cont_val = abs(int(cont))
                    if cont_val == 0: 
                        return False
                    if cont_val > 1:
                        from sympy.ntheory import factorint
                        num_factors += sum(factorint(cont_val).values())
                elif hasattr(domain, 'is_Field') and domain.is_Field:
                    if expr == 0: 
                        return False
                for fac, exp in factors:
                    num_factors += exp
                return num_factors == 1
            except Exception:
                return False

        irred_f = is_irred(f)
        
        if hasattr(f, 'subs'):
            f_c = f.subs(var, var + c).expand()
        else:
            f_c = f
            
        irred_fc = is_irred(f_c)
        
        equiv = (irred_f == irred_fc)
        neg_q_ok = not equiv
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]