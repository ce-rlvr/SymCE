import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy import eye, zeros
import math
import itertools
import functools

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_fp(g):
    """
    Helper function to determine if a group is finitely presented.
    Handles SymPy groups, custom objects with properties, and string representations.
    """
    if hasattr(g, 'is_finitely_presented'):
        val = g.is_finitely_presented() if callable(g.is_finitely_presented) else g.is_finitely_presented
        if val is not None: 
            return bool(val)
            
    if hasattr(g, 'is_fp'):
        val = g.is_fp() if callable(g.is_fp) else g.is_fp
        if val is not None: 
            return bool(val)
            
    if isinstance(g, dict):
        if 'is_finitely_presented' in g: 
            return bool(g['is_finitely_presented'])
        if 'is_fp' in g: 
            return bool(g['is_fp'])
    
    if isinstance(g, str):
        g_lower = g.lower().strip()
        non_fp_exact = [
            'q', 'r', 'c', 'z wr z', 'f_infty', 'f_inf', 's_infty', 's_inf', 
            'q/z', 'r/z', 'z^infty', 'z^inf', 'z^omega'
        ]
        if g_lower in non_fp_exact:
            return False
        for kw in ['wreath', 'infty', 'infinity', 'prüfer', 'prufer', 'z[1/', 'z(p^', 'wr ']:
            if kw in g_lower:
                return False
        # Assume finitely presented for standard string names like 'Z', 'F2', 'S3'
        return True
        
    try:
        from sympy.combinatorics import PermutationGroup, FpGroup, FreeGroup
        if isinstance(g, (PermutationGroup, FpGroup, FreeGroup)):
            return True
    except ImportError:
        pass
        
    # Default to True for other finite objects (e.g. matrices over finite fields)
    return True

def conditions(witness) -> list[bool]:
    """
    Given a witness, which should be a tuple of two groups (G, H),
    checks if it satisfies the remaining hypothesis and falsifies the conclusion.
    """
    try:
        if not isinstance(witness, (tuple, list)) or len(witness) != 2:
            return [False, False]
            
        G, H = witness
        
        # H_1: H is a finitely presented group
        h1_ok = is_fp(H)
        
        # Conclusion Q: G x H is a finitely presented group.
        # G x H is finitely presented if and only if both G and H are finitely presented.
        # Therefore, neg_Q is True iff G x H is NOT finitely presented.
        neg_q_ok = not (is_fp(G) and is_fp(H))
        
        return [bool(h1_ok), bool(neg_q_ok)]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: H is a finitely presented group",
    "¬Q: The direct product G x H is not a finitely presented group"
]

N_HYP = 1
NEG_Q_INDEX = 1