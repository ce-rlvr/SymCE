import sympy
from sympy import Symbol, Piecewise, S, EmptySet
from sympy.calculus.util import maximum, minimum
import z3

# Top-level setup for witness expressions
x = Symbol('x', real=True)

CONDITION_LABELS = [
    "H_1: There exists a real number M such that |f(x)| <= M for all x in R",
    "¬Q: f has no fixed points (for all c in R, f(c) != c)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1_ok = False
    neg_q_ok = False
    
    # 1. Try Z3 evaluation
    try:
        zx = z3.Real('x')
        if callable(witness):
            zfx = witness(zx)
        else:
            zfx = witness
            
        if isinstance(zfx, (int, float)) and not isinstance(zfx, bool):
            zfx = z3.RealVal(zfx)
            
        if z3.is_expr(zfx):
            # H1: Boundedness
            M = z3.Real('M')
            s1 = z3.Solver()
            s1.add(z3.ForAll(zx, z3.And(zfx <= M, zfx >= -M)))
            s1.set("timeout", 2000)
            if s1.check() == z3.sat:
                h1_ok = True
                
            # ¬Q: No fixed points
            c = z3.Real('c')
            if callable(witness):
                zfc = witness(c)
            else:
                zfc = z3.substitute(zfx, (zx, c))
                
            s2 = z3.Solver()
            s2.add(zfc == c)
            s2.set("timeout", 2000)
            if s2.check() == z3.unsat:
                neg_q_ok = True
    except Exception:
        pass

    # If Z3 successfully proved both, we can return early
    if h1_ok and neg_q_ok:
        return [True, True]
        
    # 2. Try SymPy evaluation for any remaining unproven conditions
    try:
        if callable(witness):
            fx = witness(x)
        else:
            fx = witness
            
        # H1: Boundedness
        if not h1_ok:
            try:
                max_val = maximum(fx, x, S.Reals)
                min_val = minimum(fx, x, S.Reals)
                if (max_val.is_real == True or max_val.is_bounded == True) and \
                   (min_val.is_real == True or min_val.is_bounded == True):
                    h1_ok = True
            except Exception:
                pass
                
        # ¬Q: No fixed points
        if not neg_q_ok:
            try:
                from sympy import solveset
                fps = solveset(fx - x, x, domain=S.Reals)
                if fps == EmptySet:
                    neg_q_ok = True
            except Exception:
                pass
                
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]