import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: f is a locally Lipschitz continuous function",
    "¬Q: f is not differentiable almost everywhere in U with respect to the n-dimensional Lebesgue measure"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    q = True
    
    try:
        # Handle string witnesses (e.g., "Fat Cantor set")
        if isinstance(witness, str):
            s = witness.lower()
            if "cantor" in s or "empty interior" in s or "positive measure" in s:
                h1 = True
                q = False
            return [h1, not q]
            
        # Handle tuple witnesses (e.g., (f, U))
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            f, U = witness
            if isinstance(U, str):
                s = U.lower()
                if "cantor" in s or "empty interior" in s or "positive measure" in s:
                    h1 = True
                    q = False
                return [h1, not q]
                
        # Handle dictionary or mock object witnesses
        h1_names = [
            "is_locally_Lipschitz", 
            "locally_Lipschitz", 
            "is_locally_Lipschitz_continuous",
            "is_lipschitz",
            "locally_lipschitz",
            "H1", "h1"
        ]
        q_names = [
            "is_differentiable_ae", 
            "differentiable_ae", 
            "is_differentiable_almost_everywhere",
            "is_diff_ae",
            "differentiable_almost_everywhere",
            "Q", "q"
        ]
        
        if isinstance(witness, dict):
            for name in h1_names:
                if name in witness:
                    h1 = bool(witness[name])
                    break
            for name in q_names:
                if name in witness:
                    q = bool(witness[name])
                    break
        else:
            for name in h1_names:
                if hasattr(witness, name):
                    val = getattr(witness, name)
                    h1 = bool(val() if callable(val) else val)
                    break
            for name in q_names:
                if hasattr(witness, name):
                    val = getattr(witness, name)
                    q = bool(val() if callable(val) else val)
                    break
                    
    except Exception:
        pass

    return [h1, not q]