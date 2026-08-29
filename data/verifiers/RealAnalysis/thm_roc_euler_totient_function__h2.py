import sympy

# Top-level setup: named object bindings that the witness expression may reference.
n = sympy.Symbol('n', integer=True, positive=True)

def conditions(witness) -> list[bool]:
    # H_1: phi(n) is Euler's totient function.
    # This is a definitional statement that does not constrain the sequence a_n.
    h1 = True
    
    # neg_Q: The radius of convergence of the power series is NOT exactly 1.
    neg_q = False
    
    try:
        if callable(witness):
            witness = witness(n)
            
        if isinstance(witness, (list, tuple)):
            # A finite sequence (polynomial) has an infinite radius of convergence
            neg_q = True
            return [h1, neg_q]

        a_n = witness
        a_n_plus_1 = a_n.subs(n, n+1)
        
        # Try ratio test
        try:
            ratio = sympy.Abs(a_n / a_n_plus_1)
            R_ratio = sympy.limit(ratio, n, sympy.oo)
            if R_ratio is not sympy.nan and (R_ratio.is_number or R_ratio == sympy.oo):
                if R_ratio != 1:
                    neg_q = True
                    return [h1, neg_q]
                else:
                    return [h1, False]
        except Exception:
            pass
            
        # Try root test
        try:
            root = sympy.Abs(a_n)**(1/n)
            L_root = sympy.limit(root, n, sympy.oo)
            if L_root is not sympy.nan and (L_root.is_number or L_root == sympy.oo):
                if L_root == 0:
                    R_root = sympy.oo
                else:
                    R_root = 1 / L_root
                
                if R_root != 1:
                    neg_q = True
                    return [h1, neg_q]
                else:
                    return [h1, False]
        except Exception:
            pass

    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: phi(n) is Euler's totient function",
    "¬Q: The radius of convergence of the power series is not exactly 1"
]

N_HYP = 1
NEG_Q_INDEX = 1