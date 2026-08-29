import sympy
from sympy import symbols, Poly, QQ

x, y, z = symbols('x y z')

def flatten(lst):
    res = []
    for item in lst:
        if isinstance(item, (list, tuple, set)):
            res.extend(flatten(item))
        else:
            res.append(item)
    return res

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            if 'gens' in witness:
                witness = witness['gens']
            elif 'polys' in witness:
                witness = witness['polys']
            elif 'I' in witness:
                witness = witness['I']
            else:
                witness = list(witness.values())
                
        if hasattr(witness, 'gens'):
            witness = witness.gens
            
        if isinstance(witness, (list, tuple, set)):
            witness = flatten(witness)
            cleaned = []
            for p in witness:
                if p in [sympy.QQ, sympy.RR, sympy.CC, sympy.ZZ]:
                    continue
                if isinstance(p, str) and p in ['QQ', 'RR', 'CC', 'ZZ']:
                    continue
                cleaned.append(p)
            exprs = [sympy.sympify(p) for p in cleaned]
        else:
            exprs = [sympy.sympify(witness)]
            
        if not exprs:
            return [False, False]
            
        vars_used = set()
        for expr in exprs:
            if hasattr(expr, 'free_symbols'):
                vars_used.update(expr.free_symbols)
                
        if len(vars_used) > 1:
            return [True, False]
            
        if len(vars_used) == 1:
            v = list(vars_used)[0]
        else:
            v = x
            
        polys = [Poly(p, v, domain=QQ) for p in exprs]
        h1_ok = True
    except Exception:
        return [False, False]
        
    try:
        g = polys[0]
        for p in polys[1:]:
            g = g.gcd(p)
            
        if g.is_zero:
            neg_q_ok = False
            return [h1_ok, neg_q_ok]
            
        rad_g = g.sqf_part()
        
        rational_roots = g.ground_roots()
        
        iv_g = Poly(1, v, domain=QQ)
        for r in rational_roots.keys():
            iv_g = iv_g * Poly(v - r, v, domain=QQ)
            
        iv_g_monic = iv_g.monic()
        rad_g_monic = rad_g.monic()
        
        neg_q_ok = bool(iv_g_monic != rad_g_monic)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = ["H_1: I is an ideal in the polynomial ring", "¬Q: I(V(I)) != rad(I)"]
N_HYP = 1
NEG_Q_INDEX = 1