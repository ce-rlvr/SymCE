import sympy as sp
from sympy import Poly, rem

# Top-level setup
x = sp.Symbol('x')

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample to the false conjecture.
    The witness should be a tuple of 4 SymPy expressions in `x`: (P, Q, I, T)
      - P: Minimal polynomial of the field extension K/F (assuming F = Q).
      - Q: Minimal polynomial of the intermediate field E/F.
      - I: Polynomial representing the inclusion E -> K (I(x) is a root of Q in K).
      - T: Polynomial representing the embedding tau: E -> K (T(x) is a root of Q in K).
    """
    try:
        if len(witness) != 4:
            return [False, False, False]
        P, Q, I, T = witness
    except Exception:
        return [False, False, False]

    # H_1: E is an intermediate field such that F <= E <= K
    try:
        P_poly = Poly(P, x, domain='QQ')
        Q_poly = Poly(Q, x, domain='QQ')
        
        # K and E must be valid field extensions over Q
        h1_1 = P_poly.is_irreducible
        h1_2 = Q_poly.is_irreducible
        h1_3 = P_poly.degree() > 0 and Q_poly.degree() > 0
        
        # I(x) must be a valid embedding of E into K (i.e., I(x) is a root of Q mod P)
        rem_I = rem(Q.subs(x, I), P, x)
        h1_4 = sp.expand(rem_I) == 0
        
        h1 = bool(h1_1 and h1_2 and h1_3 and h1_4)
    except Exception:
        h1 = False

    # H_2: tau: E -> K is an F-embedding
    try:
        # T(x) must be a valid embedding of E into K (i.e., T(x) is a root of Q mod P)
        rem_T = rem(Q.subs(x, T), P, x)
        h2 = bool(sp.expand(rem_T) == 0)
    except Exception:
        h2 = False

    # neg_Q: There does NOT exist an F-automorphism sigma of K such that sigma|_E = tau
    try:
        y = sp.Symbol('y')
        P_y = P.subs(x, y)
        
        # Find all roots of P(y) in K = Q[x]/(P(x)) to find all F-automorphisms of K
        alpha = sp.rootof(P, 0)
        factored = sp.factor(P_y, extension=alpha)
        
        roots = []
        if factored.func == sp.Mul:
            factors = factored.args
        else:
            factors = [factored]
            
        for f in factors:
            if f.func == sp.Pow:
                base = f.args[0]
            else:
                base = f
                
            # Linear factors correspond to roots in K
            if sp.degree(base, y) == 1:
                sol = sp.solve(base, y)
                if sol:
                    root_alpha = sol[0]
                    # Convert the root expression from alpha to x
                    root_x = root_alpha.subs(alpha, x)
                    root_x = sp.rem(root_x, P, x)
                    roots.append(root_x)
                    
        if len(roots) == 0:
            neg_q = False
        else:
            extends = False
            # Check if any automorphism A(x) restricts to T(x) on E
            for A in roots:
                # Restriction of A to E is A(I(x)) mod P(x)
                I_A = sp.rem(sp.expand(I.subs(x, A)), P, x)
                T_rem = sp.rem(T, P, x)
                if sp.expand(I_A - T_rem) == 0:
                    extends = True
                    break
            
            # The conclusion fails if NO automorphism extends tau
            neg_q = not extends
            
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: E is an intermediate field F <= E <= K",
    "H_2: tau is an F-embedding of E into K",
    "¬Q: There does not exist an F-automorphism of K extending tau"
]

N_HYP = 2
NEG_Q_INDEX = 2