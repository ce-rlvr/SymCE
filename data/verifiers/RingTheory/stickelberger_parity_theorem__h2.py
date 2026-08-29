import sympy as sp
from sympy.abc import x

# Top-level setup for witness expressions
# The witness is expected to be a dictionary: {'q': int, 'f': expr, 'n': int, 'r': int}
# or a tuple: (q, f_expr, n, r)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            f_expr = witness.get('f')
            n = witness.get('n')
            r = witness.get('r')
        else:
            q, f_expr, n, r = witness
    except Exception:
        return [False, False, False, False]

    # H1: F_q is a finite field of odd characteristic
    try:
        q = int(q)
        if q < 3 or q % 2 == 0:
            h1 = False
        else:
            factors = sp.factorint(q)
            h1 = len(factors) == 1
    except Exception:
        h1 = False

    # H2: f(x) has distinct roots in its splitting field over F_q
    try:
        factors = sp.factorint(q)
        p = list(factors.keys())[0]
        
        # We evaluate over F_p. If q is a prime power, we assume the witness 
        # provides a polynomial with coefficients in F_p (which is a subfield of F_q).
        f_poly = sp.Poly(f_expr, x, domain=sp.FF(p))
        f_deriv = f_poly.diff()
        gcd_poly = f_poly.gcd(f_deriv)
        h2 = gcd_poly.degree() == 0
    except Exception:
        h2 = False

    # H3: r is the number of irreducible factors of f(x) over F_q
    try:
        if q == p:
            # For prime fields, sympy can factor directly
            _, fac_list = sp.factor_list(f_poly)
            actual_r = sum(mult for _, mult in fac_list)
            h3 = (r == actual_r)
        else:
            # For prime power fields F_q where q = p^k (k > 1), we count irreducible factors
            # using Distinct Degree Factorization (DDF) logic.
            # Since f is square-free (from H2), gcd(f, x^(q^i) - x) gives the product of all 
            # irreducible factors of degree dividing i.
            rem_f = f_poly
            actual_r = 0
            i = 1
            x_poly = sp.Poly(x, x, domain=sp.FF(p))
            while rem_f.degree() > 0:
                # Compute x^(q^i) mod rem_f
                x_qi = pow(x_poly, q**i, rem_f)
                # gcd(rem_f, x^(q^i) - x)
                gcd_i = rem_f.gcd(x_qi - x_poly)
                deg_gcd = gcd_i.degree()
                if deg_gcd > 0:
                    actual_r += deg_gcd // i
                    rem_f = rem_f.quo(gcd_i)
                i += 1
            h3 = (r == actual_r)
    except Exception:
        h3 = False

    # Conclusion: n = r mod 2 iff discriminant of f(x) is a non-zero square in F_q
    try:
        p = list(sp.factorint(q).keys())[0]
        k = list(sp.factorint(q).values())[0]
        
        f_poly = sp.Poly(f_expr, x, domain=sp.FF(p))
        disc_val = f_poly.discriminant()
        disc_int = int(disc_val) % p
        
        is_square = False
        if disc_int != 0:
            if k % 2 == 0:
                # In F_{p^k} with k even, every element of F_p is a square
                is_square = True
            else:
                # In F_{p^k} with k odd, an element of F_p is a square iff it is a square in F_p
                is_square = pow(disc_int, (p - 1) // 2, p) == 1
                
        lhs = (int(n) % 2) == (int(r) % 2)
        rhs = is_square and (disc_int != 0)
        
        conclusion = (lhs == rhs)
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1, h2, h3, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F_q is a finite field of odd characteristic",
    "H_2: f(x) has distinct roots in its splitting field over F_q",
    "H_3: r is the number of irreducible factors of f(x) over F_q",
    "¬Q: The equivalence (n ≡ r mod 2 iff discriminant is a non-zero square) fails"
]

N_HYP = 3
NEG_Q_INDEX = 3