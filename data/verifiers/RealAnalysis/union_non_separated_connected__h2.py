import sympy
from sympy import Interval, FiniteSet, Union, Intersection, EmptySet, S, Set

def closure(s):
    """
    Computes the closure of a set in the standard topology of the real line.
    Supports EmptySet, FiniteSet, Interval, and finite Unions of these.
    """
    if s == EmptySet or getattr(s, 'is_empty', False) is True:
        return EmptySet
    elif isinstance(s, FiniteSet):
        return s
    elif isinstance(s, Interval):
        return Interval(s.inf, s.sup, False, False)
    elif isinstance(s, Union):
        return Union(*[closure(arg) for arg in s.args])
    elif s == S.Reals:
        return S.Reals
    else:
        return s

def is_connected(s):
    """
    Checks if a set is connected in the standard topology of the real line.
    In R, connected sets are exactly the intervals (including rays and the whole line),
    singletons, and the empty set.
    """
    if s == EmptySet or getattr(s, 'is_empty', False) is True:
        return True
    if isinstance(s, FiniteSet):
        return len(s) <= 1
    if isinstance(s, Interval):
        return True
    if s == S.Reals:
        return True
    return False

def is_nonempty(s):
    """
    Safely checks if a sympy Set is non-empty.
    """
    if s == EmptySet:
        return False
    if getattr(s, 'is_empty', None) is True:
        return False
    if getattr(s, 'is_empty', None) is False:
        return True
    if isinstance(s, (FiniteSet, Interval, Union)):
        return True
    return False

def conditions(witness):
    """
    Given a witness (A, B) where A and B are sympy Sets representing subsets of R,
    checks if they satisfy the remaining hypotheses and falsify the conclusion.
    """
    try:
        A, B = witness
    except Exception:
        return [False, False, False]
    
    # H_1: X is a topological space (implicitly R with standard topology)
    # We verify that A and B are valid sympy Sets.
    try:
        h1 = isinstance(A, Set) and isinstance(B, Set)
    except Exception:
        h1 = False
        
    # H_2: A and B are not separated
    # Meaning A \cap \overline{B} \neq \emptyset or \overline{A} \cap B \neq \emptyset
    try:
        A_clos = closure(A)
        B_clos = closure(B)
        int1 = A.intersect(B_clos)
        int2 = A_clos.intersect(B)
        not_sep = is_nonempty(int1) or is_nonempty(int2)
    except Exception:
        not_sep = False
        
    # ¬Q: The union A \cup B is NOT a connected subset of X
    try:
        A_union_B = Union(A, B)
        neg_q = not is_connected(A_union_B)
    except Exception:
        neg_q = False
        
    return [h1, not_sep, neg_q]

CONDITION_LABELS = [
    "H_1: X is a topological space",
    "H_2: A and B are not separated",
    "¬Q: A U B is not connected"
]

N_HYP = 2
NEG_Q_INDEX = 2