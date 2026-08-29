import sympy
from sympy import Interval, FiniteSet, EmptySet, Union, Intersection
from sympy.sets.fancysets import Reals
from sympy.sets.sets import Set
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def is_connected(S):
    """Check if a SymPy set S in Reals is connected."""
    if S.is_empty == True:
        return True
    if isinstance(S, Interval):
        return True
    if isinstance(S, FiniteSet) and len(S) <= 1:
        return True
    if S == Reals:
        return True
    try:
        S_simp = S.simplify()
        if isinstance(S_simp, Interval):
            return True
        if isinstance(S_simp, FiniteSet) and len(S_simp) <= 1:
            return True
        if S_simp.is_empty == True:
            return True
    except Exception:
        pass
    return False

def to_set(obj):
    """Convert lists/tuples to SymPy FiniteSet, leave Sets as is."""
    if isinstance(obj, Set):
        return obj
    if isinstance(obj, (list, tuple, set)):
        return FiniteSet(*obj)
    return obj

def conditions(witness):
    """
    Check the hypotheses and negated conclusion for the conjecture.
    Witness can be a tuple (A, B, E) or (X, A, B, E), or a dictionary.
    """
    try:
        if isinstance(witness, dict):
            A = to_set(witness.get('A'))
            B = to_set(witness.get('B'))
            E = to_set(witness.get('E'))
            X = to_set(witness.get('X', Reals))
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 3:
                A, B, E = map(to_set, witness)
                X = Reals
            elif len(witness) == 4:
                X, A, B, E = map(to_set, witness)
            else:
                return [False] * 4
        else:
            return [False] * 4
    except Exception:
        return [False] * 4

    # H_1: A and B are separated sets in X
    try:
        if A is None or B is None or X is None:
            h1 = False
        elif not (A.is_subset(X) == True and B.is_subset(X) == True):
            h1 = False
        else:
            # In a subspace X of Reals, A and B are separated iff they are separated in Reals
            # because A \cap cl_X(B) = A \cap (cl(B) \cap X) = A \cap cl(B)
            cond1 = A.intersect(B.closure).is_empty
            cond2 = B.intersect(A.closure).is_empty
            h1 = (cond1 is True) and (cond2 is True)
    except Exception:
        h1 = False

    # H_2: E is a connected subset of X
    try:
        if E is None or X is None:
            h2 = False
        elif not (E.is_subset(X) == True):
            h2 = False
        else:
            h2 = is_connected(E)
    except Exception:
        h2 = False

    # H_3: E is a subset of the union A U B
    try:
        if E is None or A is None or B is None:
            h3 = False
        else:
            h3 = (E.is_subset(A.union(B)) is True)
    except Exception:
        h3 = False

    # ¬Q: E is NOT a subset of A and E is NOT a subset of B
    try:
        if E is None or A is None or B is None:
            neg_q = False
        else:
            sub_A = E.is_subset(A)
            sub_B = E.is_subset(B)
            if sub_A is None or sub_B is None:
                neg_q = False
            else:
                neg_q = not (sub_A or sub_B)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A and B are separated sets in X",
    "H_2: E is a connected subset of X",
    "H_3: E is a subset of the union A U B",
    "¬Q: E is not a subset of A and E is not a subset of B"
]

N_HYP = 3
NEG_Q_INDEX = 3