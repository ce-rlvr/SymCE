import sympy
from sympy.polys.numberfields import primitive_element
from sympy import sympify, Dummy

# Top-level setup
I = sympy.I
sqrt = sympy.sqrt
Rational = sympy.Rational

def deg(gens):
    """
    Computes the degree of the field extension Q(gens) over Q.
    """
    if not gens:
        return 1
    filtered_gens = []
    for g in gens:
        sg = sympify(g)
        if not sg.is_rational:
            filtered_gens.append(sg)
    if not filtered_gens:
        return 1
    x = Dummy('x')
    _, p = primitive_element(filtered_gens, x)
    return p.degree()

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            F_gens = witness.get('F', [])
            K_gens = witness.get('K', [])
            L_gens = witness.get('L', [])
            alpha = witness.get('alpha')
        else:
            K_gens, L_gens, alpha = witness
            F_gens = []
            
        if not isinstance(F_gens, list): F_gens = [F_gens]
        if not isinstance(K_gens, list): K_gens = [K_gens]
        if not isinstance(L_gens, list): L_gens = [L_gens]
        
        # Compute degrees over Q
        d_F = deg(F_gens)
        d_K = deg(F_gens + K_gens)
        d_L = deg(F_gens + L_gens)
        d_KL = deg(F_gens + K_gens + L_gens)
        
        d_F_alpha = deg(F_gens + [alpha])
        d_L_alpha = deg(F_gens + L_gens + [alpha])
        
        # H1: K and L are field extensions of F contained in a common larger field.
        # In our representation, all elements are algebraic numbers in C, 
        # so they naturally lie in the common larger field C.
        h1 = True
        
        # H2: K and L are linearly disjoint over F.
        # This holds iff [KL : F] == [K : F] * [L : F]
        # Equivalent to: d_KL / d_F == (d_K / d_F) * (d_L / d_F)
        h2 = (d_KL * d_F == d_K * d_L)
        
        # Conclusion: The minimal polynomial of alpha over F is identical to the minimal polynomial of alpha over L.
        # Since F is a subfield of L, the minimal polynomial of alpha over L divides the one over F.
        # Being monic, they are identical if and only if they have the same degree.
        # [F(alpha) : F] == [L(alpha) : L]
        # Equivalent to: d_F_alpha / d_F == d_L_alpha / d_L
        neg_q = (d_F_alpha * d_L != d_L_alpha * d_F)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: K and L are field extensions of F contained in a common larger field",
    "H_2: K and L are linearly disjoint over F",
    "¬Q: The minimal polynomial of alpha over F is NOT identical to the minimal polynomial of alpha over L"
]

N_HYP = 2
NEG_Q_INDEX = 2