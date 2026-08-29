import sympy as sp

x = sp.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should provide the integer n and the element zeta.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            zeta = witness.get('zeta')
        else:
            n, zeta = witness
    except Exception:
        return [False, False]

    # H_1: n >= 3 is an integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n >= 3
    except Exception:
        h1 = False

    # ¬Q: The reciprocal zeta^{-1} is not a root of Phi_n(x), or zeta^{-1} == zeta
    try:
        if not h1:
            neg_q = False
        else:
            poly = sp.cyclotomic_poly(n, x)
            zeta_sym = sp.sympify(zeta)
            
            if zeta_sym == 0:
                # 0 has no reciprocal, so the conclusion fails
                neg_q = True
            else:
                recip = zeta_sym**(-1)
                val = poly.subs(x, recip)
                
                val_simp = sp.simplify(val)
                if val_simp == 0:
                    is_root = True
                else:
                    try:
                        is_root = abs(complex(val_simp.evalf())) < 1e-12
                    except Exception:
                        is_root = False

                diff = sp.simplify(recip - zeta_sym)
                if diff == 0:
                    is_neq = False
                else:
                    try:
                        is_neq = abs(complex(diff.evalf())) > 1e-12
                    except Exception:
                        is_neq = True
                
                q = is_root and is_neq
                neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "¬Q: The reciprocal zeta^{-1} is not a root of Phi_n(x), or zeta^{-1} == zeta"
]

N_HYP = 1
NEG_Q_INDEX = 1