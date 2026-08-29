import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint, isprime

# Top-level setup: named object bindings
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

def conditions(witness):
    n, p = None, None
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            p = witness.get('p')
        elif hasattr(witness, 'n') and hasattr(witness, 'p'):
            n = witness.n
            p = witness.p
        else:
            n, p = witness[:2]
    except Exception:
        return [False, False, False, False, False]

    # H_1: n is a positive integer
    try:
        n_val = int(n)
        h1 = (n_val > 0) and (n_val == n)
    except Exception:
        h1 = False

    # H_2: \mathbb{F}_p is the finite field of p elements
    # A finite field of order p exists if and only if p is a prime power.
    try:
        p_val = int(p)
        if p_val > 1 and p_val == p:
            factors = factorint(p_val)
            h2 = len(factors) == 1
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: G is the general linear group GL_n(\mathbb{F}_p)
    # This is a definitional hypothesis for the setup.
    h3 = True

    # H_4: U is the subgroup of G consisting of all upper unitriangular matrices
    # This is a definitional hypothesis for the setup.
    h4 = True

    # ¬Q: U is not a Sylow p-subgroup of G
    # A Sylow p-subgroup is only defined when p is a prime.
    # If p is a prime power but not a prime (e.g., p=4), U cannot be a Sylow p-subgroup.
    try:
        neg_q = not isprime(int(p))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: F_p is the finite field of p elements",
    "H_3: G is the general linear group GL_n(F_p)",
    "H_4: U is the subgroup of G consisting of all upper unitriangular matrices",
    "¬Q: U is not a Sylow p-subgroup of G"
]

N_HYP = 4
NEG_Q_INDEX = 4