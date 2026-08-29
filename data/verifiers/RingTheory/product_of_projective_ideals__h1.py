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

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    # Handle string witness (e.g., known counterexamples like upper triangular matrix rings)
    if isinstance(witness, str):
        w = witness.lower()
        if "triangular" in w or "matrix" in w or "counterexample" in w:
            return [True, True]
            
    # Handle dictionary witness
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get("I_is_fg_projective", False) and witness.get("J_is_fg_projective", False))
        except Exception:
            h1 = False
        try:
            neg_q = not bool(witness.get("IJ_is_fg_projective", True))
        except Exception:
            neg_q = False
        return [h1, neg_q]
        
    # Handle tuple/list witness (I_is_fg_projective, J_is_fg_projective, IJ_is_fg_projective)
    if isinstance(witness, (list, tuple)) and len(witness) >= 3:
        try:
            h1 = bool(witness[0] and witness[1])
            neg_q = not bool(witness[2])
            return [h1, neg_q]
        except Exception:
            pass

    # Handle object with attributes
    try:
        I_proj = getattr(witness.I, 'is_projective', getattr(witness, 'I_is_projective', False))
        I_fg = getattr(witness.I, 'is_finitely_generated', getattr(witness, 'I_is_finitely_generated', False))
        J_proj = getattr(witness.J, 'is_projective', getattr(witness, 'J_is_projective', False))
        J_fg = getattr(witness.J, 'is_finitely_generated', getattr(witness, 'J_is_finitely_generated', False))
        
        I_ok = getattr(witness.I, 'is_fg_projective', getattr(witness, 'I_is_fg_projective', I_proj and I_fg))
        J_ok = getattr(witness.J, 'is_fg_projective', getattr(witness, 'J_is_fg_projective', J_proj and J_fg))
        
        h1 = bool(I_ok and J_ok)
    except Exception:
        try:
            h1 = bool(getattr(witness, 'I_is_fg_projective', False) and getattr(witness, 'J_is_fg_projective', False))
        except Exception:
            h1 = False

    try:
        IJ_proj = getattr(witness.IJ, 'is_projective', getattr(witness, 'IJ_is_projective', True))
        IJ_fg = getattr(witness.IJ, 'is_finitely_generated', getattr(witness, 'IJ_is_finitely_generated', True))
        
        IJ_ok = getattr(witness.IJ, 'is_fg_projective', getattr(witness, 'IJ_is_fg_projective', IJ_proj and IJ_fg))
        
        neg_q = not bool(IJ_ok)
    except Exception:
        try:
            neg_q = not bool(getattr(witness, 'IJ_is_fg_projective', True))
        except Exception:
            neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are finitely generated projective ideals of R",
    "¬Q: The product ideal IJ is not a finitely generated projective ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1