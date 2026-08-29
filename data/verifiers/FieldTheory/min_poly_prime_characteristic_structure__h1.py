import sympy
from sympy import Poly
from sympy.abc import x, t

# Top-level setup
# Symbols x and t are provided for constructing polynomials and rational function fields.

CONDITION_LABELS = [
    "H_1: alpha is an algebraic element over F (m is a valid polynomial and p is prime)",
    "H_2: m(x) is the minimal polynomial of alpha over F (monic and irreducible)",
    "¬Q: There does not exist e >= 0 and separable irreducible g(x) such that m(x) = g(x^{p^e})"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        p, m = witness
    except Exception:
        return [False, False, False]
        
    # H1: alpha is algebraic over F -> m is a valid non-constant univariate polynomial
    try:
        h1 = isinstance(p, int) and sympy.isprime(p) and isinstance(m, Poly) and m.degree() > 0 and len(m.gens) == 1
    except Exception:
        h1 = False
        
    # H2: m is the minimal polynomial -> m is monic and irreducible
    try:
        h2 = bool(m.is_monic and m.is_irreducible)
    except Exception:
        h2 = False
        
    # neg_Q: NO e >= 0 and separable irreducible g exists such that m(x) = g(x^{p^e})
    try:
        q_holds = False
        monoms = m.monoms()
        exponents = [mon[0] for mon in monoms]
        
        max_e = 0
        while p**(max_e + 1) <= m.degree():
            max_e += 1
            
        for e in range(max_e + 1):
            pe = p**e
            if all(exp % pe == 0 for exp in exponents):
                g_dict = { (exp // pe,) : c for (exp,), c in zip(monoms, m.coeffs()) }
                g = Poly.from_dict(g_dict, m.gens[0], domain=m.domain)
                
                # g is guaranteed to be irreducible because m is irreducible
                g_diff = g.diff()
                if g_diff.is_zero:
                    is_sep = False
                else:
                    gcd_poly = g.gcd(g_diff)
                    is_sep = gcd_poly.degree() == 0
                    
                if is_sep:
                    q_holds = True
                    break
        neg_q = not q_holds
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]