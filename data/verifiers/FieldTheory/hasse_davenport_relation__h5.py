import sympy
from sympy import Poly, isprime, exp, I, pi
from sympy.abc import x
from sympy.polys.domains import GF
import itertools

# Top-level setup
x_sym = x

def conditions(witness):
    """
    witness is expected to be a dictionary with:
      'q': prime number (order of F)
      'n': degree of extension E over F
      'P': list of coefficients of an irreducible polynomial of degree n over F_q (highest degree first)
      'chi': list of length q representing the multiplicative character on F (chi[0] to chi[q-1])
      'chi_prime': dict mapping n-tuples (elements of E) to their character values
      'c': integer in [1, q-1] defining the additive character on F: psi(x) = exp(2*pi*i*c*x/q)
      'c_prime': n-tuple defining the additive character on E: psi'(x) = exp(2*pi*i*Tr(c_prime * x)/q)
    """
    try:
        q = witness['q']
        n = witness['n']
        P_coeffs = witness['P']
        chi = witness['chi']
        chi_prime = witness['chi_prime']
        c = witness['c']
        c_prime = witness['c_prime']
    except (TypeError, KeyError):
        return [False] * 4 + [False]

    # H_1: F is a finite field of order q
    # For simplicity in this verifier, we restrict to prime fields F_q
    try:
        h1 = isprime(q)
    except Exception:
        h1 = False

    # H_2: E is a finite field extension of F of degree n
    try:
        if len(P_coeffs) != n + 1:
            h2 = False
        else:
            P_poly = Poly(P_coeffs, x, domain=GF(q))
            h2 = P_poly.is_irreducible
    except Exception:
        h2 = False

    # H_3: chi is a non-trivial multiplicative character of F
    try:
        h3 = True
        if len(chi) != q:
            h3 = False
        elif abs(complex(sympy.N(chi[0]))) > 1e-7:
            h3 = False
        elif abs(complex(sympy.N(chi[1] - 1))) > 1e-7:
            h3 = False
        else:
            # Check multiplicativity
            for i in range(q):
                for j in range(q):
                    diff = complex(sympy.N(chi[(i * j) % q] - chi[i] * chi[j]))
                    if abs(diff) > 1e-7:
                        h3 = False
            # Check non-triviality
            is_trivial = True
            for i in range(1, q):
                if abs(complex(sympy.N(chi[i] - 1))) > 1e-7:
                    is_trivial = False
                    break
            if is_trivial:
                h3 = False
    except Exception:
        h3 = False

    # H_4: chi' is the lifted multiplicative character on E defined by chi' = chi o N_{E/F}
    try:
        h4 = True
        elements = list(itertools.product(range(q), repeat=n))
        
        def mul_E(A_coeffs, B_coeffs):
            A = Poly(A_coeffs, x, domain=GF(q))
            B = Poly(B_coeffs, x, domain=GF(q))
            res = (A * B) % P_poly
            res_coeffs = res.all_coeffs()
            res_coeffs = [0] * (n - len(res_coeffs)) + res_coeffs
            return tuple(int(val) for val in res_coeffs)

        def norm_E(A_coeffs):
            if all(val == 0 for val in A_coeffs):
                return 0
            res = [0] * (n - 1) + [1]
            cur = A_coeffs
            for _ in range(n):
                res = mul_E(res, cur)
                cur_q = [0] * (n - 1) + [1]
                base = cur
                power = q
                while power > 0:
                    if power % 2 == 1:
                        cur_q = mul_E(cur_q, base)
                    base = mul_E(base, base)
                    power //= 2
                cur = cur_q
            return res[-1] % q

        for elem in elements:
            expected = chi[norm_E(elem)]
            actual = chi_prime.get(elem)
            if actual is None:
                h4 = False
                break
            diff = complex(sympy.N(actual - expected))
            if abs(diff) > 1e-7:
                h4 = False
                break
    except Exception:
        h4 = False

    # ¬Q: -g(chi') != (-g(chi))^n
    try:
        # Compute g(chi) over F
        g_chi = 0
        for i in range(1, q):
            g_chi += chi[i] * exp(2 * I * pi * c * i / q)
        
        def trace_E(A_coeffs):
            res = [0] * n
            cur = A_coeffs
            for _ in range(n):
                res = [(r + c_val) % q for r, c_val in zip(res, cur)]
                cur_q = [0] * (n - 1) + [1]
                base = cur
                power = q
                while power > 0:
                    if power % 2 == 1:
                        cur_q = mul_E(cur_q, base)
                    base = mul_E(base, base)
                    power //= 2
                cur = cur_q
            return res[-1] % q

        # Compute g(chi') over E
        g_chi_prime = 0
        for elem in elements:
            if all(val == 0 for val in elem):
                continue
            cx = mul_E(c_prime, elem)
            tr = trace_E(cx)
            g_chi_prime += chi_prime[elem] * exp(2 * I * pi * tr / q)
        
        lhs = -g_chi_prime
        rhs = (-g_chi)**n
        
        diff = complex(sympy.N(lhs - rhs))
        neg_q_ok = abs(diff) > 1e-7
        
        # Ensure the additive characters chosen are non-trivial
        if c % q == 0:
            neg_q_ok = False
        if all(val % q == 0 for val in c_prime):
            neg_q_ok = False

    except Exception:
        neg_q_ok = False

    return [h1, h2, h3, h4, neg_q_ok]

CONDITION_LABELS = [
    "H_1: F is a finite field of order q",
    "H_2: E is a finite field extension of F of degree n",
    "H_3: chi is a non-trivial multiplicative character of F",
    "H_4: chi' is the lifted multiplicative character on E defined by chi' = chi o N_{E/F}",
    "¬Q: -g(chi') != (-g(chi))^n"
]

N_HYP = 4
NEG_Q_INDEX = 4