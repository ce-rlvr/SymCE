import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import sympy.polys

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple: (p, poly_coeffs, sigma_k)
    where:
      - p is a prime integer (characteristic of K and degree of L/K).
      - poly_coeffs is a list of integers representing the coefficients of an 
        irreducible polynomial of degree p over GF(p), defining L = GF(p)[x]/(poly).
      - sigma_k is an integer representing the power of the Frobenius automorphism 
        that defines sigma.
    """
    try:
        p, poly_coeffs, sigma_k = witness
        p = int(p)
        sigma_k = int(sigma_k)
        poly_coeffs = [int(c) for c in poly_coeffs]
    except Exception:
        return [False, False, False]
        
    # H_1: K is a field of prime characteristic p
    try:
        h1 = sympy.isprime(p)
    except Exception:
        h1 = False
        
    # H_2: L/K is a cyclic Galois extension of degree p
    try:
        if not h1:
            h2 = False
        else:
            x = sympy.Symbol('x')
            domain = sympy.GF(p)
            poly = sympy.Poly.from_list(poly_coeffs, gens=x, domain=domain)
            if poly.degree() != p:
                h2 = False
            else:
                h2 = poly.is_irreducible
    except Exception:
        h2 = False
        
    # Conclusion: There exists \alpha \in L such that L = K(\alpha), \sigma(\alpha) = \alpha + 1, 
    # and the minimal polynomial of \alpha over K is x^p - x - a for some a \in K.
    try:
        if not (h1 and h2):
            q = False
        else:
            x = sympy.Symbol('x')
            domain = sympy.GF(p)
            poly = sympy.Poly.from_list(poly_coeffs, gens=x, domain=domain)
            
            sigma_k = sigma_k % p
            
            def poly_pow(base_expr, exp, mod_poly):
                res = sympy.Poly(1, gens=x, domain=domain)
                base = sympy.Poly(base_expr, gens=x, domain=domain) % mod_poly
                while exp > 0:
                    if exp % 2 == 1:
                        res = (res * base) % mod_poly
                    base = (base * base) % mod_poly
                    exp //= 2
                return res

            power = pow(p, sigma_k)
            sigma_x = poly_pow(x, power, poly)
            
            # Build matrix M for the linear map \sigma over GF(p)
            M = sympy.matrices.zeros(p, p)
            current = sympy.Poly(1, gens=x, domain=domain)
            for i in range(p):
                coeffs = current.all_coeffs()
                coeffs = coeffs[::-1]
                for j in range(len(coeffs)):
                    M[j, i] = coeffs[j]
                current = (current * sigma_x) % poly

            # We want to solve \sigma(\alpha) - \alpha = 1, which is (M - I)c = e_0
            A = M - sympy.matrices.eye(p)
            b = sympy.matrices.zeros(p, 1)
            b[0, 0] = 1
            
            Aug = A.row_join(b)
            Aug_list = [[int(val) % p for val in Aug.row(i)] for i in range(p)]
            
            # Gaussian elimination over GF(p)
            for i in range(p):
                pivot = -1
                for j in range(i, p):
                    if Aug_list[j][i] % p != 0:
                        pivot = j
                        break
                if pivot == -1:
                    continue
                Aug_list[i], Aug_list[pivot] = Aug_list[pivot], Aug_list[i]
                inv = pow(int(Aug_list[i][i]), p - 2, p)
                for j in range(i, p + 1):
                    Aug_list[i][j] = (Aug_list[i][j] * inv) % p
                for j in range(p):
                    if i != j and Aug_list[j][i] % p != 0:
                        factor = Aug_list[j][i]
                        for k in range(i, p + 1):
                            Aug_list[j][k] = (Aug_list[j][k] - factor * Aug_list[i][k]) % p
                            
            solution_exists = True
            for i in range(p):
                all_zero = True
                for j in range(p):
                    if Aug_list[i][j] % p != 0:
                        all_zero = False
                        break
                if all_zero and Aug_list[i][p] % p != 0:
                    solution_exists = False
                    break
                    
            if not solution_exists:
                q = False
            else:
                # Extract one solution
                c = [0] * p
                for i in range(p):
                    pivot_col = -1
                    for j in range(p):
                        if Aug_list[i][j] % p != 0:
                            pivot_col = j
                            break
                    if pivot_col != -1:
                        c[pivot_col] = Aug_list[i][p]
                        
                alpha = sympy.Poly.from_list(c[::-1], gens=x, domain=domain)
                
                # Check if L = K(\alpha) (i.e., \alpha is not in K)
                if alpha.degree() <= 0:
                    q = False
                else:
                    # Check if minimal polynomial is x^p - x - a
                    alpha_p = poly_pow(alpha.as_expr(), p, poly)
                    a_poly = (alpha_p - alpha) % poly
                    if a_poly.degree() > 0:
                        q = False
                    else:
                        q = True
    except Exception:
        # If evaluation fails, we conservatively assume the conclusion holds to avoid false positives
        q = True
        
    neg_q = not q
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field of prime characteristic p",
    "H_2: L/K is a cyclic Galois extension of degree p",
    "¬Q: Conclusion fails (no such alpha exists for the given sigma)"
]

N_HYP = 2
NEG_Q_INDEX = 2