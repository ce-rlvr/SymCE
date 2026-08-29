import sympy as sp
from sympy.abc import x
from sympy import Poly, Rational, GF, QQ, ZZ, RR, CC
import math

# Top-level setup
# Standard fields and the symbol x are provided for witness construction.
# A witness can be a SymPy Poly, an Expr, or a tuple (domain, expr).

def is_kth_power(c, k, domain):
    if k == 1:
        return True
    if domain.is_QQ:
        from sympy import integer_nthroot
        try:
            c_rat = Rational(c)
            if c_rat < 0 and k % 2 == 0:
                return False
            num_root, num_exact = integer_nthroot(abs(c_rat.p), k)
            den_root, den_exact = integer_nthroot(c_rat.q, k)
            return num_exact and den_exact
        except Exception:
            return False
    elif hasattr(domain, 'order'):
        try:
            q = domain.order
            if c == domain.zero or c == 0:
                return True
            gcd_val = math.gcd(k, q - 1)
            power = (q - 1) // gcd_val
            
            if hasattr(domain, 'mod') and domain.order == domain.mod:
                p = domain.mod
                c_val = int(c) % p
                return pow(c_val, power, p) == 1
            else:
                return (c ** power) == domain.one
        except Exception:
            return False
    elif domain.is_RR:
        try:
            return float(c) >= 0 or k % 2 != 0
        except Exception:
            return False
    elif domain.is_CC:
        return True
    else:
        return False

def parse_witness(witness):
    if isinstance(witness, tuple):
        domain, expr = witness
        if isinstance(expr, Poly):
            poly = expr
        else:
            poly = Poly(expr, x, domain=domain)
    elif isinstance(witness, Poly):
        poly = witness
    else:
        poly = Poly(witness, x)
        # Promote ZZ to QQ since the conjecture requires a field
        if poly.domain == ZZ:
            poly = Poly(witness, x, domain=QQ)
    return poly

def conditions(witness) -> list[bool]:
    try:
        poly = parse_witness(witness)
        F = poly.domain
        H_1 = bool(F.is_Field)
    except Exception:
        H_1 = False

    try:
        if not H_1:
            neg_Q = False
        else:
            if poly.is_zero or poly.degree() <= 0:
                # The zero ring and F polynomials itself are not local rings.
                # Constants and 0 are not powers of a single irreducible polynomial.
                is_local = False
                is_power = False
            else:
                c, factors = poly.factor_list()
                # Factor ring is local iff f has exactly one distinct irreducible factor
                is_local = (len(factors) == 1)
                
                if len(factors) == 1:
                    p1, k1 = factors[0]
                    # f is a power of an irreducible polynomial iff its leading coefficient
                    # is a k1-th power in the field F.
                    is_power = is_kth_power(c, k1, F)
                else:
                    is_power = False
            
            # The conclusion is an iff statement, so its negation is an XOR
            neg_Q = bool(is_local != is_power)
    except Exception:
        neg_Q = False

    return [H_1, neg_Q]

CONDITION_LABELS = [
    "H_1: F is a field",
    "neg_Q: factor ring is local XOR f is a power of a single irreducible polynomial"
]

N_HYP = 1
NEG_Q_INDEX = 1