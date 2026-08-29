import sympy
from sympy import Poly, diff, lcm, Rational
from sympy.polys.polytools import factor_list
from sympy.polys.domains import ZZ, QQ
from sympy.ntheory import isprime
from sympy.abc import x
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    # H1: f(x) is a non-constant polynomial
    h1_ok = False
    try:
        if isinstance(witness, sympy.Poly):
            f = witness
            h1_ok = f.degree() >= 1
        elif isinstance(witness, sympy.Expr):
            symbols = witness.free_symbols
            if len(symbols) == 1:
                gen = list(symbols)[0]
            elif len(symbols) == 0:
                gen = sympy.Symbol('x')
            else:
                gen = None
            if gen is not None:
                f = sympy.Poly(witness, gen)
                h1_ok = f.degree() >= 1
    except Exception:
        h1_ok = False

    # H2: K is the splitting field of f(x) over F
    h2_ok = True

    # H3: L is the splitting field of f'(x) over F
    h3_ok = True

    # Conclusion: L is a subfield of K
    # We want neg_Q to be True if L is NOT a subfield of K
    l_subset_k = True
    try:
        if h1_ok:
            if isinstance(witness, sympy.Poly):
                f = witness
                gen = f.gen
            else:
                symbols = witness.free_symbols
                gen = list(symbols)[0] if len(symbols) == 1 else sympy.Symbol('x')
                f = sympy.Poly(witness, gen)
                
            f_prime = f.diff()
            if f_prime.degree() > 0:
                domain = f.domain
                
                # Clear denominators if over QQ to work over ZZ
                if domain == QQ:
                    lcm_den = 1
                    for coeff in f.coeffs():
                        if isinstance(coeff, sympy.Rational):
                            lcm_den = lcm(lcm_den, coeff.q)
                    f = f * lcm_den
                    f = f.set_domain(ZZ)
                    f_prime = f.diff()
                    domain = ZZ

                if domain.is_FiniteField:
                    factors_f = factor_list(f)[1]
                    k = 1
                    for fac, mult in factors_f:
                        k = lcm(k, fac.degree())
                        
                    factors_fp = factor_list(f_prime)[1]
                    m = 1
                    for fac, mult in factors_fp:
                        m = lcm(m, fac.degree())
                        
                    l_subset_k = (k % m == 0)

                elif domain == ZZ:
                    try:
                        f_sqf = f.sqf_part()
                        fp_sqf = f_prime.sqf_part()
                        disc_f = f_sqf.discriminant()
                        disc_fp = fp_sqf.discriminant()
                    except Exception:
                        disc_f = 1
                        disc_fp = 1

                    primes_checked = 0
                    p = 2
                    # Check splitting field degrees modulo unramified primes
                    # By Chebotarev density, if L is not a subfield of K, there exists a prime p
                    # where the splitting field degree of f' does not divide that of f.
                    while primes_checked < 100 and p < 2000:
                        p += 1
                        if not isprime(p):
                            continue
                            
                        lc_f = f.LC()
                        lc_fp = f_prime.LC()
                        if lc_f % p == 0 or lc_fp % p == 0:
                            continue
                            
                        if disc_f != 0 and disc_f % p == 0:
                            continue
                        if disc_fp != 0 and disc_fp % p == 0:
                            continue
                            
                        try:
                            f_mod = f.set_domain(sympy.GF(p))
                            fp_mod = f_prime.set_domain(sympy.GF(p))
                        except Exception:
                            continue
                            
                        factors_f = factor_list(f_mod)[1]
                        k_p = 1
                        for fac, mult in factors_f:
                            k_p = lcm(k_p, fac.degree())
                            
                        factors_fp = factor_list(fp_mod)[1]
                        m_p = 1
                        for fac, mult in factors_fp:
                            m_p = lcm(m_p, fac.degree())
                            
                        if k_p % m_p != 0:
                            l_subset_k = False
                            break
                            
                        primes_checked += 1
    except Exception:
        # If evaluation fails, assume L is a subfield to avoid false positives
        l_subset_k = True

    neg_q = not l_subset_k

    return [h1_ok, h2_ok, h3_ok, neg_q]

CONDITION_LABELS = [
    "H_1: f(x) is a non-constant polynomial",
    "H_2: K is the splitting field of f(x) over F",
    "H_3: L is the splitting field of f'(x) over F",
    "¬Q: L is not a subfield of K"
]

N_HYP = 3
NEG_Q_INDEX = 3