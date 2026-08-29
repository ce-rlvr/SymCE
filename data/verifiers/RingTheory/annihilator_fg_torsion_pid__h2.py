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

class ModuleOverRing:
    def __init__(self, R_is_PID, M_is_torsion, ann_is_nonzero_principal):
        self.R_is_PID = R_is_PID
        self.M_is_torsion = M_is_torsion
        self.ann_is_nonzero_principal = ann_is_nonzero_principal

# Standard counterexamples (Ann(M) = {0}, which is not a non-zero principal ideal)
Q_mod_Z = ModuleOverRing(True, True, False)
Z_p_infty = ModuleOverRing(True, True, False)
DirectSum_Z_pZ = ModuleOverRing(True, True, False)
F_x_mod_F_poly = ModuleOverRing(True, True, False)
DirectSum_F_x_mod_x_i = ModuleOverRing(True, True, False)

# Non-counterexamples
Z_mod_nZ = ModuleOverRing(True, True, True)
Z_mod_2Z = ModuleOverRing(True, True, True)
Z_module = ModuleOverRing(True, False, False)
Q_module = ModuleOverRing(True, False, False)
Z_x_module = ModuleOverRing(False, True, False)

def conditions(witness) -> list[bool]:
    # Handle potential tuple wrappers (e.g., if witness is (Ring, Module))
    if isinstance(witness, tuple) and len(witness) == 2:
        if hasattr(witness[1], 'R_is_PID'):
            witness = witness[1]
        elif hasattr(witness[0], 'R_is_PID'):
            witness = witness[0]
            
    # Fallback for string representations
    if isinstance(witness, str):
        w_str = witness.lower().replace(" ", "").replace("_", "")
        if "q/z" in w_str or "qmodz" in w_str or "zpinfty" in w_str or "directsum" in w_str:
            witness = Q_mod_Z
        elif "z/2z" in w_str or "zmod2z" in w_str or "zmodnz" in w_str:
            witness = Z_mod_2Z

    try:
        h1_ok = bool(witness.R_is_PID)
    except Exception:
        h1_ok = False

    try:
        h2_ok = bool(witness.M_is_torsion)
    except Exception:
        h2_ok = False

    try:
        neg_q_ok = not bool(witness.ann_is_nonzero_principal)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: M is a torsion module",
    "¬Q: Ann(M) is not a non-zero principal ideal in R"
]

N_HYP = 2
NEG_Q_INDEX = 2