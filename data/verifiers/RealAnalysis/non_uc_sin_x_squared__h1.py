import sympy
from sympy import Symbol, S, diff, oo, sympify
from sympy.calculus.util import continuous_domain, maximum, minimum

# Top-level setup
x = Symbol('x', real=True)

def conditions(witness) -> list[bool]:
    neg_q = False
    
    try:
        # Handle both callable functions and SymPy expressions
        if callable(witness):
            try:
                f = witness(x)
            except Exception:
                try:
                    f = witness()
                except Exception:
                    f = witness
        else:
            f = witness
            
        f = sympify(f)
        
        free_syms = f.free_symbols
        if len(free_syms) == 0:
            # Constant functions are uniformly continuous on R
            neg_q = True
        elif len(free_syms) == 1:
            var = list(free_syms)[0]
            
            # Check if the function is continuous on all of R
            dom = continuous_domain(f, var, S.Reals)
            if dom == S.Reals:
                df = diff(f, var)
                
                # If the derivative is constant, it's uniformly continuous (e.g., linear functions)
                if df.is_constant():
                    neg_q = True
                else:
                    # If the derivative is bounded on R, the function is uniformly continuous
                    max_df = maximum(df, var, S.Reals)
                    min_df = minimum(df, var, S.Reals)
                    if max_df < oo and min_df > -oo:
                        neg_q = True
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: f is uniformly continuous on R"
]

N_HYP = 0
NEG_Q_INDEX = 0