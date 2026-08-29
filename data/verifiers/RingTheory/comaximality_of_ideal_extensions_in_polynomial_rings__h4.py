import sympy
from sympy import sympify, Expr, gcd
from sympy.polys import groebner
from functools import reduce

x, y, z = sympy.symbols('x y z')

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: The ring is a polynomial ring over R",
    "H_3: I and J are ideals of R",
    "¬Q: The extended ideals are not comaximal"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        
        I_gens, J_gens = witness
        
        if not isinstance(I_gens, (list, tuple, set)):
            I_gens = [I_gens]
        if not isinstance(J_gens, (list, tuple, set)):
            J_gens = [J_gens]
            
        def is_valid_elem(e):
            try:
                e = sympify(e)
                if getattr(e, 'is_Matrix', False):
                    return False
                if e.has(sympy.Float):
                    return False
                return e.is_Integer or isinstance(e, Expr)
            except Exception:
                return False
                
        if not all(is_valid_elem(e) for e in I_gens):
            return [False, False, False, False]
        if not all(is_valid_elem(e) for e in J_gens):
            return [False, False, False, False]
            
        h1 = True
        h2 = True
        h3 = True
        
        all_gens = [sympify(e) for e in I_gens] + [sympify(e) for e in J_gens]
        
        if not all_gens:
            is_comaximal = False
        elif all(e.is_Integer for e in all_gens):
            overall_gcd = reduce(gcd, all_gens)
            is_comaximal = (abs(overall_gcd) == 1)
        else:
            free_syms = set()
            for e in all_gens:
                free_syms.update(e.free_symbols)
                
            if not free_syms:
                overall_gcd = reduce(gcd, all_gens)
                is_comaximal = (overall_gcd != 0 and overall_gcd.is_constant())
            else:
                gb = groebner(all_gens, *free_syms)
                is_comaximal = (len(gb) == 1 and gb[0].is_constant() and gb[0] != 0)
                
        neg_q = not is_comaximal
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]