import sympy
from sympy import ZZ, QQ

class Module:
    def __init__(self, ring, is_torsion, annihilator_is_zero):
        self.ring = ring
        self.is_torsion = is_torsion
        self.annihilator_is_zero = annihilator_is_zero

# Standard named objects for the witness namespace
Q_mod_Z = Module(ZZ, True, True)
DirectSum_Z_mod_nZ = Module(ZZ, True, True)
Z_mod_2Z = Module(ZZ, True, False)
Q_module = Module(ZZ, False, True)
Z_module = Module(ZZ, False, True)

def conditions(witness) -> list[bool]:
    # Handle string witnesses
    if isinstance(witness, str):
        w = witness.lower().replace(" ", "").replace("_", "")
        if "q/z" in w or "qmodz" in w or "directsum" in w:
            witness = Q_mod_Z

    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            ring, is_torsion, ann_zero = witness
        elif isinstance(witness, dict):
            ring = witness.get("ring", None)
            is_torsion = witness.get("is_torsion", False)
            ann_zero = witness.get("annihilator_is_zero", False)
        else:
            ring = getattr(witness, "ring", None)
            is_torsion = getattr(witness, "is_torsion", False)
            ann_zero = getattr(witness, "annihilator_is_zero", False)
    except Exception:
        return [False, False, False]

    try:
        h1 = False
        if ring in [ZZ, QQ, sympy.S.Integers, sympy.S.Rationals, sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
        elif hasattr(ring, "is_domain") and ring.is_domain:
            h1 = True
        elif hasattr(ring, "is_integral_domain") and ring.is_integral_domain:
            h1 = True
        elif ring is not None:
            for cls in type(ring).__mro__:
                if cls.__name__ == "Domain":
                    h1 = True
                    break
    except Exception:
        h1 = False

    try:
        h2 = bool(is_torsion)
    except Exception:
        h2 = False

    try:
        neg_q = bool(ann_zero)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: M is a torsion module",
    "¬Q: Ann_R(M) is zero"
]

N_HYP = 2
NEG_Q_INDEX = 2