import sympy
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    try:
        # Parse witness
        if isinstance(witness, dict):
            n = int(witness.get('n', 0))
            if 'p' in witness:
                p = int(witness['p'])
            elif 'F' in witness and hasattr(witness['F'], 'characteristic'):
                p = int(witness['F'].characteristic())
            else:
                p = 0
            a = int(witness.get('a', 0))
            alpha = witness.get('alpha', 0)
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 4:
                if hasattr(witness[0], 'characteristic'):
                    p = int(witness[0].characteristic())
                    n = int(witness[1])
                    a = int(witness[2])
                    alpha = witness[3]
                else:
                    n = int(witness[0])
                    p = int(witness[1])
                    a = int(witness[2])
                    alpha = witness[3]
            else:
                return [False, False, False, False]
        else:
            return [False, False, False, False]

        if n < 1:
            return [False, False, False, False]

        # H1: F is a field containing a primitive n-th root of unity
        # We assume F = GF(p)
        try:
            if not sympy.isprime(p):
                h1 = False
            else:
                h1 = ((p - 1) % n == 0)
        except Exception:
            h1 = False

        # H2: characteristic of F does not divide n
        try:
            h2 = (n % p != 0)
        except Exception:
            h2 = False

        # H3: a is not a d-th power in F for any divisor d > 1 of n
        try:
            h3 = True
            a_mod = a % p
            for d in range(2, n + 1):
                if n % d == 0:
                    if a_mod == 0:
                        h3 = False
                        break
                    power = (p - 1) // math.gcd(d, p - 1)
                    if pow(a_mod, power, p) == 1:
                        h3 = False
                        break
        except Exception:
            h3 = False

        # Conclusion: x^n - a is irreducible over F and is exactly the minimal polynomial of alpha over F
        try:
            x = sympy.Symbol('x')
            poly = sympy.Poly(x**n - a_mod, x, domain=sympy.GF(p))
            is_irred = poly.is_irreducible

            if isinstance(alpha, int) or (hasattr(alpha, 'is_integer') and alpha.is_integer):
                val = (int(alpha)**n - a_mod) % p
                is_root = (val == 0)
            else:
                try:
                    val = alpha**n - a_mod
                    if hasattr(val, 'is_zero'):
                        is_root = bool(val.is_zero)
                    else:
                        is_root = (val == 0)
                except Exception:
                    is_root = False

            is_min_poly = is_irred and is_root
            q = is_irred and is_min_poly
            neg_q = not q
        except Exception:
            neg_q = False

        return [h1, h2, h3, neg_q]

    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field containing a primitive n-th root of unity",
    "H_2: characteristic of F does not divide n",
    "H_3: a is not a d-th power in F for any divisor d > 1 of n",
    "¬Q: x^n - a is not irreducible over F or is not exactly the minimal polynomial of alpha over F"
]

N_HYP = 3
NEG_Q_INDEX = 3