import itertools
from sympy import Matrix, Poly, symbols
from sympy.abc import x
from sympy.ntheory import isprime, factorint

# Standard named bindings
I2 = Matrix.eye(2)
I3 = Matrix.eye(3)
O2 = Matrix.zeros(2, 2)
O3 = Matrix.zeros(3, 3)

def conditions(witness):
    try:
        q = witness['q']
        n = witness['n']
        alphas = witness['alphas']
        M = witness['M']
        p = witness.get('p', q)
        modulus = witness.get('modulus', 0)
        
        if not isinstance(M, Matrix):
            M = Matrix(M)
            
        # H_1: Fq is a finite field with q elements
        factors = factorint(q)
        h1 = len(factors) == 1 and p in factors and isprime(p)
        
        # H_2: n is a positive integer
        h2 = isinstance(n, int) and n > 0 and len(alphas) == n and M.shape == (n, n)
        
        # Helper to check equality in the ring R = F_p[x]/(modulus) or F_p
        if hasattr(modulus, 'free_symbols') and modulus.free_symbols:
            var = list(modulus.free_symbols)[0]
            def is_zero(expr):
                try:
                    poly = Poly(expr, var, domain=f'GF({p})')
                    mod_poly = Poly(modulus, var, domain=f'GF({p})')
                    return (poly % mod_poly).is_zero
                except Exception:
                    return False
        else:
            def is_zero(expr):
                try:
                    return (int(expr) % p) == 0
                except Exception:
                    return False

        # H_3: M is the n x n Moore matrix defined by M_{i,j} = alpha_i^{q^{j-1}}
        h3 = True
        for i in range(n):
            for j in range(n):
                # j is 0-indexed, so q**j corresponds to q^{j+1-1}
                diff = M[i, j] - alphas[i]**(q**j)
                if not is_zero(diff):
                    h3 = False
                    break
                    
        # Check linear independence over Fq
        Fq_elements = witness.get('Fq_elements', list(range(p)))
        if len(Fq_elements) != q:
            is_indep = False
        else:
            is_indep = True
            for coeffs in itertools.product(Fq_elements, repeat=n):
                if all(c == 0 or is_zero(c) for c in coeffs):
                    continue
                comb = sum(c * a for c, a in zip(coeffs, alphas))
                if is_zero(comb):
                    is_indep = False
                    break
                    
        # Check determinant
        det_M = M.det()
        det_nonzero = not is_zero(det_M)
        
        # ¬Q: The conclusion FAILS
        # Conclusion is: det(M) != 0 iff alphas are linearly independent over Fq
        neg_q_cond = bool(det_nonzero != is_indep)
        
        return [bool(h1), bool(h2), bool(h3), neg_q_cond]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: Fq is a finite field with q elements",
    "H_2: n is a positive integer",
    "H_3: M is the n x n Moore matrix",
    "¬Q: det(M) != 0 iff alphas are linearly independent over Fq FAILS"
]

N_HYP = 3
NEG_Q_INDEX = 3