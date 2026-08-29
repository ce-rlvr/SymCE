import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_topological_space(X, T):
    try:
        if not isinstance(X, (list, tuple, set, frozenset)):
            return False
        if not isinstance(T, (list, tuple, set, frozenset)):
            return False
            
        X_set = frozenset(X)
        T_sets = set()
        for u in T:
            if not isinstance(u, (list, tuple, set, frozenset)):
                return False
            T_sets.add(frozenset(u))
            
        # Check if all elements of T are subsets of X
        for u in T_sets:
            if not u.issubset(X_set):
                return False
                
        # Empty set and X must be in T
        if frozenset() not in T_sets or X_set not in T_sets:
            return False
            
        # Closed under finite union and intersection
        for u in T_sets:
            for v in T_sets:
                if u.union(v) not in T_sets:
                    return False
                if u.intersection(v) not in T_sets:
                    return False
                    
        return True
    except Exception:
        return False

def is_connected(X, T):
    try:
        X_set = frozenset(X)
        T_sets = set(frozenset(u) for u in T)
        for U in T_sets:
            if U != frozenset() and U != X_set:
                # If there is a proper non-empty open set whose complement is also open,
                # then the space is disconnected.
                if (X_set - U) in T_sets:
                    return False
        return True
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    # H_1: {X_i}_{i \in I} is a non-empty family of topological spaces
    try:
        h1 = False
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            h1 = True
            for space in witness:
                if not isinstance(space, (list, tuple)) or len(space) != 2:
                    h1 = False
                    break
                X, T = space
                if not is_topological_space(X, T):
                    h1 = False
                    break
    except Exception:
        h1 = False

    # H_2: X_i is non-empty for all i \in I
    try:
        h2 = False
        if h1:
            h2 = True
            for space in witness:
                X, T = space
                if len(X) == 0:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The product space \prod_{i \in I} X_i is not connected in the product topology
    try:
        neg_q = False
        if h1 and h2:
            # A product of non-empty topological spaces is connected if and only if 
            # every factor space is connected.
            product_connected = True
            for space in witness:
                X, T = space
                if not is_connected(X, T):
                    product_connected = False
                    break
            neg_q = not product_connected
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: {X_i}_{i \\in I} is a non-empty family of topological spaces",
    "H_2: X_i is non-empty for all i \\in I",
    "¬Q: The product space \\prod_{i \\in I} X_i is not connected in the product topology"
]

N_HYP = 2
NEG_Q_INDEX = 2