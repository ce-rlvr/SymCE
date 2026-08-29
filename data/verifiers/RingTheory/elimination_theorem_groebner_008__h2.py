import sympy
from sympy import Poly, reduced, groebner, Expr, Symbol
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: I is an ideal in the polynomial ring",
    "H_2: l is an integer between 0 and n",
    "not Q: G intersection with the elimination ring is NOT a Groebner basis"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            I_gens = witness.get('I', [])
            G = witness.get('G', [])
            l = witness.get('l', 0)
            vars = witness.get('vars', [])
        else:
            I_gens, G, l, vars = witness
    except Exception:
        return [False, False, False]

    # H1: I is an ideal in k[vars]
    try:
        h1 = isinstance(I_gens, (list, tuple)) and isinstance(vars, (list, tuple))
        if h1:
            vars_set = set(vars)
            h1 = all(isinstance(v, Symbol) for v in vars)
            if h1:
                for p in I_gens:
                    if isinstance(p, (int, float)):
                        continue
                    if hasattr(p, 'free_symbols'):
                        if not p.free_symbols.issubset(vars_set):
                            h1 = False
                            break
                    else:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: 0 <= l <= n
    try:
        n = len(vars)
        h2 = isinstance(l, int) and 0 <= l <= n
    except Exception:
        h2 = False

    # neg_Q: G \cap k[x_{l+1}..] is NOT a Gröbner basis of I \cap k[x_{l+1}..]
    try:
        if not isinstance(G, (list, tuple, set)):
            neg_q = False
        else:
            elim_vars = vars[l:]
            elim_vars_set = set(elim_vars)
            
            # Compute the true elimination ideal Gröbner basis
            if not I_gens:
                GB = []
            else:
                if not vars:
                    GB = I_gens
                else:
                    GB = groebner(I_gens, *vars, order='lex')
                    
            true_elim_GB = []
            for p in GB:
                if p == 0: 
                    continue
                if hasattr(p, 'free_symbols'):
                    if p.free_symbols.issubset(elim_vars_set):
                        true_elim_GB.append(p)
                elif isinstance(p, (int, float)):
                    true_elim_GB.append(p)
                    
            # Compute G \cap k[x_{l+1}..]
            G_elim = []
            for g in G:
                if g == 0: 
                    continue
                if hasattr(g, 'free_symbols'):
                    if g.free_symbols.issubset(elim_vars_set):
                        G_elim.append(g)
                elif isinstance(g, (int, float)):
                    G_elim.append(g)
                    
            is_GB = True
            if not elim_vars:
                # If there are no elimination variables, the ideal is in the base field k
                true_ideal_is_one = len(true_elim_GB) > 0
                G_ideal_is_one = len(G_elim) > 0
                G_subset_of_true = not G_ideal_is_one or true_ideal_is_one
                generates_true = (true_ideal_is_one == G_ideal_is_one)
                is_GB = G_subset_of_true and generates_true
            else:
                # 1. Check if G_elim is a subset of the elimination ideal
                for g in G_elim:
                    if not true_elim_GB:
                        is_GB = False
                        break
                    rem = reduced(g, true_elim_GB, *elim_vars, order='lex')[1]
                    if rem != 0:
                        is_GB = False
                        break
                
                # 2. Check if the leading terms of G_elim generate the initial ideal
                if is_GB:
                    for t in true_elim_GB:
                        t_poly = Poly(t, *elim_vars, order='lex')
                        t_LM = t_poly.monoms()[0]
                        
                        divisible = False
                        for g in G_elim:
                            g_poly = Poly(g, *elim_vars, order='lex')
                            g_LM = g_poly.monoms()[0]
                            
                            # Check if g_LM divides t_LM
                            if all(te >= ge for te, ge in zip(t_LM, g_LM)):
                                divisible = True
                                break
                        if not divisible:
                            is_GB = False
                            break
                            
            neg_q = not is_GB
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]