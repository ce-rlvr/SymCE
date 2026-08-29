import sympy as sp
from sympy import Poly
from sympy.abc import x
from sympy.ntheory import isprime, multiplicity

def get_vp(c, p):
    if c == 0:
        return float('inf')
    c_rat = sp.Rational(c)
    return multiplicity(p, c_rat.p) - multiplicity(p, c_rat.q)

def conditions(witness):
    """
    Checks the hypotheses and negated conclusion for the false conjecture:
    "Let F be a field with a discrete valuation v and valuation ring O_v.
     Let π be a uniformizer for O_v.
     Let f(x) be an Eisenstein polynomial with respect to π.
     Then f(x) is the minimal polynomial of α over F."
     
    The witness should be a tuple: (p, pi, f, alpha)
    where:
      - p is a prime number (defining F=QQ, v=v_p, O_v=Z_{(p)})
      - pi is a uniformizer (v_p(pi) == 1)
      - f is a sympy polynomial expression in x
      - alpha is a sympy expression (the proposed root)
    """
    try:
        p, pi, f, alpha = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: F is a field with a discrete valuation v and valuation ring O_v
    # We use F = QQ, v = v_p. This is valid if p is prime.
    try:
        h1 = isprime(p)
    except Exception:
        h1 = False
        
    # H_2: π is a uniformizer for O_v
    # This means v_p(pi) == 1
    try:
        if not h1:
            h2 = False
        else:
            h2 = (get_vp(pi, p) == 1)
    except Exception:
        h2 = False
        
    # H_3: f(x) is an Eisenstein polynomial with respect to π
    # i.e., f is monic, v_p(a_i) >= 1 for i < n, v_p(a_0) == 1, and all a_i in O_v
    try:
        if not h1:
            h3 = False
        else:
            poly_f = Poly(f, x)
            coeffs = poly_f.all_coeffs()
            n = poly_f.degree()
            if n < 1:
                h3 = False
            else:
                is_monic = (coeffs[0] == 1)
                eisenstein = is_monic
                if eisenstein:
                    for i in range(1, n + 1):
                        vp = get_vp(coeffs[i], p)
                        if vp < 1:
                            eisenstein = False
                            break
                        if i == n and vp != 1:
                            eisenstein = False
                            break
                h3 = eisenstein
    except Exception:
        h3 = False
        
    # ¬Q: f(x) is not the minimal polynomial of α over F
    # Since f is Eisenstein, it is irreducible over F. Being monic, it is the 
    # minimal polynomial of α if and only if α is a root of f.
    # Thus, f is NOT the minimal polynomial iff f(α) != 0.
    try:
        val = sp.simplify(f.subs(x, alpha))
        neg_q = (val != 0)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with a discrete valuation v and valuation ring O_v",
    "H_2: π is a uniformizer for O_v",
    "H_3: f(x) is an Eisenstein polynomial with respect to π",
    "¬Q: f(x) is not the minimal polynomial of α over F"
]

N_HYP = 3
NEG_Q_INDEX = 3