import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint
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

def gaussian_binomial(n, k, q):
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    num = 1
    den = 1
    for i in range(k):
        num *= (q**n - q**i)
        den *= (q**k - q**i)
    return num // den

def conditions(witness):
    try:
        if isinstance(witness, dict):
            q = witness.get('q')
            n = witness.get('n')
            k = witness.get('k')
            V = witness.get('V')
            if V is None:
                V = witness.get('V_dim')
        else:
            q, n, k, V = witness
            
        if isinstance(V, (int, sympy.Integer)):
            V_dim = int(V)
        elif isinstance(V, str):
            if '^' in V:
                V_dim = int(V.split('^')[1])
            else:
                V_dim = int(V)
        else:
            try:
                V_dim = int(V)
            except Exception:
                V_dim = len(V)
    except Exception:
        return [False, False, False]

    # H1: F_q is a finite field with q elements
    try:
        q_val = float(q)
        if q_val != int(q_val):
            h1 = False
        else:
            q_int = int(q_val)
            h1 = (q_int >= 2) and (len(factorint(q_int)) == 1)
    except Exception:
        h1 = False

    # H2: k is an integer such that 0 <= k <= n
    try:
        k_val = float(k)
        n_val = float(n)
        if k_val != int(k_val) or n_val != int(n_val):
            h2 = False
        else:
            k_int = int(k_val)
            n_int = int(n_val)
            h2 = (0 <= k_int <= n_int)
    except Exception:
        h2 = False

    # neg_Q: The number of distinct k-dimensional subspaces of V is NOT \prod_{i=0}^{k-1} \frac{q^n - q^i}{q^k - q^i}
    try:
        actual_subspaces = gaussian_binomial(V_dim, int(float(k)), int(float(q)))
        formula_subspaces = gaussian_binomial(int(float(n)), int(float(k)), int(float(q)))
        neg_q = actual_subspaces != formula_subspaces
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F_q is a finite field with q elements",
    "H_2: k is an integer such that 0 <= k <= n",
    "¬Q: The number of distinct k-dimensional subspaces of V is not equal to the formula"
]

N_HYP = 2
NEG_Q_INDEX = 2