import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    Checks if the witness is a valid counterexample.
    The witness should represent R = Z/nZ, M = Z/mZ, K = Z/kZ.
    It can be a tuple of three integers (n, m, k) or a dict with keys 'n', 'm', 'k'.
    """
    try:
        if isinstance(witness, dict):
            n = abs(int(witness['n']))
            m = abs(int(witness['m']))
            k = abs(int(witness['k']))
        else:
            n = abs(int(witness[0]))
            m = abs(int(witness[1]))
            k = abs(int(witness[2]))
    except Exception:
        return [False, False, False]

    # H_1: R is an integral domain
    try:
        if n == 0:
            h1 = True
        elif n == 1:
            h1 = False
        else:
            h1 = sympy.isprime(n)
    except Exception:
        h1 = False

    # H_2: M is a torsion-free R-module
    try:
        def is_r_module(n, m):
            if m == 0:
                return n == 0
            return n % m == 0

        def is_torsion_free(n, m):
            if not is_r_module(n, m):
                return False
            if n == 0 and m == 0:
                return True
            if n == 0 and m > 0:
                return m == 1
            for r in range(1, n):
                for x in range(1, m):
                    if (r * x) % m == 0:
                        return False
            return True

        h2 = is_torsion_free(n, m)
    except Exception:
        h2 = False

    # ¬Q: The canonical map M -> M \otimes_R K is not injective
    try:
        def is_r_algebra(n, k):
            if k == 0:
                return n == 0
            return n % k == 0

        def is_injective(m, k):
            if m == 0:
                return k == 0
            return k % m == 0

        if not is_r_algebra(n, k):
            neg_q = False
        else:
            neg_q = not is_injective(m, k)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is a torsion-free R-module",
    "¬Q: The canonical map M -> M \\otimes_R K is not injective"
]

N_HYP = 2
NEG_Q_INDEX = 2