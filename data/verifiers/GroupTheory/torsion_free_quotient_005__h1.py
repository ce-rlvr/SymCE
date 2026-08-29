import sympy
from sympy import S
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: The torsion elements of G form a subgroup T",
    "¬Q: The quotient group G/T is not a free abelian group"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False

    # 1. Check if witness is a string
    if isinstance(witness, str):
        w = witness.lower().strip()
        if w in ["q", "rationals", "r", "reals", "c", "complexes", "heisenberg", "z^omega", "freegroup(2)"]:
            return [True, True]
        if w in ["z", "integers", "s3", "s4", "a4", "v4", "d4", "q/z"]:
            return [True, False]

    # 2. Check if witness is a sympy Set
    try:
        if witness in (S.Rationals, S.Reals, S.Complexes):
            return [True, True]
        if witness == S.Integers:
            return [True, False]
    except Exception:
        pass

    # 3. Check duck typing for custom objects
    custom_obj = False
    try:
        if hasattr(witness, "torsion_elements_form_subgroup"):
            h1 = bool(witness.torsion_elements_form_subgroup())
            custom_obj = True
        elif hasattr(witness, "has_torsion_subgroup"):
            h1 = bool(witness.has_torsion_subgroup)
            custom_obj = True
        elif hasattr(witness, "is_abelian"):
            if callable(witness.is_abelian):
                h1 = bool(witness.is_abelian())
            else:
                h1 = bool(witness.is_abelian)
    except Exception:
        pass

    try:
        if hasattr(witness, "quotient_is_free_abelian"):
            neg_q = not bool(witness.quotient_is_free_abelian())
            custom_obj = True
        elif hasattr(witness, "is_quotient_free_abelian"):
            neg_q = not bool(witness.is_quotient_free_abelian)
            custom_obj = True
    except Exception:
        pass

    if custom_obj:
        return [h1, neg_q]

    # 4. Check if witness is a PermutationGroup
    try:
        if isinstance(witness, PermutationGroup):
            return [True, False]
    except Exception:
        pass

    # 5. Check if witness is a FreeGroup
    if type(witness).__name__ == "FreeGroup":
        try:
            if len(witness.generators) > 1:
                return [True, True]
            else:
                return [True, False]
        except Exception:
            pass

    # 6. Check if witness is an FpGroup
    if type(witness).__name__ == "FpGroup":
        try:
            gens = witness.generators
            is_abelian = True
            for i in range(len(gens)):
                for j in range(i+1, len(gens)):
                    if gens[i]*gens[j] != gens[j]*gens[i]:
                        is_abelian = False
                        break
            if is_abelian:
                return [True, False]
            else:
                if len(witness.relators) == 0:
                    if len(gens) > 1:
                        return [True, True]
                    else:
                        return [True, False]
        except Exception:
            pass

    # 7. Check if witness is a list of integers (invariant factors)
    if isinstance(witness, list) and all(isinstance(x, int) for x in witness):
        return [True, False]

    return [h1, neg_q]