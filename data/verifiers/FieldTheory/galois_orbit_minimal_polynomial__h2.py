import sympy as sp

# Top-level setup: named object bindings that the witness expression may reference.
x = sp.Symbol('x')
sqrt2 = sp.sqrt(2)
sqrt3 = sp.sqrt(3)
I = sp.I

def conditions(witness) -> list[bool]:
    from sympy import Symbol, sqrt, Poly, minpoly, simplify, sympify, sqrtdenest
    x = Symbol('x')
    
    alpha = None
    d = 2  # Default to E = QQ(sqrt(2))
    
    # Parse the witness to extract alpha and optionally the defining polynomial of E
    try:
        if isinstance(witness, dict):
            alpha = witness.get('alpha', None)
            if alpha is None:
                vals = list(witness.values())
                if len(vals) > 0:
                    alpha = vals[0]
                    
            E_poly = witness.get('E_poly', None)
            if E_poly is not None:
                try:
                    p = Poly(E_poly, x)
                    coeffs = p.all_coeffs()
                    if len(coeffs) == 3 and coeffs[0] == 1 and coeffs[1] == 0:
                        d = -coeffs[2]
                except Exception:
                    pass
        elif isinstance(witness, tuple) or isinstance(witness, list):
            for item in witness:
                try:
                    p = Poly(item, x)
                    coeffs = p.all_coeffs()
                    if len(coeffs) == 3 and coeffs[0] == 1 and coeffs[1] == 0:
                        d = -coeffs[2]
                except Exception:
                    pass
            for item in witness:
                try:
                    p = Poly(item, x)
                    coeffs = p.all_coeffs()
                    if len(coeffs) == 3 and coeffs[0] == 1 and coeffs[1] == 0 and -coeffs[2] == d:
                        continue
                except Exception:
                    pass
                alpha = item
                break
            if alpha is None and len(witness) > 0:
                alpha = witness[0]
        else:
            alpha = witness
            
        if alpha is None:
            return [False, False, False]
            
        alpha = sqrtdenest(simplify(sympify(alpha)))
        d = sympify(d)
    except Exception:
        return [False, False, False]
        
    # H_1: E/F is a finite Galois extension.
    # We evaluate the conjecture over F = QQ and E = QQ(sqrt(d)).
    # This is a finite Galois extension of degree 2 (or 1 if d is a perfect square).
    h1 = True
    
    # H_2: O_alpha is the orbit of alpha under the action of the Galois group.
    try:
        sq_d = sqrt(d)
        alpha1 = alpha
        if sq_d.is_rational:
            alpha2 = alpha
        else:
            # Apply the non-trivial automorphism of QQ(sqrt(d))/QQ
            alpha2 = alpha.subs(sq_d, -sq_d)
            
        # Determine the distinct elements in the orbit
        if (alpha1 - alpha2).equals(0):
            O_alpha = [alpha1]
        else:
            O_alpha = [alpha1, alpha2]
        h2 = True
    except Exception:
        h2 = False
        O_alpha = []
        
    # ¬Q: The minimal polynomial of alpha over F is NOT given by the product over the orbit.
    try:
        # Compute the product \prod_{beta \in O_alpha} (x - beta)
        prod = 1
        for beta in O_alpha:
            prod *= (x - beta)
        prod = prod.expand()
        
        # Compute the true minimal polynomial of alpha over QQ
        mp = minpoly(alpha, x)
        
        # The conclusion fails if the product does not equal the minimal polynomial
        diff = mp - prod
        neg_q = not diff.equals(0)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E/F is a finite Galois extension",
    "H_2: O_alpha is the orbit of alpha under the action of the Galois group",
    "¬Q: The minimal polynomial of alpha over F is NOT given by the product over the orbit"
]

N_HYP = 2
NEG_Q_INDEX = 2