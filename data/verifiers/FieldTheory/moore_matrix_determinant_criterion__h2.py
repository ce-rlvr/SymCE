import itertools
from sympy import Poly, GF
from sympy.abc import x
from sympy.ntheory import isprime

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: alpha_1, alpha_2, ..., alpha_n are elements of the extension field F_{q^n}",
    "H_3: M is the n x n Moore matrix defined by M_{i,j} = alpha_i^{q^{j-1}}",
    "¬Q: The determinant of M is non-zero iff alpha_1, ..., alpha_n are linearly independent over F_q FAILS"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    q = witness.get('q')
    n = witness.get('n')
    p = witness.get('p')
    m = witness.get('m')
    minpoly_coeffs = witness.get('minpoly')
    alphas_coeffs = witness.get('alphas')
    
    h1 = False
    try:
        if isinstance(p, int) and isprime(p) and isinstance(m, int) and m >= 1:
            if q == p**m:
                h1 = True
    except Exception:
        pass

    h2 = False
    try:
        if h1 and isinstance(n, int) and n >= 1:
            Fp = GF(p)
            minpoly = Poly.from_list(minpoly_coeffs, gens=x, domain=Fp)
            if minpoly.degree() == m * n and minpoly.is_irreducible:
                if isinstance(alphas_coeffs, list) and len(alphas_coeffs) == n:
                    valid = True
                    for c in alphas_coeffs:
                        if not isinstance(c, list):
                            valid = False
                            break
                        Poly.from_list(c, gens=x, domain=Fp)
                    if valid:
                        h2 = True
    except Exception:
        pass

    h3 = True

    neg_q = False
    try:
        if not (h1 and h2):
            return [h1, h2, h3, False]
            
        if q**n > 2048:
            return [h1, h2, h3, False]
            
        Fp = GF(p)
        minpoly = Poly.from_list(minpoly_coeffs, gens=x, domain=Fp)
        alphas = [Poly.from_list(c, gens=x, domain=Fp) for c in alphas_coeffs]
        
        M = []
        for i in range(n):
            row = []
            for j in range(n):
                power = q**j
                res = Poly(1, gens=x, domain=Fp)
                base = alphas[i]
                exp = power
                while exp > 0:
                    if exp % 2 == 1:
                        res = (res * base) % minpoly
                    base = (base * base) % minpoly
                    exp //= 2
                row.append(res)
            M.append(row)
            
        det_M = Poly(0, gens=x, domain=Fp)
        for perm in itertools.permutations(range(n)):
            inv = 0
            for i in range(n):
                for j in range(i+1, n):
                    if perm[i] > perm[j]:
                        inv += 1
            sign = 1 if inv % 2 == 0 else -1
            
            term = Poly(sign, gens=x, domain=Fp)
            for i in range(n):
                term = (term * M[i][perm[i]]) % minpoly
            det_M = (det_M + term) % minpoly
            
        is_det_nonzero = not det_M.is_zero
        
        F_q_elements = []
        for coeffs in itertools.product(range(p), repeat=m*n):
            poly = Poly.from_list(coeffs, gens=x, domain=Fp)
            res = Poly(1, gens=x, domain=Fp)
            base = poly
            exp = q
            while exp > 0:
                if exp % 2 == 1:
                    res = (res * base) % minpoly
                base = (base * base) % minpoly
                exp //= 2
            if (res - poly) % minpoly == Poly(0, gens=x, domain=Fp):
                F_q_elements.append(poly)
                
        is_lin_indep = True
        for coeffs in itertools.product(F_q_elements, repeat=n):
            if all(c.is_zero for c in coeffs):
                continue
            
            lin_comb = Poly(0, gens=x, domain=Fp)
            for c, a in zip(coeffs, alphas):
                term = (c * a) % minpoly
                lin_comb = (lin_comb + term) % minpoly
                
            if lin_comb.is_zero:
                is_lin_indep = False
                break
                
        neg_q = (is_det_nonzero != is_lin_indep)
        
    except Exception:
        pass

    return [h1, h2, h3, neg_q]