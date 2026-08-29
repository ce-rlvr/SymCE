import sympy
import sympy.combinatorics as combinatorics
import sympy.combinatorics.named_groups as named_groups
import sympy.matrices as matrices
import math
import itertools
import functools

# Top-level setup for potential witness references
S3 = named_groups.SymmetricGroup(3)
S4 = named_groups.SymmetricGroup(4)
A4 = named_groups.AlternatingGroup(4)
D4 = named_groups.DihedralGroup(4)
C4 = named_groups.CyclicGroup(4)
V4 = named_groups.AlternatingGroup(4)
Z2 = named_groups.CyclicGroup(2)
Z3 = named_groups.CyclicGroup(3)
Z4 = named_groups.CyclicGroup(4)
Z6 = named_groups.CyclicGroup(6)
trivial = named_groups.CyclicGroup(1)
I2 = matrices.eye(2)
I3 = matrices.eye(3)
O2 = matrices.zeros(2, 2)
O3 = matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            x = witness.get('x', witness.get('x_n'))
            k = witness.get('k')
            y = witness.get('y', witness.get('y_n'))
        else:
            x, k, y = witness
            
        # Safely consume iterables that are not lists/tuples or callables
        if hasattr(x, '__iter__') and not isinstance(x, (list, tuple)) and not callable(x):
            x = list(itertools.islice(x, 200))
        if hasattr(y, '__iter__') and not isinstance(y, (list, tuple)) and not callable(y):
            y = list(itertools.islice(y, 200))
    except Exception:
        return [False, False, False]

    # H1: (x_n) is a sequence of real numbers
    try:
        if isinstance(x, (list, tuple)):
            h1_ok = len(x) > 0 and all(isinstance(i, (int, float, sympy.Basic)) for i in x)
        elif callable(x):
            val = x(1)
            h1_ok = isinstance(val, (int, float, sympy.Basic))
        else:
            h1_ok = False
    except Exception:
        h1_ok = False

    # H2: k is a fixed positive integer
    try:
        h2_ok = int(k) == k and k > 0
    except Exception:
        h2_ok = False

    # neg_Q: The set of subsequential limits of (x_n) is NOT equal to the set of subsequential limits of (y_n)
    try:
        def get_lims(seq):
            if isinstance(seq, (list, tuple)):
                if len(seq) > 50:
                    # For long sequences, approximate limits by looking at the tail
                    return set(round(float(v), 2) for v in seq[-50:])
                else:
                    # For short lists (likely representing periodic sequences), use exact values
                    return set(round(float(v), 5) for v in seq)
            elif callable(seq):
                # Evaluate terms far out in the sequence
                return set(round(float(seq(n)), 2) for n in range(100, 150))
            else:
                return set()
        
        lims_x = get_lims(x)
        lims_y = get_lims(y)
        
        neg_q_ok = (lims_x != lims_y)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: (x_n) is a sequence of real numbers",
    "H_2: k is a fixed positive integer",
    "¬Q: The set of subsequential limits of (x_n) is NOT equal to the set of subsequential limits of (y_n)"
]

N_HYP = 2
NEG_Q_INDEX = 2