import sympy as sp
from sympy.abc import x

def parse_witness(witness):
    p = 0
    poly = None
    try:
        if isinstance(witness, sp.Poly):
            poly = witness
            if poly.domain.is_FiniteField:
                p = poly.domain.mod
            elif hasattr(poly.domain, 'char'):
                p = poly.domain.char
            else:
                p = 0
            return poly, p
            
        if isinstance(witness, tuple) and len(witness) == 2:
            obj, p = witness
            if p > 0:
                domain = sp.GF(p)
            else:
                domain = sp.QQ
            poly = sp.Poly(obj, x, domain=domain)
            return poly, p
            
        if isinstance(witness, list):
            poly = sp.Poly(witness, x, domain=sp.QQ)
            return poly, 0
            
        if isinstance(witness, sp.Expr):
            poly = sp.Poly(witness, x, domain=sp.QQ)
            return poly, 0
            
    except Exception:
        pass
    return poly, p

def conditions(witness) -> list[bool]:
    try:
        poly, p = parse_witness(witness)
        if poly is None:
            return [False, False, False]
            
        if p != 0 and not sp.isprime(p):
            return [False, False, False]
            
        n = poly.degree()
        if n < 1:
            return [False, False, False]
            
        # H_1: E is a finite field extension of F
        # Represented by an irreducible polynomial over F
        h1 = poly.is_irreducible
        
        # H_2: E/F is a separable extension
        # An irreducible polynomial is separable iff its formal derivative is not identically zero
        deriv = poly.diff()
        h2 = h1 and not deriv.is_zero
        
        # ¬Q: The field trace map Tr_{E/F}: E \to F is not surjective
        # The trace map is surjective iff it is not identically zero.
        # We check if Tr(x^k) != 0 for some k in 0..n-1.
        if p == 0 or n % p != 0:
            # Tr(1) = n != 0, so it is surjective
            is_surjective = True
        else:
            monic_poly = poly.monic()
            monic_coeffs = monic_poly.all_coeffs()
            
            s = [0] * n
            s[0] = 0  # since n % p == 0
            is_surjective = False
            
            # Use Newton's identities to find the traces of powers of x
            for k in range(1, n):
                term_sum = 0
                for i in range(1, k):
                    term_sum += monic_coeffs[i] * s[k - i]
                term_sum += k * monic_coeffs[k]
                
                s_k = -term_sum
                
                is_z = False
                if hasattr(s_k, 'is_zero') and s_k.is_zero is not None:
                    is_z = s_k.is_zero
                else:
                    try:
                        is_z = (int(s_k) % p == 0)
                    except Exception:
                        is_z = (s_k == 0)
                        
                if not is_z:
                    is_surjective = True
                    break
                s[k] = s_k
                
        neg_q = not is_surjective
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: E is a finite field extension of F",
    "H_2: E/F is a separable extension",
    "¬Q: The field trace map Tr_{E/F}: E \\to F is not surjective"
]

N_HYP = 2
NEG_Q_INDEX = 2