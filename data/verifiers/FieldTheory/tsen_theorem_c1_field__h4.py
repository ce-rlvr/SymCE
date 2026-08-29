import sympy
from sympy.abc import t, x, y, z, w, u, v
import itertools

def has_nontrivial_zero(f, vars, L_gen):
    if not vars:
        return False
        
    if sympy.expand(f) == 0:
        return True
        
    n = len(vars)
    
    # 1. Check if any variable can be solved directly as a rational function
    if n == 1:
        try:
            sols = sympy.solve(f, vars[0])
            for sol in sols:
                if sol != 0 and sol.is_rational_function(L_gen):
                    return True
        except Exception:
            pass
        return False

    # Dehomogenize and solve
    for i, v_i in enumerate(vars):
        f_dehom = f.subs(v_i, 1)
        rem_vars = vars[:i] + vars[i+1:]
        try:
            sols = sympy.solve(f_dehom, rem_vars, dict=True)
            for sol in sols:
                free_syms = set()
                for rv in rem_vars:
                    val = sol.get(rv, rv)
                    if hasattr(val, 'free_symbols'):
                        free_syms.update(val.free_symbols)
                free_syms -= {L_gen}
                
                if not free_syms:
                    if all(sol.get(rv, rv).is_rational_function(L_gen) for rv in rem_vars):
                        return True
                else:
                    # Test a few simple substitutions for free variables
                    test_vals = [0, 1, -1, sympy.I, -sympy.I, L_gen, -L_gen, sympy.I*L_gen, -sympy.I*L_gen]
                    for pt in itertools.product(test_vals, repeat=len(free_syms)):
                        sub_dict = dict(zip(free_syms, pt))
                        valid = True
                        for rv in rem_vars:
                            val = sol.get(rv, rv).subs(sub_dict)
                            if not val.is_rational_function(L_gen):
                                valid = False
                                break
                        if valid:
                            return True
        except Exception:
            pass

    # 2. Bounded search for small polynomial solutions
    coeffs = [-1, 0, 1]
    polys = [c0 + c1*L_gen for c0 in coeffs for c1 in coeffs]
    
    if n <= 4:
        for pt in itertools.product(polys, repeat=n):
            if all(p == 0 for p in pt):
                continue
            try:
                val = f.subs(dict(zip(vars, pt)))
                if sympy.expand(val) == 0:
                    return True
            except Exception:
                pass
                
    return False

def conditions(witness):
    try:
        K = witness.get('K')
        L_gen = witness.get('L_gen')
        f = witness.get('f')
        vars = witness.get('vars')
        
        # H_1: K is an algebraically closed field
        h1 = (K in ('C', 'AlgebraicallyClosed') or K == sympy.S.Complexes)
        
        # H_2: L is a field extension of K of transcendence degree 1
        h2 = isinstance(L_gen, sympy.Symbol)
        
        # H_3: f is a homogeneous polynomial of degree d in n variables over L
        h3 = False
        if isinstance(vars, (list, tuple)) and len(vars) > 0 and all(isinstance(v, sympy.Symbol) for v in vars):
            free_syms = f.free_symbols
            if free_syms.issubset(set(vars) | {L_gen}):
                poly = sympy.Poly(f, *vars)
                if poly.is_homogeneous:
                    coeffs = poly.coeffs()
                    h3 = all(c.is_rational_function(L_gen) for c in coeffs)
                    
        # ¬Q: f has no non-trivial zero in L
        neg_q = False
        if h3:
            has_zero = has_nontrivial_zero(f, vars, L_gen)
            neg_q = not has_zero
            
    except Exception:
        h1 = h2 = h3 = neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: L is a field extension of K of transcendence degree 1",
    "H_3: f is a homogeneous polynomial of degree d in n variables over L",
    "¬Q: f has no non-trivial zero in L"
]

N_HYP = 3
NEG_Q_INDEX = 3