import sympy
import sympy.combinatorics
import sympy.matrices
from sympy.ntheory import factorint

# Top-level setup for potential witness expressions
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to provide the parameters (n, q, k).
    """
    try:
        if isinstance(witness, dict):
            n = witness['n']
            q = witness['q']
            k = witness['k']
        elif hasattr(witness, 'n') and hasattr(witness, 'q') and hasattr(witness, 'k'):
            n = witness.n
            q = witness.q
            k = witness.k
        elif isinstance(witness, (tuple, list)) and len(witness) == 2 and isinstance(witness[0], (tuple, list)):
            (n, q), k = witness
        else:
            n, q, k = witness
            
        n = int(n)
        q = int(q)
        k = int(k)
    except Exception:
        return [False, False, False]

    # H_1: V is an n-dimensional vector space over F_q
    # Interpreted as valid dimensions and base field/ring size
    try:
        h1 = (n >= 0) and (q >= 2)
    except Exception:
        h1 = False

    # H_2: k is an integer such that 0 <= k <= n
    try:
        h2 = (0 <= k <= n)
    except Exception:
        h2 = False

    # ¬Q: The number of distinct k-dimensional subspaces of V is NOT the given formula
    try:
        # Calculate the formula given in the conjecture
        if k == 0 or k == n:
            formula = 1
        else:
            num = 1
            den = 1
            for i in range(k):
                num *= (q**n - q**i)
                den *= (q**k - q**i)
            formula = num // den

        # Calculate the actual number of free submodules of rank k in (Z/qZ)^n
        factors = factorint(q)
        if len(factors) == 1:
            # If q is a prime power, F_q is a field and the formula is correct
            actual = formula
        else:
            # If q is not a prime power, F_q is the ring Z/qZ.
            # The number of free submodules of rank k is the product over its prime power components.
            actual = 1
            for p, e in factors.items():
                if k == 0 or k == n:
                    gb = 1
                else:
                    p_num = 1
                    p_den = 1
                    for i in range(k):
                        p_num *= (p**n - p**i)
                        p_den *= (p**k - p**i)
                    gb = p_num // p_den
                actual *= gb * (p ** ((e - 1) * k * (n - k)))

        neg_q = (actual != formula)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is an n-dimensional vector space over F_q",
    "H_2: k is an integer such that 0 <= k <= n",
    "¬Q: The number of distinct k-dimensional subspaces of V is not the given formula"
]

N_HYP = 2
NEG_Q_INDEX = 2