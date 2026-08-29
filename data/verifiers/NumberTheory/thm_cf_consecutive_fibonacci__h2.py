import sympy

# Top-level setup
# (No named bindings needed for this number theory conjecture)

def conditions(witness) -> list[bool]:
    try:
        # The witness should be an integer index n
        h1 = (isinstance(witness, int) and not isinstance(witness, bool)) or isinstance(witness, sympy.Integer)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            n = int(witness)
            # The conclusion states that the continued fraction of F_n / F_{n-1} 
            # is exactly [1; 1, ..., 1] of length n-1.
            # This requires n-1 >= 1 (so n >= 2) for the continued fraction to be well-defined and non-empty.
            if n < 2:
                q = False
            else:
                f_n = sympy.fibonacci(n)
                f_n_minus_1 = sympy.fibonacci(n-1)
                
                if f_n_minus_1 == 0:
                    q = False
                else:
                    val1 = sympy.Rational(f_n, f_n_minus_1)
                    
                    # Evaluate the continued fraction [1; 1, ..., 1] of length n-1.
                    # The value of this continued fraction is F_{L+1} / F_L where L = n-1.
                    length = n - 1
                    num = sympy.fibonacci(length + 1)
                    den = sympy.fibonacci(length)
                    
                    if den == 0:
                        q = False
                    else:
                        val2 = sympy.Rational(num, den)
                        q = (val1 == val2)
            
            neg_q = not q
    except Exception:
        # If any evaluation fails (e.g., division by zero), the conclusion fails.
        neg_q = True

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer",
    "¬Q: The continued fraction expansion of F_n / F_{n-1} is not exactly n-1 ones"
]

N_HYP = 1
NEG_Q_INDEX = 1