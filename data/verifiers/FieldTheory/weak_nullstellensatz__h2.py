import sympy
from sympy import CC, symbols

# Top-level setup for potential witness expressions
x, y, z = symbols('x y z')

def conditions(witness) -> list[bool]:
    # H_1: K is an algebraically closed field
    try:
        K = witness['K']
        # In SymPy, CC is the standard algebraically closed field
        h1_ok = (K == CC)
    except Exception:
        h1_ok = False

    # H_2: M is a maximal ideal of R
    try:
        R = witness['R']
        M_gens = witness['M_gens']
        vars = witness['vars']
        
        h2_ok = False
        if getattr(R, 'is_Field', False):
            # In a field, the only maximal ideal is the zero ideal (0)
            h2_ok = all(g == R.zero for g in M_gens)
        elif getattr(R, 'is_Poly', False) or hasattr(R, 'domain'):
            # In a polynomial ring over CC, an ideal is maximal iff it is of the form (x_1 - a_1, ..., x_n - a_n)
            from sympy import groebner
            gb = groebner(M_gens, vars).polys
            if len(gb) == len(vars):
                h2_ok = True
                for p, v in zip(gb, vars):
                    if p.degree(v) != 1:
                        h2_ok = False
                        break
                    if any(p.degree(u) > 0 for u in vars if u != v):
                        h2_ok = False
                        break
    except Exception:
        h2_ok = False

    # ¬Q: M is not of the form (x_1 - a_1, ..., x_n - a_n) for any a_i in K
    try:
        R = witness['R']
        M_gens = witness['M_gens']
        vars = witness['vars']
        
        neg_q_ok = False
        if hasattr(R, 'gens') and len(vars) > 0:
            if getattr(R, 'is_Field', False):
                # In a fraction field, x_i are transcendental, so x_i - a_i != 0.
                # Thus (x_1 - a_1, ...) is the whole ring (1).
                # If M is (0), then M != (1), so it is never of the form (x_1 - a_1, ...).
                is_zero = all(g == R.zero for g in M_gens)
                if is_zero:
                    neg_q_ok = True
            elif getattr(R, 'is_Poly', False) or hasattr(R, 'domain'):
                from sympy import groebner
                gb = groebner(M_gens, vars).polys
                if len(gb) != len(vars):
                    neg_q_ok = True
                else:
                    is_form = True
                    for p, v in zip(gb, vars):
                        if p.degree(v) != 1:
                            is_form = False
                            break
                        if any(p.degree(u) > 0 for u in vars if u != v):
                            is_form = False
                            break
                    neg_q_ok = not is_form
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: K is an algebraically closed field",
    "H_2: M is a maximal ideal of R",
    "¬Q: M is not of the form (x_1 - a_1, ..., x_n - a_n) for any a_i in K"
]

N_HYP = 2
NEG_Q_INDEX = 2