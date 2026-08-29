import sympy
from sympy.combinatorics import Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
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

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            a = witness.get('a')
            b = witness.get('b')
            c = witness.get('c')
            tau_1 = witness.get('tau_1')
            tau_2 = witness.get('tau_2')
        else:
            witness = tuple(witness)
            if len(witness) == 6:
                n, a, b, c, tau_1, tau_2 = witness
            elif len(witness) == 4:
                n, a, b, c = witness
                tau_1 = None
                tau_2 = None
            else:
                return [False, False, False, False]
                
        # If tau_1 and tau_2 are not provided, construct them to satisfy the hypothesis
        if tau_1 is None and tau_2 is None:
            if isinstance(a, int) and isinstance(b, int) and isinstance(c, int):
                tau_1 = Permutation(a - 1, b - 1)
                tau_2 = Permutation(b - 1, c - 1)
    except Exception:
        return [False, False, False, False]

    # H_1: Let n >= 3 be an integer
    try:
        h1 = isinstance(n, int) and not isinstance(n, bool) and n >= 3
    except Exception:
        h1 = False

    # H_2: Let a, b, c be three distinct elements from the set 1 to n
    try:
        h2 = (isinstance(a, int) and isinstance(b, int) and isinstance(c, int) and
              not isinstance(a, bool) and not isinstance(b, bool) and not isinstance(c, bool) and
              len({a, b, c}) == 3 and
              all(1 <= x <= n for x in (a, b, c)))
    except Exception:
        h2 = False

    # H_3: Let tau_1 = (a b) and tau_2 = (b c) be transpositions in S_n
    try:
        def check_tau(tau, x, y, n_val):
            if not isinstance(tau, Permutation):
                return False
            
            try:
                moved = set(tau.support())
            except Exception:
                moved = {i for i in range(tau.size) if tau(i) != i}
                
            # Check 1-indexed interpretation
            try:
                if moved.issubset({x, y}) and tau(x) == y and tau(y) == x:
                    return True
            except Exception:
                pass
                
            # Check 0-indexed interpretation
            try:
                if moved.issubset({x - 1, y - 1}) and tau(x - 1) == y - 1 and tau(y - 1) == x - 1:
                    return True
            except Exception:
                pass
                    
            return False

        if h1 and h2:
            ok1 = check_tau(tau_1, a, b, n)
            ok2 = check_tau(tau_2, b, c, n)
            h3 = ok1 and ok2
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: The commutator of tau_1 and tau_2 is NOT a 3-cycle
    try:
        if isinstance(tau_1, Permutation) and isinstance(tau_2, Permutation):
            # Commutator [tau_1, tau_2] = tau_1^-1 * tau_2^-1 * tau_1 * tau_2
            comm = tau_1**-1 * tau_2**-1 * tau_1 * tau_2
            
            # A 3-cycle has exactly one cycle of length 3, and all other cycles of length 1.
            # SymPy's cyclic_form omits cycles of length 1 (fixed points).
            cycles = comm.cyclic_form
            is_3_cycle = (len(cycles) == 1 and len(cycles[0]) == 3)
            
            neg_q = not is_3_cycle
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 3 is an integer",
    "H_2: a, b, c are three distinct elements from 1 to n",
    "H_3: tau_1 = (a b) and tau_2 = (b c) are transpositions in S_n",
    "¬Q: The commutator of tau_1 and tau_2 is not a 3-cycle"
]

N_HYP = 3
NEG_Q_INDEX = 3