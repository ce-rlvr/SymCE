import sympy as sp

CONDITION_LABELS = [
    "H_1: K is a field of characteristic not equal to 2",
    "H_2: f(x) is a separable polynomial of degree n over K",
    "H_3: Delta is the discriminant of the polynomial f(x)",
    "¬Q: Conclusion fails (Gal(L/K) <= A_n iff Delta is a square)"
]

N_HYP = 3
NEG_Q_INDEX = 3

# Top-level setup
x = sp.Symbol('x')

def conditions(witness):
    """
    witness: tuple (f_expr, L_expr)
    where f_expr is the polynomial f(x) over QQ,
    and L_expr is a polynomial over QQ whose splitting field is L.
    """
    try:
        f_expr, L_expr = witness
        f = sp.Poly(f_expr, x, domain='QQ')
        g = sp.Poly(L_expr, x, domain='QQ')
    except Exception:
        return [False, False, False, False]
        
    # H_1: K is a field of characteristic not equal to 2
    # We evaluate over K = QQ, which has characteristic 0 != 2.
    h1 = True
    
    # H_2: f(x) is a separable polynomial of degree n over K
    try:
        n = f.degree()
        if n < 1:
            h2 = False
        else:
            f_diff = f.diff()
            gcd_f = f.gcd(f_diff)
            h2 = (gcd_f.degree() == 0)
    except Exception:
        h2 = False
        
    # H_3: Delta is the discriminant of the polynomial f(x)
    # This is a definition, so it holds as long as we can compute it.
    try:
        Delta = sp.discriminant(f_expr, x)
        h3 = True
    except Exception:
        h3 = False
        Delta = None
        
    # ¬Q: The conclusion fails.
    # Conclusion: Gal(L/K) viewed as a permutation group on the roots of f(x) 
    # is a subgroup of A_n if and only if Delta is the square of an element in K.
    try:
        if Delta is None:
            neg_q = False
        else:
            # Q_part: Delta is a square in K (QQ)
            if Delta < 0:
                Q_part = False
            else:
                root = sp.sqrt(Delta)
                Q_part = root.is_rational
                
            # P_part: Gal(L/K) viewed as a permutation group on the roots of f(x) is a subgroup of A_n
            # For Gal(L/K) to be viewed as a permutation group on the roots of f(x), 
            # L MUST contain all the roots of f(x).
            # If L contains the roots of f(x), the image of Gal(L/K) in Sym(roots) is exactly Gal(F/K),
            # where F is the splitting field of f. By Galois theory, Gal(F/K) <= A_n iff Delta is a square.
            # So if L contains the roots, P_part == Q_part is ALWAYS True.
            # If L DOES NOT contain the roots of f(x), Gal(L/K) cannot act on them, so P_part is False.
            
            # We check if L contains the roots of f(x).
            # To make the verifier robust and fast, we check two main cases the prover might use:
            if sp.simplify(f_expr - L_expr) == 0:
                # L is the splitting field of f(x). It contains the roots.
                P_part = Q_part
            else:
                # Check if L is just QQ (e.g., L_expr = x)
                roots_L = sp.roots(L_expr, x)
                if roots_L and all(r.is_rational for r in roots_L):
                    # L = QQ. It contains the roots of f iff all roots of f are rational.
                    roots_f = sp.roots(f_expr, x)
                    if sum(roots_f.values()) == n and all(r.is_rational for r in roots_f):
                        P_part = True
                    else:
                        P_part = False
                else:
                    # For other arbitrary L, we default to False (not a permutation group on the roots)
                    # unless we can trivially prove f splits in L.
                    P_part = False
            
            # The conclusion is (P_part == Q_part). We want it to FAIL.
            conclusion = (P_part == Q_part)
            neg_q = not conclusion
            
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]