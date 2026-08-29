import sympy
import math

# Top-level setup: named object bindings that the witness expression may reference.
x = sympy.Symbol('x', real=True)
k = sympy.Symbol('k', real=True)

CONDITION_LABELS = [
    "H_1: p and q are real numbers such that 1 <= p <= 2 and 1/p + 1/q = 1",
    "¬Q: The Fourier transform f_hat does not belong to L^q or ||f_hat||_q > ||f||_p"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The witness should be a tuple (p, q, f) or a dictionary {'p': p, 'q': q, 'f': f},
    where p and q are numbers (or sympy.oo) and f is a sympy expression representing a function.
    """
    if isinstance(witness, dict):
        p = witness.get('p')
        q = witness.get('q')
        f = witness.get('f')
    else:
        p, q, f = witness
        
    try:
        p = sympy.sympify(p)
        q = sympy.sympify(q)
    except Exception:
        pass
        
    if hasattr(f, 'free_symbols'):
        free_syms = f.free_symbols
        if len(free_syms) == 1:
            var = list(free_syms)[0]
        elif len(free_syms) == 0:
            var = x
        else:
            if x in free_syms:
                var = x
            else:
                var = list(free_syms)[0]
    else:
        try:
            f = sympy.sympify(f)
            var = x
        except Exception:
            f = sympy.S.Zero
            var = x

    # H1: 1 <= p <= 2 and 1/p + 1/q = 1
    h1_ok = False
    try:
        if p == sympy.oo:
            p_val = float('inf')
            p_inv = 0.0
        else:
            p_val = float(p)
            p_inv = 1.0 / p_val
            
        if q == sympy.oo:
            q_val = float('inf')
            q_inv = 0.0
        else:
            q_val = float(q)
            q_inv = 1.0 / q_val
            
        if 1 <= p_val <= 2:
            if math.isclose(p_inv + q_inv, 1.0, rel_tol=1e-7, abs_tol=1e-7):
                h1_ok = True
    except Exception:
        h1_ok = False
        
    # neg_Q: f_hat not in L^q OR ||f_hat||_q > ||f||_p
    neg_q_ok = False
    try:
        # Compute Fourier transform
        f_hat = sympy.fourier_transform(f, var, k)
        if f_hat.has(sympy.FourierTransform):
            # Try manual integration if fourier_transform remains unevaluated
            f_hat = sympy.integrate(f * sympy.exp(-2 * sympy.pi * sympy.I * var * k), (var, -sympy.oo, sympy.oo))
            
        if f_hat.has(sympy.DiracDelta):
            # Dirac delta functions are not in L^q for any q
            neg_q_ok = True
        else:
            # Compute norm_f_hat
            if q == sympy.oo:
                try:
                    norm_f_hat = sympy.maximum(sympy.Abs(f_hat), k, sympy.Interval(-sympy.oo, sympy.oo))
                except Exception:
                    norm_f_hat = None
            else:
                int_f_hat = sympy.integrate(sympy.Abs(f_hat)**q, (k, -sympy.oo, sympy.oo))
                if int_f_hat == sympy.oo:
                    norm_f_hat = sympy.oo
                elif int_f_hat == sympy.nan or isinstance(int_f_hat, sympy.Integral):
                    norm_f_hat = None
                else:
                    norm_f_hat = int_f_hat ** (1/q)
                    
            if norm_f_hat == sympy.oo:
                neg_q_ok = True
            elif norm_f_hat is not None:
                # Compute norm_f
                if p == sympy.oo:
                    try:
                        norm_f = sympy.maximum(sympy.Abs(f), var, sympy.Interval(-sympy.oo, sympy.oo))
                    except Exception:
                        norm_f = None
                else:
                    int_f = sympy.integrate(sympy.Abs(f)**p, (var, -sympy.oo, sympy.oo))
                    if int_f == sympy.oo:
                        norm_f = sympy.oo
                    elif int_f == sympy.nan or isinstance(int_f, sympy.Integral):
                        norm_f = None
                    else:
                        norm_f = int_f ** (1/p)
                        
                if not neg_q_ok and norm_f is not None:
                    if norm_f == sympy.oo:
                        # If f is not in L^p, then ||f||_p = oo, so ||f_hat||_q <= ||f||_p is trivially true
                        neg_q_ok = False
                    else:
                        try:
                            diff = float(norm_f_hat - norm_f)
                        except Exception:
                            diff = float((norm_f_hat - norm_f).evalf())
                        if diff > 1e-7:
                            neg_q_ok = True
    except Exception:
        pass
        
    return [h1_ok, neg_q_ok]