import sympy
from sympy import cyclotomic_poly
from sympy.abc import x
from sympy.polys.polytools import factor_list

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: q is a prime number",
    "H_2: q is distinct from p",
    "H_3: zeta_p is a primitive p-th root of unity",
    "¬Q: The equivalence between splitting into p-1 ideals and q ≡ 1 (mod p) fails"
]

def conditions(witness):
    try:
        p, q = witness
    except Exception:
        return [False, False, False, False]
        
    try:
        h1 = sympy.isprime(q)
    except Exception:
        h1 = False
        
    try:
        h2 = (q != p)
    except Exception:
        h2 = False
        
    try:
        h3 = (int(p) == p) and (p >= 1)
    except Exception:
        h3 = False
        
    try:
        if not h1 or not h3:
            neg_q = False
        else:
            # The number of distinct prime ideals in the factorization of q in Q(zeta_p)
            # corresponds to the number of distinct irreducible factors of the p-th 
            # cyclotomic polynomial over GF(q).
            poly = cyclotomic_poly(int(p), x)
            factors = factor_list(poly, modulus=int(q))
            g = len(factors[1])
            
            splits_completely = (g == p - 1)
            congruence = ((q - 1) % p == 0)
            
            conclusion = (splits_completely == congruence)
            neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]