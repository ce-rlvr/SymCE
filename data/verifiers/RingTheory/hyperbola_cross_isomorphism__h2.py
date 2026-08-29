import sympy
from sympy import symbols
from sympy.polys.domains import QQ, ZZ, GF, RR, CC
from sympy.abc import x, y, u, v, z, w

CONDITION_LABELS = [
    "H_1: F is a field of characteristic not equal to 2",
    "H_2: I is the principal ideal (x^2 - y^2) in R",
    "¬Q: R/I is not isomorphic to S/(uv)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            F = witness.get('F')
            R = witness.get('R')
            S = witness.get('S')
            I = witness.get('I')
        elif isinstance(witness, (list, tuple)) and len(witness) == 4:
            F, R, S, I = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: F is a field of characteristic not equal to 2
    try:
        if isinstance(F, str):
            if any(d in F for d in ['QQ', 'RR', 'CC', 'Rational', 'Real', 'Complex']):
                h1 = True
            elif 'GF' in F and '2' not in F:
                h1 = True
        elif hasattr(F, 'is_Field') and F.is_Field:
            if hasattr(F, 'characteristic'):
                char = F.characteristic()
            elif hasattr(F, 'char'):
                char = F.char
            else:
                char = 0
            if char != 2:
                h1 = True
    except Exception:
        pass

    # H2: I is the principal ideal (x^2 - y^2) in R
    try:
        if isinstance(R, str):
            if 'x' in R and 'y' in R:
                I_str = str(I).replace(' ', '')
                if I_str in ['(x**2-y**2)', 'x**2-y**2', '[x**2-y**2]', 'x^2-y^2', '(x^2-y^2)']:
                    h2 = True
        elif hasattr(R, 'gens'):
            r_gens_str = [str(g) for g in R.gens]
            if 'x' in r_gens_str and 'y' in r_gens_str:
                x_idx = r_gens_str.index('x')
                y_idx = r_gens_str.index('y')
                R_x = R.gens[x_idx]
                R_y = R.gens[y_idx]
                target_I = R_x**2 - R_y**2
                
                if isinstance(I, str):
                    I_str = I.replace(' ', '')
                    if I_str in ['(x**2-y**2)', 'x**2-y**2', '[x**2-y**2]', 'x^2-y^2', '(x^2-y^2)']:
                        h2 = True
                elif isinstance(I, (list, tuple, set)):
                    I_list = list(I)
                    if len(I_list) == 1:
                        gen = I_list[0]
                        if gen == target_I or str(gen) == str(target_I) or str(gen).replace(' ', '') in ['x**2-y**2', 'x^2-y**2']:
                            h2 = True
                else:
                    if I == target_I or str(I) == str(target_I) or str(I).replace(' ', '') in ['x**2-y**2', 'x^2-y**2']:
                        h2 = True
    except Exception:
        pass

    # neg_Q: R/I is not isomorphic to S/(uv)
    try:
        if isinstance(R, str) and isinstance(S, str):
            r_domain = R.split('[')[0] if '[' in R else R
            s_domain = S.split('[')[0] if '[' in S else S
            
            r_vars_str = R.split('[')[1].split(']')[0] if '[' in R else ""
            s_vars_str = S.split('[')[1].split(']')[0] if '[' in S else ""
            
            r_gens = [v.strip() for v in r_vars_str.split(',')] if r_vars_str else []
            s_gens = [v.strip() for v in s_vars_str.split(',')] if s_vars_str else []
            
            if r_domain != s_domain:
                neg_q = True
            elif len(r_gens) != len(s_gens):
                neg_q = True
            elif 'u' not in s_gens or 'v' not in s_gens:
                neg_q = True
            else:
                neg_q = False
        elif not hasattr(S, 'gens') or not hasattr(R, 'gens'):
            neg_q = True
        else:
            s_gens_str = [str(g) for g in S.gens]
            if getattr(R, 'domain', None) != getattr(S, 'domain', None):
                neg_q = True
            elif len(R.gens) != len(S.gens):
                neg_q = True
            elif 'u' not in s_gens_str or 'v' not in s_gens_str:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]