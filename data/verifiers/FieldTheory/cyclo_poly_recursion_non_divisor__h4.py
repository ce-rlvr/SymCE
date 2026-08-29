import sympy as sp

# Top-level setup
# No specific named objects required for this number theory/polynomial conjecture

def conditions(witness) -> list[bool]:
    try:
        n, p = witness
    except Exception:
        return [False, False, False, False]
    
    # H_1: n >= 1 is an integer
    try:
        h1 = isinstance(n, (int, sp.Integer)) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: p is a prime number
    try:
        h2 = sp.isprime(p)
    except Exception:
        h2 = False
        
    # H_3: p does not divide n
    try:
        h3 = (n % p != 0)
    except Exception:
        h3 = False
        
    # ¬Q: Phi_{pn}(x) != Phi_n(x^p) / Phi_n(x)
    try:
        x = sp.Symbol('x')
        phi_pn = sp.cyclotomic_poly(int(p * n), x)
        phi_n = sp.cyclotomic_poly(int(n), x)
        phi_n_xp = phi_n.subs(x, x**int(p))
        
        # Check if Phi_{pn}(x) * Phi_n(x) == Phi_n(x^p)
        diff = sp.expand(phi_pn * phi_n - phi_n_xp)
        concl = (diff == 0)
        neg_q = not concl
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1 is an integer",
    "H_2: p is a prime number",
    "H_3: p does not divide n",
    "¬Q: Phi_{pn}(x) != Phi_n(x^p) / Phi_n(x)"
]

N_HYP = 3
NEG_Q_INDEX = 3