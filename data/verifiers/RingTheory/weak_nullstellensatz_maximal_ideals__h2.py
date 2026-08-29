import sympy
from sympy import groebner, Poly
from sympy.abc import x, y, z, t

# Top-level setup for witness expressions
CC = sympy.CC
QQ = sympy.QQ
ZZ = sympy.ZZ

CONDITION_LABELS = [
    "H_1: F is an algebraically closed field",
    "¬Q: I is not of the form <x_1 - a_1, ..., x_n - a_n>"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Witness can be (F, I_gens, vars) or just (I_gens, vars) with implicit F = CC
        if len(witness) == 3:
            F, I_gens, vars = witness
        elif len(witness) == 2:
            I_gens, vars = witness
            F = sympy.CC
        else:
            return [False, False]
    except Exception:
        return [False, False]
    
    # H_1: F is an algebraically closed field
    try:
        h1_ok = (F in ('CC', 'C', sympy.CC))
    except Exception:
        h1_ok = False
        
    # neg_Q: I is NOT of the form <x_1 - a_1, ..., x_n - a_n>
    try:
        if not vars or len(vars) < 1:
            neg_q_ok = False
        else:
            # Compute the reduced Groebner basis
            gb = groebner(I_gens, *vars)
            gb_polys = list(gb)
            
            is_form = True
            # For the ideal to be of the form <x_1 - a_1, ..., x_n - a_n>,
            # its reduced Groebner basis must have exactly n elements,
            # and each element must have a total degree of exactly 1.
            if len(gb_polys) != len(vars):
                is_form = False
            else:
                for p in gb_polys:
                    poly = Poly(p, *vars)
                    if poly.total_degree() != 1:
                        is_form = False
                        break
                        
            neg_q_ok = not is_form
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]