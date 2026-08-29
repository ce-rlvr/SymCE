import sympy
from sympy.ntheory import totient

# Top-level setup
# (No specific named bindings required for this Number Theory conjecture; use integers directly)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the conjecture:
    Hypotheses:
      - a >= 2
      - n >= 1
    Conclusion:
      - n divides phi(a^n - 1)
    """
    try:
        a, n = witness
    except Exception:
        return [False, False, False]
    
    # Check H_1: a >= 2
    try:
        a_sym = sympy.sympify(a)
        try:
            h1 = bool(a_sym >= 2)
        except TypeError:
            h1 = bool(a_sym.evalf() >= 2)
    except Exception:
        h1 = False
        
    # Check H_2: n >= 1
    try:
        n_sym = sympy.sympify(n)
        try:
            h2 = bool(n_sym >= 1)
        except TypeError:
            h2 = bool(n_sym.evalf() >= 1)
    except Exception:
        h2 = False
        
    # Check ¬Q: n does not divide phi(a^n - 1)
    try:
        a_sym = sympy.sympify(a)
        n_sym = sympy.sympify(n)
        val = sympy.simplify(a_sym**n_sym - 1)
        
        # Determine if a^n - 1 is an integer
        if val.is_Integer:
            val_int = int(val)
        else:
            try:
                val_f = val.evalf()
                if val_f.is_real and abs(val_f - round(val_f)) < 1e-9:
                    val_int = int(round(val_f))
                else:
                    val_int = None
            except Exception:
                val_int = None
                
        # If a^n - 1 is not a positive integer, the totient function is undefined,
        # meaning the conclusion fails (so ¬Q is True).
        if val_int is None or val_int < 1:
            neg_q = True
        else:
            phi_val = totient(val_int)
            
            # Determine if n is an integer
            if n_sym.is_Integer:
                n_int = int(n_sym)
            else:
                try:
                    n_f = n_sym.evalf()
                    if n_f.is_real and abs(n_f - round(n_f)) < 1e-9:
                        n_int = int(round(n_f))
                    else:
                        n_int = None
                except Exception:
                    n_int = None
                    
            # If n is not an integer or is zero, divisibility fails
            if n_int is None or n_int == 0:
                neg_q = True
            else:
                neg_q = (phi_val % n_int) != 0
                
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a >= 2",
    "H_2: n >= 1",
    "¬Q: n does not divide phi(a^n - 1)"
]

N_HYP = 2
NEG_Q_INDEX = 2