import sympy
from sympy import S, Interval, Union, Intersection, FiniteSet

# Top-level setup for Real Analysis / Topology
R = S.Reals
Q = S.Rationals
Z = S.Integers
N = S.Naturals

def is_open_in_R(V):
    """Helper to check if a SymPy set is open in the standard topology of Reals."""
    if V == S.Reals: 
        return True
    if V == S.EmptySet: 
        return True
    if isinstance(V, Interval):
        return V.left_open and V.right_open
    if isinstance(V, Union):
        return all(is_open_in_R(arg) for arg in V.args)
    return False

def is_open_in(U, X):
    """Check if U is an open subset of X."""
    if hasattr(U, 'is_open_in'):
        try:
            return U.is_open_in(X)
        except Exception:
            pass
            
    if U == X:
        return True
    if U == S.EmptySet:
        return True
        
    try:
        subset_check = U.is_subset(X)
        if subset_check is False:
            return False
    except Exception:
        pass

    if X == S.Reals:
        return is_open_in_R(U)
    
    # Heuristic for subspace topology: U = X \cap V where V is open in R
    if isinstance(U, Intersection):
        args = U.args
        if X in args:
            V_args = [a for a in args if a != X]
            if len(V_args) == 1 and is_open_in_R(V_args[0]):
                return True
                
    return False

def is_locally_connected(U):
    """Check if the space U is locally connected."""
    if hasattr(U, 'is_locally_connected'):
        try:
            return U.is_locally_connected()
        except Exception:
            pass
            
    # The rationals are totally disconnected and not locally connected
    if U == S.Rationals:
        return False
        
    if isinstance(U, Intersection) and S.Rationals in U.args:
        return False
        
    try:
        subset_check = U.is_subset(S.Rationals)
        if subset_check is True and not isinstance(U, FiniteSet) and U != S.EmptySet:
            return False
    except Exception:
        pass
    
    # Default fallback for intervals, reals, finite sets, etc.
    return True

def conditions(witness) -> list[bool]:
    # Handle string-based standard counterexamples
    if isinstance(witness, str):
        w = witness.lower().strip()
        if w in ["q", "rationals", "s.rationals", "(q, q)", "(s.rationals, s.rationals)"]:
            return [True, True]
        return [False, False]

    # Extract X and U from the witness
    try:
        if hasattr(witness, 'X') and hasattr(witness, 'U'):
            X = witness.X
            U = witness.U
        elif isinstance(witness, dict):
            X = witness.get('X', witness.get('x'))
            U = witness.get('U', witness.get('u', X))
        elif isinstance(witness, tuple) and len(witness) == 2:
            X, U = witness
        else:
            X = witness
            U = witness
    except Exception:
        X = witness
        U = witness

    # H_1: U is an open subset of X
    try:
        h1_ok = bool(is_open_in(U, X))
    except Exception:
        h1_ok = False

    # ¬Q: U is NOT locally connected when equipped with the subspace topology
    try:
        neg_q_ok = not bool(is_locally_connected(U))
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: U is an open subset of X",
    "¬Q: U is not locally connected"
]

N_HYP = 1
NEG_Q_INDEX = 1