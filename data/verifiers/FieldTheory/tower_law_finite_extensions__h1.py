import sympy
from sympy import oo
import math

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            deg_M_L = witness.get('deg_M_L')
            deg_L_K = witness.get('deg_L_K')
            deg_M_K = witness.get('deg_M_K')
        elif hasattr(witness, 'deg_M_L'):
            deg_M_L = witness.deg_M_L
            deg_L_K = witness.deg_L_K
            deg_M_K = witness.deg_M_K
        else:
            deg_M_L, deg_L_K, deg_M_K = witness
            
        def parse_deg(deg):
            if isinstance(deg, str):
                if deg.lower() in ('oo', 'inf', 'infinity'):
                    return oo
                try:
                    return int(deg)
                except Exception:
                    pass
            return deg

        deg_M_L = parse_deg(deg_M_L)
        deg_L_K = parse_deg(deg_L_K)
        deg_M_K = parse_deg(deg_M_K)

        def is_valid_deg(d):
            if d in (oo, float('inf'), math.inf):
                return True
            try:
                return int(d) >= 1 and int(d) == d
            except Exception:
                return False

        def is_realizable(a, b, c):
            if not (is_valid_deg(a) and is_valid_deg(b) and is_valid_deg(c)):
                return False
            inf_vals = (oo, float('inf'), math.inf)
            if a in inf_vals or b in inf_vals:
                return c in inf_vals
            return c == a * b

        def is_finite(deg):
            if not is_valid_deg(deg):
                return False
            return deg not in (oo, float('inf'), math.inf)

        try:
            h1 = is_finite(deg_M_L) and is_realizable(deg_M_L, deg_L_K, deg_M_K)
        except Exception:
            h1 = False
        
        try:
            finite_M_K = is_finite(deg_M_K)
            
            if deg_M_L == 0 or deg_L_K == 0:
                prod = 0
            elif deg_M_L in (oo, float('inf'), math.inf) or deg_L_K in (oo, float('inf'), math.inf):
                prod = oo
            else:
                prod = deg_M_L * deg_L_K
                
            if deg_M_K in (float('inf'), math.inf):
                deg_M_K_val = oo
            else:
                deg_M_K_val = deg_M_K
                
            q = finite_M_K and (deg_M_K_val == prod)
            neg_q = not q
        except Exception:
            neg_q = False
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: M is a finite field extension of L", "¬Q: M is not a finite extension of K, or degree of M over K is not the product of degrees"]
N_HYP = 1
NEG_Q_INDEX = 1