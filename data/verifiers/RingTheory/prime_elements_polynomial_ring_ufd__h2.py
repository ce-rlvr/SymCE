import sympy
from sympy import Poly, sympify, factor_list
from sympy import ZZ, QQ
from sympy.ntheory import factorint
from sympy.abc import x, y, z

def conditions(witness):
    try:
        if isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                R, p, gen = witness
                if isinstance(R, str):
                    if R == 'ZZ': R = ZZ
                    elif R == 'QQ': R = QQ
                p = sympify(p)
                gen = sympify(gen)
            elif len(witness) == 2:
                R, p = witness
                if isinstance(R, str):
                    if R == 'ZZ': R = ZZ
                    elif R == 'QQ': R = QQ
                p = sympify(p)
                free = p.free_symbols if hasattr(p, 'free_symbols') else set()
                gen = list(free)[0] if free else x
            else:
                return [False, False, False]
        else:
            R = ZZ
            p = sympify(witness)
            free = p.free_symbols if hasattr(p, 'free_symbols') else set()
            gen = list(free)[0] if free else x
    except Exception:
        return [False, False, False]

    try:
        h1 = bool(R.is_UFD)
    except Exception:
        h1 = False

    try:
        poly = Poly(p, gen, domain=R)
        h2 = True
    except Exception:
        h2 = False

    try:
        is_prime = False
        if poly.is_zero:
            is_prime = False
        else:
            is_unit = False
            if poly.degree() == 0:
                c = poly.as_expr()
                try:
                    if R.is_unit(R.from_sympy(c)):
                        is_unit = True
                except Exception:
                    pass
            
            if is_unit:
                is_prime = False
            else:
                coeff, factors = factor_list(p, gen, domain=R)
                num_factors = 0
                
                c_dom = R.from_sympy(coeff)
                if not R.is_unit(c_dom):
                    if hasattr(coeff, 'is_Integer') and coeff.is_Integer:
                        num_factors += sum(factorint(abs(int(coeff))).values())
                    else:
                        try:
                            c_coeff, c_factors = factor_list(coeff)
                            if hasattr(c_coeff, 'is_Integer') and c_coeff.is_Integer and abs(int(c_coeff)) > 1:
                                num_factors += sum(factorint(abs(int(c_coeff))).values())
                            for cb, ce in c_factors:
                                num_factors += ce
                        except Exception:
                            num_factors += 1
                
                for base, exp in factors:
                    num_factors += exp
                    
                is_prime = (num_factors == 1)
                
        neg_q = not is_prime
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain",
    "H_2: The ring is the polynomial ring over R",
    "\u00acQ: p is not a prime element in the polynomial ring"
]

N_HYP = 2
NEG_Q_INDEX = 2