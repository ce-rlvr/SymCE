import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
sqrt = sp.sqrt
I = sp.I
Rational = sp.Rational
pi = sp.pi
exp = sp.exp
cos = sp.cos
sin = sp.sin
Symbol = sp.Symbol

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (alpha, sigma_alpha, n, x)
    where:
      - alpha is a primitive element for L over K=QQ.
      - sigma_alpha is the image of alpha under the generator sigma of Gal(L/K).
      - n is the degree of the extension [L:K].
      - x is the element for which the conclusion fails.
    """
    try:
        alpha, sigma_alpha, n, x = witness
    except Exception:
        return [False, False, False]
        
    h1 = False
    h2 = False
    try:
        if isinstance(n, int) and n >= 1:
            ma = sp.minpoly(alpha)
            gen = list(ma.free_symbols)[0] if ma.free_symbols else sp.Symbol('x')
            if sp.degree(ma, gen) == n:
                val = sp.simplify(ma.subs(gen, sigma_alpha))
                if val == 0:
                    current = alpha
                    is_cyclic = True
                    for k in range(1, n):
                        current = sp.simplify(current.subs(alpha, sigma_alpha))
                        if sp.simplify(current - alpha) == 0:
                            is_cyclic = False
                            break
                    if is_cyclic:
                        current = sp.simplify(current.subs(alpha, sigma_alpha))
                        if sp.simplify(current - alpha) == 0:
                            h1 = True
                            h2 = True
    except Exception:
        pass

    neg_q = False
    try:
        # Compute the field norm N_{L/K}(x) extended to the field containing x
        norm_val = x
        current_sigma_x = x
        for _ in range(1, n):
            current_sigma_x = sp.simplify(current_sigma_x.subs(alpha, sigma_alpha))
            norm_val = sp.simplify(norm_val * current_sigma_x)
        
        # The conclusion fails if N(x) == 1 but there is no y in L such that x = y / sigma(y).
        # By Hilbert's Theorem 90, if x is in L and N(x) == 1, such y ALWAYS exists.
        # Therefore, the only way for the conclusion to fail is if N(x) == 1 AND x is NOT in L.
        if sp.simplify(norm_val - 1) == 0:
            in_L = True
            # Check if x is in L = QQ(alpha) by checking the degree of the primitive element of QQ(x, alpha)
            for c in [1, 2]:
                prim = sp.simplify(x + c * alpha)
                try:
                    deg = sp.degree(sp.minpoly(prim))
                    if deg > n:
                        in_L = False
                        break
                except Exception:
                    # If minpoly fails, x is likely not algebraic, hence not in L
                    in_L = False
                    break
            
            if not in_L:
                neg_q = True
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: L/K is a finite cyclic Galois extension",
    "H_2: sigma is a generator of the Galois group Gal(L/K)",
    "¬Q: N_{L/K}(x) = 1 but there is no non-zero y in L such that x = y / sigma(y)"
]

N_HYP = 2
NEG_Q_INDEX = 2