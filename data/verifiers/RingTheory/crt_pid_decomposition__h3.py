import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
from sympy.ntheory import factorint
import math

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
I2 = sympy.matrices.eye(2)

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (a, factors) or a dict with 'a' and 'factors',
    where 'a' is an integer and 'factors' is a list of integers (m_i) or tuples (p_i, e_i).
    """
    # Parse witness
    try:
        if isinstance(witness, dict):
            a = witness.get('a')
            factors = witness.get('factors', witness.get('p_e_list', []))
        else:
            a, factors = witness
    except Exception:
        return [False, False, False]

    def is_int(x):
        try:
            return int(x) == x
        except Exception:
            return False

    # H_1: R is a Principal Ideal Domain (PID)
    # We interpret this as R = Z, so 'a' and all 'factors' must be integers.
    try:
        h1 = is_int(a) and isinstance(factors, (list, tuple))
        if h1:
            for f in factors:
                if isinstance(f, (list, tuple)):
                    if not (len(f) == 2 and is_int(f[0]) and is_int(f[1])):
                        h1 = False
                        break
                else:
                    if not is_int(f):
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H_2: a is a non-zero, non-unit element of R
    try:
        h2 = (a != 0) and (abs(a) > 1)
    except Exception:
        h2 = False

    # ¬Q: The quotient ring R/(a) is NOT isomorphic to the direct product \prod_{i=1}^k R/(p_i^{e_i})
    try:
        def get_invariants(n):
            if n == 0:
                return 1, []
            n = abs(int(n))
            if n == 1:
                return 0, []
            # The elementary divisors (prime power components) uniquely determine the isomorphism class
            return 0, sorted([p**k for p, k in factorint(n).items()])

        rank_a, inv_a = get_invariants(a)
        
        rank_f = 0
        inv_f = []
        for f in factors:
            if isinstance(f, (list, tuple)):
                val = f[0]**f[1]
            else:
                val = f
            r, inv = get_invariants(val)
            rank_f += r
            inv_f.extend(inv)
        inv_f.sort()

        isomorphic = (rank_a == rank_f) and (inv_a == inv_f)
        neg_q = not isomorphic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a Principal Ideal Domain (PID)",
    "H_2: a is a non-zero, non-unit element of R",
    "¬Q: The quotient ring R/(a) is NOT isomorphic to the direct product \\prod_{i=1}^k R/(p_i^{e_i})"
]

N_HYP = 2
NEG_Q_INDEX = 2