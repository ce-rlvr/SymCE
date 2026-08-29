import sympy as sp
import math

# Top-level setup for standard objects
S3 = sp.combinatorics.SymmetricGroup(3)
S4 = sp.combinatorics.SymmetricGroup(4)
A4 = sp.combinatorics.AlternatingGroup(4)
D4 = sp.combinatorics.DihedralGroup(4)
C4 = sp.combinatorics.CyclicGroup(4)
V4 = sp.combinatorics.AlternatingGroup(4)
Z2 = sp.combinatorics.CyclicGroup(2)
Z3 = sp.combinatorics.CyclicGroup(3)
Z4 = sp.combinatorics.CyclicGroup(4)
Z6 = sp.combinatorics.CyclicGroup(6)
trivial = sp.combinatorics.CyclicGroup(1)

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness (q, f) or (q, f, x), checks if it is a valid counterexample to the false conjecture.
    """
    try:
        if len(witness) == 3:
            q, f_expr, x = witness
        else:
            q, f_expr = witness
            free = f_expr.free_symbols
            x = list(free)[0] if free else sp.Symbol('x')
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field with q elements
    try:
        q_int = int(q)
        is_prime_power = False
        if q_int > 1:
            factors = sp.factorint(q_int)
            if len(factors) == 1:
                is_prime_power = True
        h1 = is_prime_power
    except Exception:
        h1 = False

    # H2: f(x) is a monic square-free polynomial of degree n over F_q
    try:
        if not h1:
            h2 = False
        else:
            p = list(sp.factorint(q_int).keys())[0]
            f_poly_p = sp.Poly(f_expr, x, domain=sp.GF(p))
            is_monic = (f_poly_p.LC() == 1)
            is_sqf = f_poly_p.is_squarefree
            h2 = bool(is_monic and is_sqf)
    except Exception:
        h2 = False

    # neg_Q: The number of distinct monic irreducible factors of f(x) over F_q 
    # is NOT equal to the dimension of the null space of Q - I
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            n = f_poly_p.degree()
            if n == 0:
                num_factors_q = 0
                nullity = 0
                neg_q = (num_factors_q != nullity)
            else:
                p = list(sp.factorint(q_int).keys())[0]
                m = 1
                temp_q = q_int
                while temp_q > p:
                    temp_q //= p
                    m += 1
                
                # Compute number of distinct irreducible factors over F_q
                factors = sp.factor_list(f_poly_p)[1]
                num_factors_q = 0
                for factor, mult in factors:
                    d = factor.degree()
                    num_factors_q += math.gcd(d, m)
                
                # Compute Berlekamp matrix Q using characteristic p
                def poly_pow_mod(base, exp, mod_poly):
                    res = sp.Poly(1, x, domain=base.domain)
                    base = base % mod_poly
                    while exp > 0:
                        if exp % 2 == 1:
                            res = (res * base) % mod_poly
                        base = (base * base) % mod_poly
                        exp //= 2
                    return res

                x_poly = sp.Poly(x, x, domain=sp.GF(p))
                Q_matrix = []
                for i in range(n):
                    rem = poly_pow_mod(x_poly, i * p, f_poly_p)
                    coeffs = rem.all_coeffs()[::-1]
                    coeffs += [0] * (n - len(coeffs))
                    Q_matrix.append(coeffs)
                
                # Compute Q - I mod p
                Q_minus_I_mod_p = []
                for i in range(n):
                    row = []
                    for j in range(n):
                        val = Q_matrix[i][j]
                        if i == j:
                            val -= 1
                        row.append(val % p)
                    Q_minus_I_mod_p.append(row)
                
                # Gaussian elimination over F_p to find rank
                def rank_mod_p(M, p):
                    rows = len(M)
                    if rows == 0: return 0
                    cols = len(M[0])
                    rank = 0
                    for c in range(cols):
                        pivot = -1
                        for r in range(rank, rows):
                            if M[r][c] % p != 0:
                                pivot = r
                                break
                        if pivot == -1:
                            continue
                        M[rank], M[pivot] = M[pivot], M[rank]
                        inv = pow(int(M[rank][c]), p - 2, p)
                        for j in range(c, cols):
                            M[rank][j] = (M[rank][j] * inv) % p
                        for r in range(rows):
                            if r != rank and M[r][c] % p != 0:
                                factor = M[r][c]
                                for j in range(c, cols):
                                    M[r][j] = (M[r][j] - factor * M[rank][j]) % p
                        rank += 1
                    return rank

                rank = rank_mod_p(Q_minus_I_mod_p, p)
                nullity = n - rank
                
                neg_q = (num_factors_q != nullity)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: f(x) is a monic square-free polynomial of degree n over F_q",
    "\u00acQ: The number of distinct monic irreducible factors of f(x) over F_q is NOT equal to the dimension of the null space of Q - I"
]

N_HYP = 2
NEG_Q_INDEX = 2