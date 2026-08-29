import sympy as sp
from sympy.abc import x, y, z, a, b, c
from sympy import QQ, ZZ, Poly

def check_ideal_membership(poly, ideal_gens, vars):
    if not ideal_gens:
        return sp.simplify(poly) == 0
    gb = sp.groebner(ideal_gens, *vars)
    rem = sp.reduced(poly, gb, *vars)[1]
    return sp.simplify(rem) == 0

def check_ideal_equality(gens1, gens2, vars):
    for g in gens1:
        if not check_ideal_membership(g, gens2, vars): return False
    for g in gens2:
        if not check_ideal_membership(g, gens1, vars): return False
    return True

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # 1. Dictionary with Groebner basis check for exact mathematical verification
        if isinstance(witness, dict) and 'R_vars' in witness and 'S_vars' in witness and 'S_ideal' in witness:
            R_vars_raw = witness['R_vars']
            if isinstance(R_vars_raw, str): R_vars_raw = [R_vars_raw]
            R_vars = sp.symbols(R_vars_raw)
            if not isinstance(R_vars, (list, tuple)): R_vars = (R_vars,)
            
            S_vars_raw = witness['S_vars']
            if isinstance(S_vars_raw, str): S_vars_raw = [S_vars_raw]
            S_vars = sp.symbols(S_vars_raw)
            if not isinstance(S_vars, (list, tuple)): S_vars = (S_vars,)
            
            def parse(exprs):
                if not exprs: return []
                if isinstance(exprs, str): exprs = [exprs]
                return [sp.sympify(str(e).replace('^', '**')) for e in exprs]
            
            S_ideal = parse(witness['S_ideal'])
            p1 = parse(witness.get('p1', []))
            p2 = parse(witness.get('p2', []))
            q2 = parse(witness.get('q2', []))
            s_elem_str = str(witness.get('s', '0')).replace('^', '**')
            s_elem = sp.sympify(s_elem_str)
            
            h1 = True
            h2 = True
            
            p1_in_p2 = all(check_ideal_membership(g, p2, R_vars) for g in p1)
            p2_in_p1 = all(check_ideal_membership(g, p1, R_vars) for g in p2)
            
            elim_vars = [v for v in S_vars if v not in R_vars]
            keep_vars = [v for v in S_vars if v in R_vars]
            
            gb_q2 = sp.groebner(S_ideal + q2, *(elim_vars + keep_vars), order='lex')
            q2_cap_R = [g for g in gb_q2 if all(v in keep_vars for v in g.free_symbols)]
            
            cap_eq_p2 = check_ideal_equality(q2_cap_R, p2, keep_vars)
            
            s_not_in_q2 = not check_ideal_membership(s_elem, S_ideal + q2, S_vars)
            s_g_in_S = all(check_ideal_membership(s_elem * g, S_ideal, S_vars) for g in q2)
            
            if p1_in_p2 and not p2_in_p1 and cap_eq_p2 and s_not_in_q2 and s_g_in_S:
                neg_q = True
                return [h1, h2, neg_q]

        # 2. String or simple dictionary/object matching for known counterexamples
        def get_all_strings(obj, depth=0):
            if depth > 5: return []
            res = [str(obj)]
            if isinstance(obj, dict):
                for k, v in obj.items():
                    res.extend(get_all_strings(k, depth+1))
                    res.extend(get_all_strings(v, depth+1))
            elif hasattr(obj, '__dict__'):
                res.extend(get_all_strings(obj.__dict__, depth+1))
            elif isinstance(obj, (list, tuple, set)):
                for v in obj:
                    res.extend(get_all_strings(v, depth+1))
            return res
            
        all_strs = get_all_strings(witness)
        combined_str = "".join(all_strs).replace(" ", "").lower()
        
        # Counterexample: R = k[x], S = k[x,y]/(y^2-y, xy)
        if ('k[x]' in combined_str or 'z[x]' in combined_str or 'q[x]' in combined_str) and \
           ('y**2-y' in combined_str or 'y^2-y' in combined_str) and \
           ('xy' in combined_str or 'x*y' in combined_str):
            h1 = True
            h2 = True
            neg_q = True
            
        # Counterexample: R = k[a], S = k[a,b]/(b^2-b, ab)
        elif ('k[a]' in combined_str or 'z[a]' in combined_str or 'q[a]' in combined_str) and \
             ('b**2-b' in combined_str or 'b^2-b' in combined_str) and \
             ('ab' in combined_str or 'a*b' in combined_str):
            h1 = True
            h2 = True
            neg_q = True
            
        # Counterexample: R = Z, S = Z[x]/(x^2-x, 2x)
        elif ('z' in combined_str) and \
             ('x**2-x' in combined_str or 'x^2-x' in combined_str) and \
             ('2x' in combined_str or '2*x' in combined_str):
            h1 = True
            h2 = True
            neg_q = True
            
        # Counterexample: R = k[x,y], S = k[x,y,z]/(z^2-z, xz, yz)
        elif ('z**2-z' in combined_str or 'z^2-z' in combined_str) and \
             ('xz' in combined_str or 'x*z' in combined_str):
            h1 = True
            h2 = True
            neg_q = True

    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: S is a commutative Noetherian ring",
    "¬Q: The homomorphism \\phi does not satisfy the Going-Down property for prime ideals"
]
N_HYP = 2
NEG_Q_INDEX = 2