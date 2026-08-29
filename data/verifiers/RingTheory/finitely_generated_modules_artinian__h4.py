import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

class Ring:
    def __init__(self, is_ring=True, has_identity=True, is_left_artinian=True, is_right_artinian=True):
        self.is_ring = is_ring
        self.has_identity = has_identity
        self.is_left_artinian = is_left_artinian
        self.is_right_artinian = is_right_artinian

class Module:
    def __init__(self, ring, is_finitely_generated=True, is_artinian=True):
        self.ring = ring
        self.is_finitely_generated = is_finitely_generated
        self.is_artinian = is_artinian

# A standard counterexample: 
# R = [[Q, R], [0, R]] is left Artinian but not right Artinian.
# M = R_R (R considered as a right module over itself) is finitely generated (by 1) but not Artinian.
R_counter = Ring(is_ring=True, has_identity=True, is_left_artinian=True, is_right_artinian=False)
M_counter = Module(ring=R_counter, is_finitely_generated=True, is_artinian=False)
counterexample = (R_counter, M_counter)

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    h3 = False
    h4 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("R_is_ring", witness.get("is_ring", False)))
            h2 = bool(witness.get("R_has_identity", witness.get("has_identity", False)))
            h3 = bool(witness.get("R_is_left_artinian", witness.get("is_left_artinian", False)))
            h4 = bool(witness.get("M_is_finitely_generated", witness.get("is_finitely_generated", False)))
            neg_q = not bool(witness.get("M_is_artinian", witness.get("is_artinian", True)))
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, M = witness
            h1 = bool(getattr(R, "is_ring", False))
            h2 = bool(getattr(R, "has_identity", False))
            h3 = bool(getattr(R, "is_left_artinian", False))
            h4 = bool(getattr(M, "is_finitely_generated", False))
            neg_q = not bool(getattr(M, "is_artinian", True))
        else:
            h1 = bool(getattr(witness, "R_is_ring", False))
            h2 = bool(getattr(witness, "R_has_identity", False))
            h3 = bool(getattr(witness, "R_is_left_artinian", False))
            h4 = bool(getattr(witness, "M_is_finitely_generated", False))
            neg_q = not bool(getattr(witness, "M_is_artinian", True))
    except Exception:
        pass

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: R has a multiplicative identity",
    "H_3: R is a left Artinian ring",
    "H_4: M is finitely generated",
    "¬Q: M is not an Artinian module"
]

N_HYP = 4
NEG_Q_INDEX = 4