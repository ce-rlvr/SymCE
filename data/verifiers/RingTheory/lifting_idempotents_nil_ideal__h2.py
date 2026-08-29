import sympy
from sympy import S, ZZ
import math

# Top-level setup for potential witness expressions
Z = ZZ

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: x^2 - x is in N",
    "¬Q: There is no idempotent e in R such that e - x is in N"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_collection(obj):
    if isinstance(obj, str):
        return False
    return isinstance(obj, (list, tuple, set, frozenset, sympy.Set)) or hasattr(obj, 'contains')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness is expected to represent a commutative ring R, an ideal N, and an element x.
    Since the simplest counterexamples exist in Z, we parse the witness as representing Z or Z/mZ.
    Supported witness formats:
      - (n, x) : R = Z, N = nZ, element = x
      - (m, n, x) : R = Z/mZ, N = nZ/mZ, element = x
      - dict with keys 'm'/'R', 'n'/'N', 'x'
    """
    try:
        # Parse witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                a, b = witness
                if is_collection(a):
                    n, x = a, b
                elif is_collection(b):
                    n, x = b, a
                else:
                    n, x = a, b
                m = 0
            elif len(witness) == 3:
                m, n, x = witness
            else:
                return [False, False, False]
        elif isinstance(witness, dict):
            m = witness.get('m', witness.get('R', 0))
            n = witness.get('n', witness.get('N', 0))
            x = witness.get('x', 0)
        else:
            return [False, False, False]

        # Parse m (modulus of the ring, 0 means Z)
        if str(m) in ['Integers', 'ZZ', 'Z', 'S.Integers'] or m == S.Integers or m == ZZ:
            m = 0
        else:
            try:
                m = abs(int(m))
            except Exception:
                m = 0

        # Parse x (the element)
        x = int(x)

        # Parse n (generator of the ideal N)
        if isinstance(n, sympy.Set) or hasattr(n, 'contains'):
            if hasattr(n, 'is_FiniteSet') and n.is_FiniteSet:
                gen = 0
                for elem in n:
                    try:
                        gen = math.gcd(gen, int(elem))
                    except Exception:
                        pass
                n = gen
            else:
                gen = 0
                limit = abs(x**2 - x)
                if limit == 0:
                    limit = 100
                for i in range(1, limit + 2):
                    try:
                        if n.contains(i) == True:
                            gen = i
                            break
                    except Exception:
                        pass
                n = gen
        elif isinstance(n, (list, tuple, set, frozenset)):
            gen = 0
            for elem in n:
                try:
                    gen = math.gcd(gen, int(elem))
                except Exception:
                    pass
            n = gen
        else:
            try:
                n = int(n)
            except Exception:
                n = 0
        n = abs(n)

    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring
    # We only support Z and Z/mZ, which are always commutative rings.
    h1 = True

    # H_2: x^2 - x is in N
    try:
        val = x**2 - x
        if m == 0:
            if n == 0:
                h2 = (val == 0)
            else:
                h2 = (val % n == 0)
        else:
            gen = math.gcd(n, m)
            h2 = (val % gen == 0)
    except Exception:
        h2 = False

    # neg_Q: There is no idempotent e in R such that e - x is in N
    try:
        has_idempotent = False
        if m == 0:
            # In Z, the only idempotents are 0 and 1
            idempotents = [0, 1]
            for e in idempotents:
                diff = e - x
                if n == 0:
                    if diff == 0:
                        has_idempotent = True
                        break
                else:
                    if diff % n == 0:
                        has_idempotent = True
                        break
        else:
            # In Z/mZ, we check all elements for idempotency
            gen = math.gcd(n, m)
            for e in range(m):
                if (e**2 - e) % m == 0:
                    diff = e - x
                    if diff % gen == 0:
                        has_idempotent = True
                        break
        neg_q = not has_idempotent
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]