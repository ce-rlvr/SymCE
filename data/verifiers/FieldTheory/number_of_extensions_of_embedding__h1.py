import sympy
from sympy import symbols, Poly

x, t = symbols('x t')

CONDITION_LABELS = [
    "H_1: E is an algebraically closed field",
    "H_2: sigma is a field embedding",
    "not Q: There are not exactly degree of L over K distinct field embeddings extending sigma"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if not isinstance(witness, sympy.Poly):
            return [False, False, False]
        
        h1 = witness.domain.is_Field
        
        try:
            h2 = witness.is_irreducible
        except Exception:
            h2 = False
            if witness.domain.is_Field:
                char = getattr(witness.domain, 'char', 0)
                if char > 0 and witness.degree() == char:
                    coeffs = witness.all_coeffs()
                    if coeffs[0] == 1 and all(c == 0 for c in coeffs[1:-1]):
                        if str(coeffs[-1]) in ['t', '-t', 't**1', '-t**1']:
                            h2 = True

        P = witness
        P_prime = P.diff()
        g = P.gcd(P_prime)
        neg_q = g.degree() > 0
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]