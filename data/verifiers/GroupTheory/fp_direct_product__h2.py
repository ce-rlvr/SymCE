import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def is_finitely_presented(X):
    """Helper to determine if a group is finitely presented."""
    if isinstance(X, str):
        X = X.strip().lower()
        # Common families of finite/finitely presented groups
        if len(X) > 1 and X[0] in 'zsadcf' and X[1:].isdigit():
            return True
            
        fp_names = ['z', 'f2', 'trivial', '1', 'q8', 'v4']
        not_fp_names = ['q', 'r', 'f_infty', 'z2 wr z', 'lamplighter', 'q/z', 'z^infty', 'r*', 'q*', 'c_infty', 'c']
        
        if X in fp_names:
            return True
        if X in not_fp_names:
            return False
            
        # Direct or free products
        if 'x' in X:
            parts = X.split('x')
            if len(parts) > 1:
                return all(is_finitely_presented(p) for p in parts)
        if '*' in X:
            parts = X.split('*')
            if len(parts) > 1:
                return all(is_finitely_presented(p) for p in parts)
                
    # SymPy group objects
    class_name = type(X).__name__
    if class_name in ['PermutationGroup', 'FpGroup', 'FreeGroup', 'SymmetricGroup', 'AlternatingGroup', 'DihedralGroup', 'CyclicGroup']:
        return True
        
    if hasattr(X, 'is_finitely_presented'):
        if callable(X.is_finitely_presented):
            return X.is_finitely_presented()
        return bool(X.is_finitely_presented)
        
    raise ValueError(f"Cannot determine if {X} is finitely presented")

def conditions(witness) -> list[bool]:
    # Extract G and H from the witness
    try:
        if isinstance(witness, dict):
            G = witness.get('G', "Z")
            H = witness.get('H', witness)
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            G, H = witness
        elif hasattr(witness, 'G') and hasattr(witness, 'H'):
            G = witness.G
            H = witness.H
        else:
            # If only one group is provided, assume it is H and let G be the integers
            G = "Z"
            H = witness
    except Exception:
        return [False, False]
        
    # H_1: G is a finitely presented group
    try:
        h1_ok = is_finitely_presented(G)
    except Exception:
        h1_ok = False
        
    # neg_Q: The direct product G x H is NOT a finitely presented group
    try:
        g_fp = is_finitely_presented(G)
        h_fp = is_finitely_presented(H)
        # G x H is finitely presented iff both G and H are finitely presented
        g_x_h_fp = g_fp and h_fp
        neg_q_ok = not g_x_h_fp
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finitely presented group",
    "¬Q: The direct product G x H is not a finitely presented group"
]

N_HYP = 1
NEG_Q_INDEX = 1