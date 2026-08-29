import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.free_groups import free_group, FreeGroup
from sympy.combinatorics.fp_groups import FpGroup
from sympy.matrices import eye, zeros

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

F2_group = free_group("x, y")[0]

CONDITION_LABELS = [
    "H_1: H is a free group of rank 2",
    "¬Q: There does not exist an injective group homomorphism from F into H"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    if isinstance(witness, (tuple, list)) and len(witness) == 2:
        F, H = witness
    elif isinstance(witness, dict) and 'F' in witness and 'H' in witness:
        F = witness['F']
        H = witness['H']
    else:
        F = witness
        H = F2_group

    try:
        h1_ok = isinstance(H, FreeGroup) and len(H.generators) == 2
    except Exception:
        h1_ok = False

    try:
        if isinstance(H, FreeGroup):
            if isinstance(F, FreeGroup):
                if len(H.generators) >= 2:
                    embeds = True
                elif len(H.generators) == 1:
                    embeds = len(F.generators) <= 1
                else:
                    embeds = len(F.generators) == 0
            elif isinstance(F, FpGroup) and len(F.relators) == 0:
                if len(H.generators) >= 2:
                    embeds = True
                elif len(H.generators) == 1:
                    embeds = len(F.generators) <= 1
                else:
                    embeds = len(F.generators) == 0
            elif hasattr(F, 'order'):
                try:
                    ord_F = F.order()
                    if ord_F < float('inf'):
                        embeds = (ord_F == 1)
                    else:
                        embeds = False
                except Exception:
                    embeds = False
            else:
                embeds = False
        else:
            # If H is not a FreeGroup, we cannot easily decide embedding.
            # Default to embeds = True so neg_q = False (safe fallback).
            embeds = True
            
        neg_q = not embeds
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(neg_q)]