import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    # H1: R is a principal ideal domain
    try:
        h1 = False
        if isinstance(witness, dict):
            h1 = witness.get('is_PID', witness.get('R_is_PID', False))
        else:
            if hasattr(witness, 'R_is_PID'):
                h1 = witness.R_is_PID() if callable(witness.R_is_PID) else witness.R_is_PID
            elif hasattr(witness, 'is_PID'):
                h1 = witness.is_PID() if callable(witness.is_PID) else witness.is_PID
            elif hasattr(witness, 'R') and hasattr(witness.R, 'is_PID'):
                h1 = witness.R.is_PID() if callable(witness.R.is_PID) else witness.R.is_PID
    except Exception:
        h1 = False

    # H2: 0 -> M' -> M -> M'' -> 0 is a short exact sequence of R-modules
    try:
        h2 = False
        if isinstance(witness, dict):
            h2 = witness.get('is_exact', witness.get('is_short_exact_sequence', False))
        else:
            if hasattr(witness, 'is_exact'):
                h2 = witness.is_exact() if callable(witness.is_exact) else witness.is_exact
            elif hasattr(witness, 'is_short_exact_sequence'):
                h2 = witness.is_short_exact_sequence() if callable(witness.is_short_exact_sequence) else witness.is_short_exact_sequence
    except Exception:
        h2 = False

    # ¬Q: The rank of M does not equal the rank of M' plus the rank of M''
    try:
        neg_q = False
        if isinstance(witness, dict) and 'rank_M' in witness:
            rank_M = witness['rank_M']
            rank_M_prime = witness['rank_M_prime']
            rank_M_double_prime = witness['rank_M_double_prime']
        else:
            def get_rank(m):
                if hasattr(m, 'rank'):
                    return m.rank() if callable(m.rank) else m.rank
                elif hasattr(m, 'dimension'):
                    return m.dimension() if callable(m.dimension) else m.dimension
                elif isinstance(m, (list, tuple)):
                    return len([x for x in m if x == 0 or abs(x) > 1])
                else:
                    return len(m)
            
            rank_M = get_rank(witness.M)
            rank_M_prime = get_rank(witness.M_prime)
            rank_M_double_prime = get_rank(witness.M_double_prime)
            
        q = (rank_M == rank_M_prime + rank_M_double_prime)
        neg_q = not q
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: 0 -> M' -> M -> M'' -> 0 is a short exact sequence of R-modules",
    "¬Q: The rank of M does not equal the rank of M' plus the rank of M''"
]

N_HYP = 2
NEG_Q_INDEX = 2