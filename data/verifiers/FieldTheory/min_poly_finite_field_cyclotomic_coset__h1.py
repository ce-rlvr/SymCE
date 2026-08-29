import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
x, t = sympy.symbols('x t')

def conditions(witness) -> list[bool]:
    """
    witness is expected to be a tuple: (q, m_coeffs, alpha_coeffs, d)
    where:
      - q is a prime power (the size of the base field F_q)
      - m_coeffs are the coefficients of an irreducible polynomial m(t) over F_q, defining the extension field
      - alpha_coeffs are the coefficients of alpha(t) in F_q[t]/(m(t))
      - d is the integer to test
    """
    try:
        q, m_coeffs, alpha_coeffs, d = witness
        q = int(q)
        d = int(d)
        
        # H1: alpha is an element of an extension field of F_q
        if not sympy.ntheory.isprimepower(q):
            return [False, False, False]
            
        domain = sympy.GF(q)
        
        m_poly = sympy.Poly(m_coeffs, t, domain=domain)
        if not m_poly.is_irreducible:
            h1 = False
        else:
            h1 = True
            
        alpha_poly = sympy.Poly(alpha_coeffs, t, domain=domain)
        
        # H2: d is the smallest positive integer such that alpha^{q^d} = alpha
        h2 = False
        if h1 and d > 0:
            def get_alpha_qd(i):
                res = sympy.Poly(1, t, domain=domain)
                base = alpha_poly
                p = q**i
                while p > 0:
                    if p % 2 == 1:
                        res = (res * base) % m_poly
                    base = (base * base) % m_poly
                    p //= 2
                return res

            smallest_d = None
            for i in range(1, d + 1):
                val = get_alpha_qd(i)
                if val == (alpha_poly % m_poly):
                    smallest_d = i
                    break
            
            if smallest_d == d:
                h2 = True
                
        # neg_Q: The minimal polynomial of alpha over F_q is NOT given by the product
        neg_q = False
        if h1 and h2:
            roots = [get_alpha_qd(i) for i in range(d)]
            
            # Compute the product \prod_{i=0}^{d-1} (x - alpha^{q^i})
            prod_coeffs = [sympy.Poly(1, t, domain=domain)]
            for r in roots:
                new_coeffs = [sympy.Poly(0, t, domain=domain) for _ in range(len(prod_coeffs) + 1)]
                for i in range(len(prod_coeffs)):
                    new_coeffs[i+1] = (new_coeffs[i+1] + prod_coeffs[i]) % m_poly
                    term = (prod_coeffs[i] * r) % m_poly
                    new_coeffs[i] = (new_coeffs[i] - term) % m_poly
                prod_coeffs = new_coeffs
            
            prod_coeffs = prod_coeffs[::-1]
            
            is_in_Fq = True
            fq_coeffs = []
            for c in prod_coeffs:
                if c.degree() > 0:
                    is_in_Fq = False
                    break
                if c.is_zero:
                    fq_coeffs.append(domain.zero)
                else:
                    fq_coeffs.append(domain.from_sympy(c.nth(0)))
            
            if not is_in_Fq:
                neg_q = True
            else:
                deg_m = m_poly.degree()
                vecs = []
                curr = sympy.Poly(1, t, domain=domain)
                for _ in range(d + 1):
                    vec = []
                    for i in range(deg_m):
                        if curr.is_zero:
                            vec.append(domain.zero)
                        else:
                            vec.append(domain.from_sympy(curr.nth(i)))
                    vecs.append(vec)
                    curr = (curr * alpha_poly) % m_poly
                
                # Evaluate the product polynomial at alpha
                val_prod = sympy.Poly(0, t, domain=domain)
                for c in fq_coeffs:
                    val_prod = (val_prod * alpha_poly + sympy.Poly(domain.to_sympy(c), t, domain=domain)) % m_poly
                
                if not val_prod.is_zero:
                    neg_q = True
                else:
                    # Check if there is a polynomial of smaller degree that evaluates to 0
                    # by computing the rank of the vectors 1, alpha, ..., alpha^{d-1}
                    mat = [list(v) for v in vecs[:d]]
                    rows = len(mat)
                    cols = len(mat[0]) if rows > 0 else 0
                    rank = 0
                    for c in range(cols):
                        pivot = -1
                        for r in range(rank, rows):
                            if not domain.is_zero(mat[r][c]):
                                pivot = r
                                break
                        if pivot != -1:
                            mat[rank], mat[pivot] = mat[pivot], mat[rank]
                            inv = domain.invert(mat[rank][c])
                            for j in range(c, cols):
                                mat[rank][j] = domain.mul(mat[rank][j], inv)
                            for r in range(rows):
                                if r != rank and not domain.is_zero(mat[r][c]):
                                    factor = mat[r][c]
                                    for j in range(c, cols):
                                        term = domain.mul(factor, mat[rank][j])
                                        mat[r][j] = domain.sub(mat[r][j], term)
                            rank += 1
                            if rank == rows:
                                break
                    
                    if rank < d:
                        neg_q = True
                    else:
                        neg_q = False
                        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: alpha is an element of an extension field of F_q",
    "H_2: d is the smallest positive integer such that alpha^{q^d} = alpha",
    "¬Q: The minimal polynomial of alpha over F_q is NOT given by the product"
]

N_HYP = 2
NEG_Q_INDEX = 2