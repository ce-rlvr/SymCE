import sympy

# Top-level setup
x = sympy.Symbol('x')

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (w_x, G_exprs, f)
    where:
      - w_x is a sympy.Symbol representing the generator of the field K = QQ(w_x).
      - G_exprs is a list of sympy expressions in w_x representing the automorphisms in G.
      - f is a sympy expression in w_x representing the generator of the subfield F = QQ(f).
    """
    try:
        w_x, G_exprs, f = witness
        w_x = sympy.sympify(w_x)
        G_exprs = [sympy.sympify(g) for g in G_exprs]
        f = sympy.sympify(f)
    except Exception:
        return [False, False, False]
        
    # H1: K is a field
    try:
        h1 = isinstance(w_x, sympy.Symbol)
    except Exception:
        h1 = False
        
    # H2: G is a finite group of automorphisms of K
    try:
        h2 = False
        if isinstance(G_exprs, list) and len(G_exprs) > 0:
            all_auto = True
            unique_G = []
            for g in G_exprs:
                # Must only contain the variable w_x
                if not g.free_symbols.issubset({w_x}):
                    all_auto = False
                    break
                    
                # Check for duplicates to ensure it's a valid set representation
                is_dup = False
                for ug in unique_G:
                    if sympy.cancel(g - ug) == 0:
                        is_dup = True
                        break
                if is_dup:
                    all_auto = False
                    break
                unique_G.append(g)
                
                # Check if g is a valid automorphism of QQ(w_x)
                # i.e., a fractional linear transformation (ax+b)/(cx+d) with ad-bc != 0
                g_canc = sympy.cancel(g)
                if not g_canc.has(w_x):
                    all_auto = False
                    break
                num, den = sympy.fraction(g_canc)
                if not num.is_polynomial(w_x) or not den.is_polynomial(w_x):
                    all_auto = False
                    break
                if sympy.degree(num, w_x) > 1 or sympy.degree(den, w_x) > 1:
                    all_auto = False
                    break
            
            if all_auto:
                # Check group identity
                has_id = False
                for g in G_exprs:
                    if sympy.cancel(g - w_x) == 0:
                        has_id = True
                        break
                
                if has_id:
                    # Check group closure under composition
                    closed = True
                    for g1 in G_exprs:
                        for g2 in G_exprs:
                            comp = sympy.cancel(g1.subs(w_x, g2))
                            if not any(sympy.cancel(comp - g3) == 0 for g3 in G_exprs):
                                closed = False
                                break
                        if not closed:
                            break
                    
                    if closed:
                        h2 = True
    except Exception:
        h2 = False
        
    # neg_Q: K/F is NOT a finite Galois extension OR Gal(K/F) != G
    try:
        if not f.free_symbols.issubset({w_x}):
            neg_q = False
        else:
            q = False
            # If f is constant, K/F is not finite, so Q is False.
            if f.has(w_x):
                # Check if G fixes F pointwise
                fixes_f = True
                for g in G_exprs:
                    if sympy.cancel(f.subs(w_x, g) - f) != 0:
                        fixes_f = False
                        break
                
                if fixes_f:
                    # Calculate the degree [K:F]
                    f_canc = sympy.cancel(f)
                    num, den = sympy.fraction(f_canc)
                    if num.is_polynomial(w_x) and den.is_polynomial(w_x):
                        deg_F = max(sympy.degree(num, w_x), sympy.degree(den, w_x))
                        # If [K:F] == |G| and G fixes F, then K/F is Galois and Gal(K/F) = G
                        if deg_F == len(G_exprs):
                            q = True
            neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: G is a finite group of automorphisms of K",
    "¬Q: K/F is not a finite Galois extension or Gal(K/F) != G"
]

N_HYP = 2
NEG_Q_INDEX = 2