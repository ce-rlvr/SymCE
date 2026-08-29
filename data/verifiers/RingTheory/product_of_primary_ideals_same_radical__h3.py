import sympy
from sympy import solve
from sympy.polys.polytools import groebner, reduced
from sympy.abc import x, y, z, t

# Top-level setup
# We provide x, y, z, t for polynomial rings over QQ.
# The witness is expected to provide generators for M, Q1, Q2.

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            M_gens = witness.get('M', [])
            Q1_gens = witness.get('Q1', [])
            Q2_gens = witness.get('Q2', [])
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                M_gens, Q1_gens, Q2_gens = witness
            elif len(witness) >= 4:
                M_gens, Q1_gens, Q2_gens = witness[-3:]
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        M_gens = list(M_gens)
        Q1_gens = list(Q1_gens)
        Q2_gens = list(Q2_gens)
        
        vars_set = set()
        for p in M_gens + Q1_gens + Q2_gens:
            if isinstance(p, sympy.Expr):
                vars_set.update(p.free_symbols)
        vars = sorted(list(vars_set), key=lambda v: v.name)
        
        if not vars:
            return [False, False, False]
            
    except Exception:
        return [False, False, False]

    # H1: R is a commutative Noetherian ring
    # We evaluate in QQ[vars], which is always a commutative Noetherian ring.
    h1_ok = True
    
    # H2: M is a maximal ideal of R
    h2_ok = False
    try:
        gb_M = groebner(M_gens, *vars, domain='QQ')
        roots = solve(gb_M, vars, dict=True)
        if len(roots) == 1:
            root = roots[0]
            is_rat = True
            for v in vars:
                if v not in root or not root[v].is_Rational:
                    is_rat = False
                    break
            if is_rat and len(gb_M) == len(vars):
                deg_ok = True
                for p in gb_M:
                    if p.as_poly(*vars).total_degree() != 1:
                        deg_ok = False
                        break
                if deg_ok:
                    h2_ok = True
    except Exception:
        h2_ok = False
        
    # ¬Q: Q1 * Q2 is NOT an M-primary ideal
    neg_q_ok = False
    try:
        I_gens = [f * g for f in Q1_gens for g in Q2_gens]
        
        is_primary = False
        gb_M = groebner(M_gens, *vars, domain='QQ')
        roots = solve(gb_M, vars, dict=True)
        if len(roots) == 1:
            root = roots[0]
            subset_M = True
            for g in I_gens:
                if g.subs(root) != 0:
                    subset_M = False
                    break
            
            if subset_M:
                gb_I = groebner(I_gens, *vars, domain='QQ')
                rad_contains_M = True
                for v in vars:
                    c = root.get(v, 0)
                    poly = v - c
                    found = False
                    for k in range(1, 15):
                        if reduced(poly**k, gb_I, *vars, domain='QQ')[1] == 0:
                            found = True
                            break
                    if not found:
                        rad_contains_M = False
                        break
                if rad_contains_M:
                    is_primary = True
                    
        neg_q_ok = not is_primary
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: M is a maximal ideal of R",
    "¬Q: The product ideal Q_1 Q_2 is not an M-primary ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2