import math
from sympy import ZZ, QQ, Poly, Expr
from sympy.abc import x, y, z
try:
    from sympy import reduced
except ImportError:
    from sympy.polys.polytools import reduced

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: \\bar{e} is an idempotent element in R/I",
    "¬Q: There does not exist an idempotent element e in R such that e + I = \\bar{e}"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
        R, I_gen, e_bar = witness
    except Exception:
        return [False, False, False]
        
    # Try integer ring case (e.g., Z or Z/nZ)
    try:
        if R is ZZ or R == 0:
            n = 0
        elif isinstance(R, str):
            R_clean = R.strip().upper()
            if R_clean in ["Z", "ZZ"]:
                n = 0
            elif R_clean.startswith("Z/") and R_clean.endswith("Z"):
                n = abs(int(R_clean[2:-1]))
            elif R_clean.startswith("Z") and R_clean.endswith("Z"):
                n = abs(int(R_clean[1:-1]))
            else:
                n = abs(int(R))
        else:
            n = abs(int(R))
            
        I_gen_int = int(I_gen)
        e_bar_int = int(e_bar)
        
        h1 = True
        
        if n == 0:
            m = abs(I_gen_int)
        else:
            m = math.gcd(n, I_gen_int)
            
        if m == 0:
            h2 = ((e_bar_int * e_bar_int) == e_bar_int)
        else:
            h2 = ((e_bar_int * e_bar_int) % m == e_bar_int % m)
            
        idempotents = []
        if n == 0:
            idempotents = [0, 1]
        else:
            idempotents = [val for val in range(n) if (val * val) % n == val]
            
        lift_exists = False
        for e in idempotents:
            if m == 0:
                if e == e_bar_int:
                    lift_exists = True
                    break
            else:
                if e % m == e_bar_int % m:
                    lift_exists = True
                    break
                    
        neg_q = not lift_exists
        
        return [h1, h2, neg_q]
        
    except Exception:
        pass

    # Try polynomial ring case (e.g., QQ[x])
    try:
        if isinstance(e_bar, Poly):
            e_bar_expr = e_bar.as_expr()
        elif isinstance(e_bar, Expr):
            e_bar_expr = e_bar
        else:
            e_bar_expr = e_bar
            
        if isinstance(I_gen, (list, tuple)):
            I_gens = []
            for g in I_gen:
                if isinstance(g, Poly):
                    I_gens.append(g.as_expr())
                else:
                    I_gens.append(g)
        else:
            if isinstance(I_gen, Poly):
                I_gens = [I_gen.as_expr()]
            else:
                I_gens = [I_gen]
                
        h1 = True
        diff = e_bar_expr**2 - e_bar_expr
        
        _, remainder = reduced(diff, I_gens)
        h2 = (remainder == 0)
        
        lift_exists = False
        # In integral domains like QQ[x], the only idempotents are 0 and 1
        for e in [0, 1]:
            diff_e = e - e_bar_expr
            _, rem_e = reduced(diff_e, I_gens)
            if rem_e == 0:
                lift_exists = True
                break
                
        neg_q = not lift_exists
        return [h1, h2, neg_q]
    except Exception:
        pass

    return [False, False, False]