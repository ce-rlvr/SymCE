import math
from sympy.combinatorics.permutations import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            sigma = witness.get('sigma')
            k = witness.get('k')
            n = witness.get('n')
            if n is None and hasattr(sigma, 'cyclic_form'):
                c_form = sigma.cyclic_form
                n = len(c_form[0]) if len(c_form) == 1 else (1 if len(c_form) == 0 else None)
        else:
            if len(witness) == 3:
                sigma, n, k = witness
            elif len(witness) == 2:
                sigma, k = witness
                if hasattr(sigma, 'cyclic_form'):
                    c_form = sigma.cyclic_form
                    n = len(c_form[0]) if len(c_form) == 1 else (1 if len(c_form) == 0 else None)
                else:
                    n = None
            else:
                return [False, False]
    except Exception:
        return [False, False]

    # H1: sigma is an n-cycle
    h1 = False
    try:
        if isinstance(sigma, Permutation):
            if hasattr(n, '__index__'):
                n_val = int(n)
                if n_val >= 1:
                    c_form = sigma.cyclic_form
                    if n_val == 1:
                        h1 = (len(c_form) == 0)
                    else:
                        h1 = (len(c_form) == 1 and len(c_form[0]) == n_val)
    except Exception:
        h1 = False

    # Conclusion: sigma^k is a product of gcd(n, k) disjoint cycles of length n / gcd(n, k)
    q = False
    try:
        g = math.gcd(n, k)
        l = n // g
        if n % g == 0:
            pw = sigma ** int(k)
            if l > 1:
                c_form = pw.cyclic_form
                if len(c_form) == g and all(len(c) == l for c in c_form):
                    q = True
            else:
                if pw.is_Identity:
                    q = True
    except Exception:
        q = False

    return [h1, not q]

CONDITION_LABELS = [
    "H_1: sigma is an n-cycle in a symmetric group",
    "¬Q: sigma^k is not a product of gcd(n, k) disjoint cycles of length n / gcd(n, k)"
]

N_HYP = 1
NEG_Q_INDEX = 1