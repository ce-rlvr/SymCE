import sympy
from sympy import Set, Interval, FiniteSet, Union, Intersection, ProductSet, S
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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

def is_locally_connected(s):
    """
    Evaluates whether a SymPy Set represents a locally connected topological space
    (assuming the standard subspace topology from R or R^n).
    """
    if not isinstance(s, Set):
        return False
    if s.is_EmptySet:
        return True
    if isinstance(s, Interval):
        return True
    if isinstance(s, FiniteSet):
        return True
    if s in (S.Reals, S.Integers, S.Naturals, S.Naturals0):
        return True
    if s == S.Rationals:
        return False
    if isinstance(s, Union):
        return all(is_locally_connected(arg) for arg in s.args)
    if isinstance(s, ProductSet):
        return all(is_locally_connected(arg) for arg in s.sets)
    return True

def is_topology(X, tau):
    try:
        if not isinstance(X, (set, frozenset, list, tuple)):
            return False
        if not isinstance(tau, (set, frozenset, list, tuple)):
            return False
        X_set = frozenset(X)
        tau_sets = [frozenset(U) for U in tau]
        if frozenset() not in tau_sets or X_set not in tau_sets:
            return False
        for U in tau_sets:
            for V in tau_sets:
                if U.intersection(V) not in tau_sets:
                    return False
                if U.union(V) not in tau_sets:
                    return False
        return True
    except Exception:
        return False

def is_connected_space(X_set, tau_sets):
    if not X_set:
        return True
    for U in tau_sets:
        if U == frozenset() or U == X_set:
            continue
        comp = X_set - U
        if comp in tau_sets:
            return False
    return True

def is_locally_connected_space(X, tau):
    X_set = frozenset(X)
    tau_sets = [frozenset(U) for U in tau]
    
    connected_open_sets = []
    for U in tau_sets:
        sub_tau = {V.intersection(U) for V in tau_sets}
        if is_connected_space(U, sub_tau):
            connected_open_sets.append(U)
            
    for U in tau_sets:
        union_C = frozenset()
        for C in connected_open_sets:
            if C.issubset(U):
                union_C = union_C.union(C)
        if union_C != U:
            return False
    return True

def product_topology(spaces):
    X_prod = list(itertools.product(*[X for X, tau in spaces]))
    if len(X_prod) > 50:
        raise ValueError("Product space too large")
        
    basis = []
    for U_tuple in itertools.product(*[tau for X, tau in spaces]):
        basis_elem = frozenset(itertools.product(*U_tuple))
        basis.append(basis_elem)
        
    tau_prod = set(basis)
    added = True
    while added:
        added = False
        new_sets = set()
        for A in tau_prod:
            for B in basis:
                C = A.union(B)
                if C not in tau_prod:
                    new_sets.add(C)
        if new_sets:
            tau_prod.update(new_sets)
            added = True
            if len(tau_prod) > 8192:
                raise ValueError("Topology too large")
            
    return X_prod, tau_prod

def conditions(witness) -> list[bool]:
    # H_1: X_1, ..., X_n are topological spaces
    try:
        h1 = False
        is_finite_spaces = False
        is_sympy_sets = False
        
        if isinstance(witness, (list, tuple)) and len(witness) > 0:
            if all(isinstance(s, Set) for s in witness):
                h1 = True
                is_sympy_sets = True
            elif all(isinstance(s, (list, tuple)) and len(s) == 2 for s in witness):
                if all(is_topology(X, tau) for X, tau in witness):
                    h1 = True
                    is_finite_spaces = True
    except Exception:
        h1 = False
        is_finite_spaces = False
        is_sympy_sets = False

    # H_2: Each X_i is locally connected
    try:
        h2 = False
        if h1:
            if is_sympy_sets:
                h2 = all(is_locally_connected(s) for s in witness)
            elif is_finite_spaces:
                h2 = all(is_locally_connected_space(X, tau) for X, tau in witness)
    except Exception:
        h2 = False

    # neg_Q: The product space X is NOT locally connected
    try:
        neg_q = False
        if h1:
            if is_sympy_sets:
                prod = ProductSet(*witness)
                neg_q = not is_locally_connected(prod)
            elif is_finite_spaces:
                X_prod, tau_prod = product_topology(witness)
                neg_q = not is_locally_connected_space(X_prod, tau_prod)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: X_1, ..., X_n are topological spaces",
    "H_2: Each X_i is locally connected",
    "¬Q: The product space X is not locally connected"
]

N_HYP = 2
NEG_Q_INDEX = 2