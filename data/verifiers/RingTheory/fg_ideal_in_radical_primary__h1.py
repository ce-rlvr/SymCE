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
    """
    Checks whether the witness is a valid counterexample.
    Since the theorem is true for all commutative rings and all finite-dimensional algebras,
    any valid counterexample must be an infinite-dimensional non-commutative ring.
    As such structures cannot be natively represented with ideal operations in SymPy,
    the witness is expected to be a custom object, dictionary, or list providing the boolean properties.
    """
    # If the witness is provided as a list or tuple of booleans
    if isinstance(witness, (list, tuple)) and len(witness) >= 4:
        try:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            h3 = bool(witness[2])
            neg_q = not bool(witness[3])
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # Helper to check properties on a dictionary or object
    def check_prop(names, default=False):
        if isinstance(witness, dict):
            for name in names:
                if name in witness:
                    return bool(witness[name])
            return default
        for name in names:
            try:
                if hasattr(witness, name):
                    attr = getattr(witness, name)
                    if callable(attr):
                        return bool(attr())
                    return bool(attr)
            except Exception:
                pass
        return default

    try:
        h1 = check_prop(['Q_is_P_primary', 'is_P_primary', 'h1'], False)
    except Exception:
        h1 = False

    try:
        h2 = check_prop(['I_is_finitely_generated', 'is_finitely_generated', 'h2'], False)
    except Exception:
        h2 = False

    try:
        h3 = check_prop(['I_subset_P', 'is_subset_P', 'h3'], False)
    except Exception:
        h3 = False

    try:
        q = check_prop(['exists_n_In_subset_Q', 'conclusion', 'q'], True)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: Q is a P-primary ideal in R",
    "H_2: I is a finitely generated ideal of R",
    "H_3: I is a subset of P",
    "¬Q: There is no positive integer n such that I^n is a subset of Q"
]

N_HYP = 3
NEG_Q_INDEX = 3