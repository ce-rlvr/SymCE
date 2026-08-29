import sympy
from sympy import symbols

x, y, z, t, u, v, w = symbols('x y z t u v w')

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: A is a finitely generated commutative K-algebra",
    "¬Q: A is not isomorphic to the coordinate ring of any affine algebraic set"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            field, gens, ideal = witness
        elif isinstance(witness, tuple) and len(witness) == 2:
            field = 'CC'
            gens, ideal = witness
        elif isinstance(witness, list):
            field = 'CC'
            ideal = witness
            gens = list(set().union(*(p.free_symbols for p in ideal if hasattr(p, 'free_symbols'))))
        else:
            field = 'CC'
            ideal = [witness]
            gens = list(witness.free_symbols) if hasattr(witness, 'free_symbols') else []
            
        if str(field) in ['CC', 'C', 'AlgebraicClosure', 'EX']:
            h1 = True
            
        if isinstance(gens, list) and isinstance(ideal, list):
            h2 = True
            
        if h2 and len(ideal) > 0 and len(gens) > 0:
            gb = sympy.groebner(ideal, *gens)
            gb_list = list(gb)
            
            if len(gb_list) == 1 and gb_list[0] == 1:
                neg_q = False
            else:
                for p in ideal:
                    sqf = sympy.sqf_part(p)
                    rem = sympy.reduced(sqf, gb_list, *gens)[1]
                    if rem != 0:
                        neg_q = True
                        break
                        
                if not neg_q:
                    for p in gb_list:
                        p_poly = sympy.Poly(p, *gens)
                        active_vars = [var for var in gens if p_poly.degree(var) > 0]
                        if len(active_vars) == 1:
                            v_var = active_vars[0]
                            f = sympy.Poly(p, v_var)
                            sqf = sympy.sqf_part(f)
                            if sqf.degree() < f.degree():
                                rem = sympy.reduced(sqf.as_expr(), gb_list, *gens)[1]
                                if rem != 0:
                                    neg_q = True
                                    break
    except Exception:
        pass
        
    return [h1, h2, neg_q]