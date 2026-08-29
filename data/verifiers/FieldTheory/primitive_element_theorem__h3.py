import sympy
from sympy.abc import u, v, w, x, y, z

# Expected witness format:
# A dictionary representing a finite field extension L/K:
# {
#     "characteristic": int,  # Prime p, e.g., 2
#     "base_transcendentals": [sympy.Symbol, ...],  # e.g., [u, v]
#     "extension_generators": [sympy.Symbol, ...],  # e.g., [x, y]
#     "minimal_polynomials": [sympy.Expr, ...]      # e.g., [x**2 - u, y**2 - v]
# }

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False, False, False]
            
        p = witness.get("characteristic")
        base_vars = witness.get("base_transcendentals")
        ext_vars = witness.get("extension_generators")
        min_polys = witness.get("minimal_polynomials")
        
        if p is None or base_vars is None or ext_vars is None or min_polys is None:
            return [False, False, False]
            
        if not isinstance(base_vars, list) or not isinstance(ext_vars, list) or not isinstance(min_polys, list):
            return [False, False, False]
            
        h1 = False
        h2 = False
        neg_q = False
        
        # H1: L/K is a field extension
        # We verify this by checking if p is prime and the minimal polynomials
        # are of the form X^p - U, which are irreducible over F_p(U, ...).
        if sympy.isprime(p):
            is_field_ext = True
            if len(ext_vars) != len(base_vars) or len(ext_vars) != len(min_polys):
                is_field_ext = False
            else:
                for ev, bv, poly in zip(ext_vars, base_vars, min_polys):
                    expected = ev**p - bv
                    diff = sympy.expand(poly - expected)
                    if diff != 0:
                        is_field_ext = False
                        break
            
            if is_field_ext and len(ext_vars) > 0:
                h1 = True
                
        # H2: The extension L/K is finite
        # The degree is p^(number of generators), which is finite.
        if h1:
            h2 = True
            
        # neg_Q: There is NO primitive element
        # In this purely inseparable extension, the p-th power of any element is in K.
        # Thus, the maximum degree of any element over K is p.
        # The degree of the extension is p^k where k = len(ext_vars).
        # If p^k > p (i.e., k > 1), no single element can generate L.
        if h1 and h2:
            k = len(ext_vars)
            if k > 1:
                neg_q = True
                
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L/K is a field extension",
    "H_2: The extension L/K is finite",
    "¬Q: There does not exist an element alpha in L such that L = K(alpha)"
]

N_HYP = 2
NEG_Q_INDEX = 2