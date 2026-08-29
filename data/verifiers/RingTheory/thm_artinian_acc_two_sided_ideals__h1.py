import sympy
import sympy.combinatorics
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample.
    The conjecture claims that any ring satisfies the ascending chain condition (ACC) on two-sided ideals.
    A valid counterexample must be a ring that does NOT satisfy the ACC (i.e., a non-Noetherian ring).
    """
    try:
        def satisfies_acc(w):
            # If the object explicitly defines its Noetherian property
            if hasattr(w, 'is_Noetherian') and w.is_Noetherian is not None:
                return w.is_Noetherian
                
            # SymPy's Expression Domain is non-Noetherian
            try:
                from sympy import EX
                if w == EX:
                    return False
            except ImportError:
                pass
                
            s = str(w).lower()
            
            # Check if the string representation looks like a ring
            looks_like_ring = (
                "ring" in s or 
                "[" in s or 
                s == "ex" or 
                "domain" in s or
                "algebra" in s
            )
            
            if looks_like_ring:
                # Polynomial rings with infinitely many variables
                if any(x in s for x in ["...", "infinit", "dots"]):
                    return False
                # Rings of continuous functions or algebraic integers
                if any(x in s for x in ["continuous", "algebraic integer"]):
                    return False
                # Explicitly stated non-Noetherian rings
                if any(x in s for x in ["non-noetherian", "not noetherian"]):
                    return False
                # Free algebras and tensor algebras on >= 2 generators are non-Noetherian
                if any(x in s for x in ["free algebra", "tensor algebra"]):
                    return False
                    
            # Default to True (meaning it satisfies ACC, so it's NOT a counterexample)
            return True

        neg_q = not satisfies_acc(witness)
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: R does not satisfy the ascending chain condition on two-sided ideals"
]

N_HYP = 0
NEG_Q_INDEX = 0