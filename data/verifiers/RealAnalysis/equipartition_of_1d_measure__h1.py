import sympy as sp
import math

# Top-level setup
x = sp.Symbol('x', real=True)
c = sp.Symbol('c', real=True)

CONDITION_LABELS = [
    "H_1: The improper integral \\int_{-\\infty}^\\infty f(x)dx converges to a positive real number L",
    "¬Q: There does NOT exist a real number c such that \\int_{-\\infty}^c f(x)dx = L/2"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1_ok = False
    neg_q_ok = False
    
    # Normalize the variable in the witness expression to our real symbol 'x'
    try:
        free_syms = witness.free_symbols
        if len(free_syms) == 1:
            sym = list(free_syms)[0]
            witness = witness.subs(sym, x)
        elif len(free_syms) > 1:
            for sym in free_syms:
                if sym.name == 'x':
                    witness = witness.subs(sym, x)
    except Exception:
        pass

    L_val = None
    try:
        # Check H_1: Integral over R converges to a positive real number L
        L_expr = sp.integrate(witness, (x, -sp.oo, sp.oo))
        L_c = complex(L_expr.evalf())
        if abs(L_c.imag) < 1e-7 and L_c.real > 0:
            h1_ok = True
            L_val = L_c.real
    except Exception:
        h1_ok = False
        
    if h1_ok and L_val is not None:
        target = L_val / 2.0
        try:
            # Check ¬Q: The integral from -oo to c never equals L/2
            F_expr = sp.integrate(witness, (x, -sp.oo, c))
            has_integral = F_expr.has(sp.Integral)
            
            # If Sympy couldn't evaluate the integral symbolically, use a smaller grid
            # because numerical integration via evalf() is slower.
            if has_integral:
                grid = [i/5.0 for i in range(-100, 101)]
            else:
                grid = [i/10.0 for i in range(-1000, 1001)]
                
            min_dist = float('inf')
            for c_val in grid:
                try:
                    if has_integral:
                        val_expr = F_expr.subs(c, c_val)
                        val = complex(val_expr.evalf())
                    else:
                        val = complex(F_expr.subs(c, c_val).evalf())
                        
                    dist = abs(val - target)
                    
                    # If we hit the target (or get very close), the conclusion holds, so ¬Q is False
                    if dist < 1e-2:
                        min_dist = dist
                        break
                        
                    if dist < min_dist:
                        min_dist = dist
                except Exception:
                    continue
                    
            # If the minimum distance to L/2 across the grid is strictly bounded away from 0,
            # it means the function skips L/2 (e.g. due to a jump from a DiracDelta or being complex-valued).
            if min_dist > 0.1:
                neg_q_ok = True
        except Exception:
            neg_q_ok = False
            
    return [h1_ok, neg_q_ok]