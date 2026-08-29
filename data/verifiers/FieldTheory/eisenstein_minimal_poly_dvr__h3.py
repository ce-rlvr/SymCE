import sympy
from sympy import Symbol, Poly, simplify
from sympy.ntheory import isprime

# Top-level setup: named object bindings that the witness expression may reference.
x = Symbol('x')

def conditions(witness):
    """
    Checks whether the given witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (p, f, alpha) or a dictionary with these keys, where:
      - p is a prime number (defining the p-adic valuation on Q)
      - f is a SymPy polynomial expression in x over Q
      - alpha is a root of f
    """
    try:
        if isinstance(witness, dict):
            p = witness.get('p')
            f = witness.get('f')
            alpha = witness.get('alpha')
        else:
            p, f, alpha = witness
    except Exception:
        return [False, False, False, False]

    # H_1: F is a field with a discrete valuation v and valuation ring O_v
    # We interpret F=Q and v as the p-adic valuation, which requires p to be prime.
    try:
        h1 = bool(isprime(p))
    except Exception:
        h1 = False

    # H_2: π is a uniformizer for O_v
    # For the p-adic valuation on Q, p is a uniformizer.
    try:
        h2 = bool(isprime(p))
    except Exception:
        h2 = False

    # H_3: α is a root of f(x) in some extension field of F
    try:
        # Ensure f is a valid polynomial over Q
        f_poly = Poly(f, x, domain='QQ')
        val = f.subs(x, alpha)
        h3 = bool(simplify(val) == 0 or val.equals(0))
    except Exception:
        h3 = False

    # ¬Q: f(x) is NOT the minimal polynomial of α over F
    # The minimal polynomial of α over Q is the unique monic irreducible polynomial in Q[x] having α as a root.
    try:
        f_poly = Poly(f, x, domain='QQ')
        is_monic = (f_poly.LC() == 1)
        is_irred = bool(f_poly.is_irreducible)
        
        val = f.subs(x, alpha)
        is_root = bool(simplify(val) == 0 or val.equals(0))
        
        is_min_poly = is_monic and is_irred and is_root
        neg_q = not is_min_poly
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: F is a field with a discrete valuation v and valuation ring O_v",
    "H_2: π is a uniformizer for O_v",
    "H_3: α is a root of f(x) in some extension field of F",
    "¬Q: f(x) is not the minimal polynomial of α over F"
]

N_HYP = 3
NEG_Q_INDEX = 3