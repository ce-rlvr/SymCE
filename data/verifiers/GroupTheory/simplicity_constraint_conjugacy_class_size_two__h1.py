import sympy
import sympy.combinatorics
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
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    Returns a list of booleans: [H_1_ok, neg_Q_ok]
    """
    # H_1: There exists an element x in G such that the conjugacy class of x has exactly 2 elements
    try:
        h1_ok = False
        # Try using built-in conjugacy_classes method if available
        try:
            classes = witness.conjugacy_classes()
            for c in classes:
                if len(c) == 2:
                    h1_ok = True
                    break
        except Exception:
            pass
        
        # Fallback to manual computation
        if not h1_ok:
            try:
                elements = list(witness.elements)
            except Exception:
                elements = list(witness.generate())
                
            for x in elements:
                c_class = set()
                for g in elements:
                    c_class.add(g * x * ~g)
                if len(c_class) == 2:
                    h1_ok = True
                    break
    except Exception:
        h1_ok = False

    # ¬Q: G is a simple group (negation of "G is not a simple group")
    try:
        neg_q_ok = False
        if hasattr(witness, 'is_simple'):
            is_simp = witness.is_simple
            if callable(is_simp):
                neg_q_ok = bool(is_simp())
            else:
                neg_q_ok = bool(is_simp)
        else:
            # Fallback: A group is simple iff it has exactly 2 normal subgroups (itself and the trivial group)
            normal_sgs = witness.normal_subgroups()
            neg_q_ok = (len(list(normal_sgs)) == 2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: There exists an element x in G such that the conjugacy class of x has exactly 2 elements",
    "¬Q: G is a simple group"
]

N_HYP = 1
NEG_Q_INDEX = 1