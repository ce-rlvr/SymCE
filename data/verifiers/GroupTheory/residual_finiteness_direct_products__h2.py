import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

class MockGroup:
    """
    A mock group class to allow users to easily specify groups with 
    a known residual finiteness property, since SymPy does not natively 
    decide residual finiteness for infinite finitely presented groups.
    """
    def __init__(self, name, is_res_fin):
        self.name = name
        self.is_res_fin = is_res_fin
    
    @property
    def is_residually_finite(self):
        return self.is_res_fin
        
    def __str__(self):
        return self.name
        
    def __repr__(self):
        return f"MockGroup({self.name}, {self.is_res_fin})"

# Standard finite groups (all are residually finite)
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

# A known non-residually finite group for convenience
BS23 = MockGroup("BS(2,3)", False)

CONDITION_LABELS = [
    "H_1: G is a residually finite group",
    "¬Q: The direct product G x H is not a residually finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        # The witness should provide both G and H.
        if isinstance(witness, dict):
            if 'G' in witness and 'H' in witness:
                G = witness['G']
                H = witness['H']
            else:
                return [False, False]
        elif isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        else:
            return [False, False]
            
        def is_rf(grp):
            # Check for explicit property
            if hasattr(grp, 'is_residually_finite'):
                val = grp.is_residually_finite
                return val() if callable(val) else val
                
            # Direct products
            if isinstance(grp, tuple):
                return all(is_rf(g) for g in grp)
                
            # String parsing for known groups
            if isinstance(grp, str):
                s = grp.replace(" ", "").lower()
                if "bs(" in s:
                    try:
                        inner = s.split("bs(")[1].split(")")[0]
                        m_str, n_str = inner.split(",")
                        a, b = abs(int(m_str)), abs(int(n_str))
                        if a == 1 or b == 1 or a == b:
                            return True
                        return False
                    except Exception:
                        return False
                if "non" in s or "not" in s or "false" in s:
                    return False
                if "residuallyfinite" in s:
                    return True
                    
            # Finite groups are residually finite
            if hasattr(grp, 'is_finite'):
                val = grp.is_finite
                if callable(val): val = val()
                if val: return True
                
            # Known SymPy group types
            if type(grp).__name__ in ['PermutationGroup', 'FreeGroup']:
                return True
                
            # Heuristic for FpGroup (e.g., Baumslag-Solitar)
            if type(grp).__name__ == 'FpGroup':
                try:
                    rels = str(grp.relators)
                    if ("b**2" in rels and "b**-3" in rels) or ("b**3" in rels and "b**-2" in rels):
                        return False
                except Exception:
                    pass
                    
            # Default to True to avoid false positives for neg_Q
            return True

        # Evaluate conditions
        h1 = bool(is_rf(G))
        
        # The direct product G x H is residually finite iff both G and H are.
        # Thus, it is NOT residually finite iff at least one is NOT.
        neg_q = not (is_rf(G) and is_rf(H))
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]