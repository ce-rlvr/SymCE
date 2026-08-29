import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import itertools
import functools
import math

S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: K1 is an algebraic closure of F",
    "H_2: K2 is an algebraic closure of F",
    "¬Q: There does not exist a field isomorphism φ: K1 → K2 such that φ(x) = x for all x in F"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False

    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('H_1', witness.get('K1_is_algebraic_closure', False)))
            h2 = bool(witness.get('H_2', witness.get('K2_is_algebraic_closure', False)))
            neg_q = bool(witness.get('neg_Q', not witness.get('isomorphic_over_F', True)))
            return [h1, h2, neg_q]
        except Exception:
            pass

    try:
        h1 = bool(getattr(witness, 'K1_is_algebraic_closure', False))
    except Exception:
        pass

    try:
        h2 = bool(getattr(witness, 'K2_is_algebraic_closure', False))
    except Exception:
        pass

    try:
        if hasattr(witness, 'isomorphic_over_F'):
            neg_q = not bool(witness.isomorphic_over_F)
        elif hasattr(witness, 'neg_Q'):
            neg_q = bool(witness.neg_Q)
    except Exception:
        pass

    if h1 or h2 or neg_q:
        return [h1, h2, neg_q]

    try:
        if isinstance(witness, (list, tuple)) and len(witness) == 3:
            F, K1, K2 = witness
            
            try:
                h1 = bool(K1.is_algebraic_closure(F))
            except Exception:
                pass
                
            try:
                h2 = bool(K2.is_algebraic_closure(F))
            except Exception:
                pass
                
            try:
                neg_q = not bool(K1.is_isomorphic(K2, over=F))
            except Exception:
                pass
    except Exception:
        pass

    return [h1, h2, neg_q]