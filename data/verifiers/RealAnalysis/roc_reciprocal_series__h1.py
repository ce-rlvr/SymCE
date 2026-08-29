import sympy
import math

# Top-level setup
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if callable(witness):
            a0 = witness(0)
        elif isinstance(witness, (list, tuple)):
            a0 = witness[0] if len(witness) > 0 else 0
        elif hasattr(witness, "free_symbols"):
            syms = list(witness.free_symbols)
            if len(syms) == 1:
                a0 = witness.subs(syms[0], 0)
            elif len(syms) == 0:
                a0 = witness
            else:
                a0 = 0
        else:
            a0 = 0
            
        if isinstance(a0, sympy.Basic):
            a0_val = complex(a0.evalf())
        else:
            a0_val = complex(a0)
            
        h1 = (abs(a0_val) > 1e-12)
    except Exception:
        h1 = False
        a0_val = 0.0

    try:
        if abs(a0_val) <= 1e-12:
            # If a0 is zero, the formal product can never have a constant term of 1.
            # Thus, no such reciprocal series exists, and the conclusion fails.
            neg_q = True
        else:
            # The formal reciprocal series has a strictly positive radius of convergence
            # if and only if the original series has a strictly positive radius of convergence.
            # We check if the original series has radius of convergence 0, which means
            # limsup |a_n|^(1/n) = infinity. We do this by checking if log(|a_n|)/n grows.
            def eval_log_root(n_val):
                if callable(witness):
                    val = witness(n_val)
                elif isinstance(witness, (list, tuple)):
                    val = witness[n_val] if n_val < len(witness) else 0
                elif hasattr(witness, "free_symbols"):
                    syms = list(witness.free_symbols)
                    if len(syms) == 1:
                        val = witness.subs(syms[0], n_val)
                    elif len(syms) == 0:
                        val = witness
                    else:
                        raise ValueError("Too many free symbols")
                else:
                    raise ValueError("Unknown witness type")
                    
                if isinstance(val, sympy.Basic):
                    val_f = abs(val.evalf())
                    if val_f < 1e-100:
                        return float('-inf')
                    log_val = float(sympy.log(val_f).evalf())
                    return log_val / n_val
                elif isinstance(val, int):
                    val_abs = abs(val)
                    if val_abs == 0:
                        return float('-inf')
                    return math.log(val_abs) / n_val
                else:
                    val_abs = abs(complex(val))
                    if val_abs < 1e-100:
                        return float('-inf')
                    return math.log(val_abs) / n_val

            def get_max_log_R(start, end):
                max_log_R = float('-inf')
                for n in range(start, end):
                    try:
                        lr = eval_log_root(n)
                        if lr > max_log_R:
                            max_log_R = lr
                    except Exception:
                        pass
                return max_log_R

            LR1 = get_max_log_R(20, 40)
            LR2 = get_max_log_R(80, 100)
            LR3 = get_max_log_R(180, 200)

            # Check for super-exponential growth of coefficients
            neg_q = (LR3 > LR2 + 0.08) and (LR2 > LR1 + 0.08)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: The constant term a_0 is non-zero",
    "¬Q: The formal reciprocal series has radius of convergence 0"
]

N_HYP = 1
NEG_Q_INDEX = 1