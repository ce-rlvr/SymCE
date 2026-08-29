import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, CyclicGroup, AlternatingGroup, DihedralGroup
from sympy.matrices import eye, zeros
from sympy import cyclotomic_poly, Dummy
import math

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks if it is a valid counterexample to the false conjecture.
    The dropped hypothesis is that zeta_n is a primitive n-th root of unity.
    Without it, zeta_n can be any number (e.g., a rational number like 2),
    making the Frobenius automorphism the identity, but the conclusion fails.
    """
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            zeta_n = witness.get('zeta_n')
            sigma_p = witness.get('sigma_p')
        else:
            n, p, zeta_n, sigma_p = witness
    except Exception:
        return [False, False, False, False]

    # H1: n is a positive integer
    try:
        if isinstance(n, int):
            h1 = bool(n > 0)
        elif hasattr(n, 'is_Integer') and n.is_Integer:
            h1 = bool(n > 0)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: p is a prime number that does not divide n
    try:
        h2 = bool(sympy.isprime(p) and (n % p != 0))
    except Exception:
        h2 = False

    # H3: sigma_p is the Frobenius automorphism at p in Gal(Q(zeta_n)/Q)
    try:
        h3 = False
        if callable(sigma_p):
            val = sigma_p(zeta_n)
            is_rat = False
            if isinstance(zeta_n, (int, float)):
                is_rat = True
            elif hasattr(zeta_n, 'is_Rational') and zeta_n.is_Rational:
                is_rat = True
                
            if is_rat:
                # If zeta_n is rational, Q(zeta_n) = Q.
                # The only automorphism of Q is the identity.
                h3 = bool(val == zeta_n)
            else:
                # If zeta_n is a primitive n-th root of unity, check if sigma_p acts correctly
                x = Dummy('x')
                poly = cyclotomic_poly(n, x)
                subbed = poly.subs(x, zeta_n)
                if hasattr(subbed, 'simplify'):
                    is_root = bool(subbed.simplify() == 0)
                else:
                    is_root = bool(subbed == 0)
                    
                if is_root:
                    diff = val - zeta_n**p
                    if hasattr(diff, 'simplify'):
                        h3 = bool(diff.simplify() == 0)
                    else:
                        h3 = bool(diff == 0)
    except Exception:
        h3 = False

    # neg_Q: sigma_p(zeta_n) != zeta_n**p
    try:
        neg_q = False
        if callable(sigma_p):
            val = sigma_p(zeta_n)
            diff = val - zeta_n**p
            if hasattr(diff, 'simplify'):
                neg_q = bool(diff.simplify() != 0)
            else:
                neg_q = bool(diff != 0)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: p is a prime number that does not divide n",
    "H_3: sigma_p is the Frobenius automorphism at p in Gal(Q(zeta_n)/Q)",
    "¬Q: sigma_p(zeta_n) != zeta_n**p"
]

N_HYP = 3
NEG_Q_INDEX = 3