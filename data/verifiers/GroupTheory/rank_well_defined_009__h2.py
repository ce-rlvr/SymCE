import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

# Top-level setup: named object bindings
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

Z = sympy.Symbol('Z')

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should provide a free abelian group F, and two integers n, m.
    It can be a tuple (F, n, m), a tuple (n, m) where F is implicitly Z, or a dict.
    """
    try:
        if isinstance(witness, dict):
            F = witness.get('F', 'Z')
            n = witness.get('n')
            m = witness.get('m')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                F, n, m = witness
            elif len(witness) == 2:
                F = 'Z'
                n, m = witness
            else:
                return [False, False]
        else:
            return [False, False]
            
        # H_1: F is a free abelian group
        h1_ok = False
        try:
            if isinstance(F, int) and F >= 0:
                h1_ok = True
            elif isinstance(F, str):
                s = F.replace(" ", "").lower()
                if s == "z" or s.startswith("z^") or s.startswith("z**") or "freeabelian" in s:
                    h1_ok = True
            elif str(F) == "Z":
                h1_ok = True
            elif isinstance(F, (list, tuple)) and all(x == 0 for x in F):
                h1_ok = True
            elif type(F).__name__ == 'FreeGroup' and F.rank <= 1:
                h1_ok = True
            elif hasattr(F, 'is_abelian') and F.is_abelian and hasattr(F, 'is_free') and F.is_free:
                h1_ok = True
        except Exception:
            pass
            
        # ¬Q: n != m
        neg_q_ok = False
        try:
            if n is not None and m is not None:
                neg_q_ok = bool(n != m)
        except Exception:
            pass
            
        return [h1_ok, neg_q_ok]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: F is a free abelian group",
    "¬Q: n != m"
]

N_HYP = 1
NEG_Q_INDEX = 1