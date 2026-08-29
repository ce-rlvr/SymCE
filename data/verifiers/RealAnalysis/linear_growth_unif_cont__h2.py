import sympy
import math

# Top-level setup
x = sympy.Symbol('x', real=True)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a sympy expression representing a function f(x).
    """
    # Determine the variable used in the witness expression
    try:
        free_symbols = list(witness.free_symbols)
        if len(free_symbols) == 1:
            sym = free_symbols[0]
        elif len(free_symbols) == 0:
            sym = x
        else:
            sym = next((s for s in free_symbols if s.name == 'x'), free_symbols[0])
    except Exception:
        sym = x

    # H_1: f is a real-valued function defined on R
    h1_ok = False
    try:
        # Check evaluation at several test points
        test_points = [0, 1, -1, 2.5, -2.5, math.pi, -math.e, 10, -10, 100, -100]
        h1_ok = True
        for p in test_points:
            val_expr = witness.subs(sym, p).evalf()
            
            # Check for undefined values
            if val_expr.has(sympy.nan) or val_expr.has(sympy.zoo) or val_expr.has(sympy.oo) or val_expr.has(-sympy.oo):
                h1_ok = False
                break
            
            # Check for imaginary parts (e.g., from branch cuts)
            im_part = sympy.im(val_expr)
            if im_part != 0:
                try:
                    if abs(float(im_part)) > 1e-9:
                        h1_ok = False
                        break
                except Exception:
                    # If conversion to float overflows, it's a huge imaginary part
                    h1_ok = False
                    break
                    
        # Check for formal singularities (poles, essential singularities)
        if h1_ok:
            try:
                sings = sympy.singularities(witness, sym)
                if sings.is_empty is False:
                    h1_ok = False
            except Exception:
                pass
    except Exception:
        h1_ok = False

    # neg_Q: f does not have linear growth
    # i.e., it is NOT bounded by A|x| + B for any A, B > 0.
    # Equivalently, limsup_{|x|->oo} |f(x)|/|x| = oo
    neg_q_ok = False
    
    # Check limit at positive infinity
    try:
        L1 = sympy.limit(sympy.Abs(witness) / sympy.Abs(sym), sym, sympy.oo)
        if L1 == sympy.oo or L1 == sympy.zoo or (hasattr(L1, 'max') and L1.max == sympy.oo):
            neg_q_ok = True
    except Exception:
        pass

    # Check limit at negative infinity
    if not neg_q_ok:
        try:
            L2 = sympy.limit(sympy.Abs(witness) / sympy.Abs(sym), sym, -sympy.oo)
            if L2 == sympy.oo or L2 == sympy.zoo or (hasattr(L2, 'max') and L2.max == sympy.oo):
                neg_q_ok = True
        except Exception:
            pass

    # Fallback 1: Check if it's a polynomial of degree > 1
    if not neg_q_ok:
        try:
            p_poly = sympy.poly(witness, sym)
            if p_poly.degree() > 1:
                neg_q_ok = True
        except Exception:
            pass

    # Fallback 2: Evaluate numerically at exponentially growing points
    if not neg_q_ok:
        try:
            ratios1 = []
            ratios2 = []
            for k in [2, 3, 4, 5, 6, 7]:
                v1_expr = sympy.Abs(witness.subs(sym, 10**k)).evalf()
                v2_expr = sympy.Abs(witness.subs(sym, -10**k)).evalf()
                v1 = float(v1_expr) / (10**k)
                v2 = float(v2_expr) / (10**k)
                ratios1.append(v1)
                ratios2.append(v2)
            
            def is_superlinear(ratios):
                # Check if the ratio |f(x)|/|x| is strictly and rapidly increasing
                return all(ratios[i+1] > 1.5 * ratios[i] for i in range(len(ratios)-1)) and ratios[-1] > 100
                
            if is_superlinear(ratios1) or is_superlinear(ratios2):
                neg_q_ok = True
        except Exception:
            pass

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: f is a real-valued function defined on R",
    "¬Q: f does not have linear growth (no A, B > 0 such that |f(x)| <= A|x| + B)"
]

N_HYP = 1
NEG_Q_INDEX = 1