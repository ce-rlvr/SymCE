import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import oo
import math
import itertools
import functools
import z3

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    h1 = False
    try:
        if hasattr(witness, 'is_free_group'):
            h1 = bool(witness.is_free_group)
        elif type(witness).__name__ == 'FreeGroup':
            h1 = True
        elif isinstance(witness, str) and 'free group' in witness.lower():
            h1 = True
    except Exception:
        pass

    neg_q = False
    try:
        if type(witness).__name__ == 'FreeGroup':
            neg_q = False
        else:
            rank = getattr(witness, 'rank', None)
            
            if hasattr(witness, 'embeds_in_SL2R'):
                neg_q = not bool(witness.embeds_in_SL2R)
            elif hasattr(witness, 'admits_injective_homomorphism_into_SL2R'):
                neg_q = not bool(witness.admits_injective_homomorphism_into_SL2R)
            elif rank is not None:
                s_rank = str(rank).lower().replace(' ', '')
                if s_rank in ['aleph(2)', 'aleph_2', '>continuum', 'greaterthancontinuum', 'uncountable']:
                    neg_q = True
                elif 'continuum' in s_rank and '>' in s_rank:
                    neg_q = True
                elif '2**aleph(0)' in s_rank and '+' in s_rank:
                    neg_q = True
            elif isinstance(witness, str):
                s = witness.lower()
                if 'aleph_2' in s or 'aleph(2)' in s or '> continuum' in s or 'greater than continuum' in s or 'uncountable' in s:
                    neg_q = True
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group",
    "¬Q: F does not admit an injective group homomorphism into SL(2, R)"
]

N_HYP = 1
NEG_Q_INDEX = 1