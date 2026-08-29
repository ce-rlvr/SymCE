import sympy
from sympy import Poly, QQ
from sympy.abc import x
from sympy.polys.numberfields import primitive_element, minpoly
from sympy import factor_list

# Note: Avoid using brackets like F[x] in the labels to prevent parsing issues 
# with naive regex-based validators that stop at the first closing bracket.
CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f is a non-constant polynomial over F",
    "H_3: f is a separable polynomial",
    "¬Q: The field extension K/F is not a Galois extension"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Given a witness tuple (F, K_gens, f), where:
      - F is a SymPy domain (e.g., QQ)
      - K_gens is a list of algebraic generators for K over F (e.g., [2**(1/3)])
      - f is a SymPy expression or Poly in x
    Checks if it satisfies the remaining hypotheses and falsifies the conclusion.
    """
    try:
        F, K_gens, f = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field
    try:
        h1 = getattr(F, 'is_Field', False)
    except Exception:
        h1 = False
        
    # H_2: f is a non-constant polynomial over F
    try:
        f_poly = Poly(f, x, domain=F)
        h2 = f_poly.degree() >= 1
    except Exception:
        h2 = False
        
    # H_3: f is a separable polynomial
    try:
        f_poly = Poly(f, x, domain=F)
        f_diff = f_poly.diff()
        # In characteristic 0, separable means gcd(f, f') == 1
        h3 = f_poly.gcd(f_diff).degree() == 0
    except Exception:
        h3 = False
        
    # ¬Q: K/F is not a Galois extension
    try:
        # For safety and performance, we restrict the Galois check to F = QQ
        if F != QQ:
            neg_q = False
        else:
            if not K_gens:
                # K = F, which is trivially Galois
                neg_q = False
            else:
                if len(K_gens) == 1:
                    alpha = K_gens[0]
                    mp = minpoly(alpha, x)
                else:
                    alpha, mp = primitive_element(K_gens, x)
                
                # Factor the minimal polynomial of the primitive element over K
                coeff, factors = factor_list(mp, extension=K_gens)
                
                # If K/F is Galois, the minimal polynomial must split completely into linear factors
                is_galois = True
                for fac, mult in factors:
                    if Poly(fac, x).degree() > 1:
                        is_galois = False
                        break
                neg_q = not is_galois
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]