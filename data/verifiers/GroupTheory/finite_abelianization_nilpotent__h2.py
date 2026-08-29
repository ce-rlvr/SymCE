import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.combinatorics.free_groups import free_group, FreeGroup
from sympy.combinatorics.fp_groups import FpGroup

# Standard finite groups
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

# Infinite nilpotent group (Z)
F1, (x,) = free_group("x")
Z_group = FpGroup(F1, [])
Z = Z_group

def conditions(witness):
    # H_1: G is a nilpotent group
    h1 = False
    try:
        val = getattr(witness, 'is_nilpotent', None)
        if callable(val): 
            val = val()
        if val is True:
            h1 = True
    except Exception:
        pass

    if not h1:
        try:
            val = getattr(witness, 'is_abelian', None)
            if callable(val): 
                val = val()
            if val is True:
                h1 = True
        except Exception:
            pass

    if not h1:
        try:
            gens = list(witness.generators)
            if len(gens) <= 1:
                h1 = True
            else:
                is_ab = True
                for i in range(len(gens)):
                    for j in range(i+1, len(gens)):
                        if gens[i]*gens[j] != gens[j]*gens[i]:
                            is_ab = False
                            break
                    if not is_ab:
                        break
                if is_ab:
                    h1 = True
        except Exception:
            pass

    # neg_Q: G is not a finite group
    neg_q = False
    try:
        val = getattr(witness, 'is_finite', None)
        if callable(val): 
            val = val()
        if val is False:
            neg_q = True
    except Exception:
        pass

    if not neg_q:
        try:
            val = getattr(witness, 'order', None)
            if callable(val): 
                val = val()
            if val == sympy.oo or val == float('inf'):
                neg_q = True
        except Exception:
            pass

    if not neg_q:
        try:
            if hasattr(witness, 'relators') and hasattr(witness, 'generators'):
                if len(list(witness.generators)) > 0 and len(list(witness.relators)) == 0:
                    neg_q = True
        except Exception:
            pass

    if not neg_q:
        try:
            if isinstance(witness, FreeGroup) and len(list(witness.generators)) > 0:
                neg_q = True
        except Exception:
            pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G is a nilpotent group",
    "¬Q: G is not a finite group"
]

N_HYP = 1
NEG_Q_INDEX = 1