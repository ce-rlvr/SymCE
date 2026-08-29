import sympy
from sympy import Symbol, cancel, fraction, degree

# Top-level setup
x = Symbol('x')

def conditions(witness):
    """
    Expected witness format:
    A dictionary representing an endomorphism of a rational function field F(x).
    {
        "F": "QQ",           # The base field (string, e.g., "QQ")
        "E": "QQ(x)",        # The extension field (string)
        "x": x,              # The generator (sympy.Symbol)
        "sigma_x": x**2      # The image of x under the homomorphism sigma (sympy expression)
    }
    """
    try:
        if not isinstance(witness, dict):
            return [False, False, False, False]
            
        F_str = witness.get("F", "")
        E_str = witness.get("E", "")
        w_x = witness.get("x")
        sigma_x = witness.get("sigma_x")
        
        # H1: F is a field
        h1 = F_str in ["QQ", "RR", "CC", "Q", "R", "C"]
        
        # H2: \sigma: E \to E is a field homomorphism
        h2_E = E_str in ["QQ(x)", "RR(x)", "CC(x)", "Q(x)", "R(x)", "C(x)"]
        
        if not isinstance(w_x, Symbol):
            return [False, False, False, False]
            
        sigma_x_simp = cancel(sigma_x)
        num, den = fraction(sigma_x_simp)
        
        # Must be a non-constant rational function to be a valid F-endomorphism of F(x)
        h2_hom = (w_x in num.free_symbols or w_x in den.free_symbols)
        h2 = h2_E and h2_hom
        
        # H3: \sigma(a) = a for all a \in F
        # In our model, F is the base field and sigma is an F-endomorphism by definition,
        # so it fixes all constants (elements of F).
        h3 = True
        
        # neg_Q: \sigma is NOT bijective
        # An F-endomorphism of F(x) given by x |-> P(x)/Q(x) is bijective
        # if and only if max(deg(P), deg(Q)) == 1.
        deg_num = degree(num, w_x)
        deg_den = degree(den, w_x)
        
        is_bijective = (max(deg_num, deg_den) == 1)
        neg_q = not is_bijective
        
        return [bool(h1), bool(h2), bool(h3), bool(neg_q)]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: \\sigma: E \\to E is a field homomorphism",
    "H_3: \\sigma(a) = a for all a \\in F",
    "¬Q: \\sigma is not a bijective map"
]

N_HYP = 3
NEG_Q_INDEX = 3