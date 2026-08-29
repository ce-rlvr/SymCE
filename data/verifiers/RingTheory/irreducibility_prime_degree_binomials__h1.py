import sympy
import math
import re
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Top-level setup for potential witness references
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

CONDITION_LABELS = [
    "H_1: p is a prime number",
    "H_2: a is an element of F",
    "H_3: There does not exist any element c in F such that c^p = a",
    "¬Q: The polynomial x^p - a is reducible over F"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    n, p, a, factors = None, None, None, None
    
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
            a = witness.get('a')
            factors = witness.get('factors')
            if n is None and 'ring' in witness:
                m = re.search(r'\d+', str(witness['ring']))
                if m:
                    n = int(m.group())
        elif isinstance(witness, (list, tuple)):
            if len(witness) >= 3:
                n, p, a = witness[0], witness[1], witness[2]
            if len(witness) >= 4:
                factors = witness[3]
            if len(witness) >= 5 and not isinstance(factors, (list, tuple)):
                factors = [witness[3], witness[4]]
        else:
            n = getattr(witness, 'n', None)
            p = getattr(witness, 'p', None)
            a = getattr(witness, 'a', None)
            factors = getattr(witness, 'factors', None)
    except Exception:
        pass

    # H1: p is prime
    try:
        p_val = int(p)
        h1 = sympy.isprime(p_val)
    except Exception:
        h1 = False
        p_val = None

    # H2: a in F (we assume F is Z/nZ, so n > 1 and a is an integer)
    try:
        n_val = int(n)
        a_val = int(a)
        h2 = (n_val > 1)
    except Exception:
        h2 = False
        n_val = None
        a_val = None

    # H3: no c in F such that c^p = a
    try:
        if h2 and h1:
            h3 = True
            a_mod = a_val % n_val
            for c in range(n_val):
                if pow(c, p_val, n_val) == a_mod:
                    h3 = False
                    break
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: x^p - a is reducible over F
    neg_q = False
    try:
        if h2 and h1:
            # Over Z/nZ, if n has >= 2 distinct prime factors, x^p - a is ALWAYS reducible.
            # Proof: Z/nZ = R1 x R2. x^p - a = (x^p - a, 1) * (1, x^p - a).
            # Neither factor is a unit because the leading coefficient (1, 0) is not nilpotent.
            factors_n = sympy.factorint(n_val)
            if len(factors_n) > 1:
                neg_q = True
            
            # If not neg_q yet, check provided factors (e.g., if n is a prime power)
            if not neg_q and p_val <= 10000 and factors is not None and len(factors) >= 2:
                A = factors[0]
                B = factors[1]
                
                def strip_zeros(poly, mod):
                    res = [int(x) % mod for x in poly]
                    while len(res) > 1 and res[-1] == 0:
                        res.pop()
                    if len(res) == 1 and res[0] == 0:
                        return []
                    return res

                def is_unit(poly, mod):
                    if not poly: return False
                    if math.gcd(poly[0], mod) != 1: return False
                    primes = list(sympy.factorint(mod).keys())
                    for c in poly[1:]:
                        for q in primes:
                            if c % q != 0:
                                return False
                    return True

                def poly_mul(poly1, poly2, mod):
                    if not poly1 or not poly2: return []
                    res = [0] * (len(poly1) + len(poly2) - 1)
                    for i, c1 in enumerate(poly1):
                        for j, c2 in enumerate(poly2):
                            res[i+j] = (res[i+j] + c1 * c2) % mod
                    return strip_zeros(res, mod)

                A_asc = strip_zeros(A, n_val)
                B_asc = strip_zeros(B, n_val)
                A_desc = strip_zeros(A[::-1], n_val)
                B_desc = strip_zeros(B[::-1], n_val)

                target = [0] * (p_val + 1)
                target[0] = (-a_val) % n_val
                target[-1] = 1 % n_val
                target = strip_zeros(target, n_val)

                if not is_unit(A_asc, n_val) and not is_unit(B_asc, n_val):
                    if poly_mul(A_asc, B_asc, n_val) == target:
                        neg_q = True
                
                if not neg_q and not is_unit(A_desc, n_val) and not is_unit(B_desc, n_val):
                    if poly_mul(A_desc, B_desc, n_val) == target:
                        neg_q = True
    except Exception:
        pass

    return [h1, h2, h3, neg_q]