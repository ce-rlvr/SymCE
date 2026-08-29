import sympy
import math
import itertools
import functools

class NormedSpace:
    def __init__(self, name, is_finite_dim):
        self.name = name
        self.is_finite_dim = is_finite_dim

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

# Infinite-dimensional spaces
l1 = NormedSpace("l1", False)
l2 = NormedSpace("l2", False)
lp = NormedSpace("lp", False)
linf = NormedSpace("linf", False)
c0 = NormedSpace("c0", False)
c = NormedSpace("c", False)
L1 = NormedSpace("L1", False)
L2 = NormedSpace("L2", False)
Lp = NormedSpace("Lp", False)
Linf = NormedSpace("Linf", False)
C_0_1 = NormedSpace("C[0,1]", False)
R_x = NormedSpace("R[x]", False)
C_x = NormedSpace("C[x]", False)

# Finite-dimensional spaces
R = NormedSpace("R", True)
C = NormedSpace("C", True)
R2 = NormedSpace("R^2", True)
R3 = NormedSpace("R^3", True)
Rn = NormedSpace("R^n", True)
Cn = NormedSpace("C^n", True)

KNOWN_SPACES = {
    "l1": False, "l^1": False, "l_1": False,
    "l2": False, "l^2": False, "l_2": False,
    "lp": False, "l^p": False, "l_p": False,
    "linf": False, "l^inf": False, "l_inf": False, "l^\\infty": False, "l_\\infty": False,
    "c0": False, "c_0": False,
    "c": False,
    "L1": False, "L^1": False, "L_1": False,
    "L2": False, "L^2": False, "L_2": False,
    "Lp": False, "L^p": False, "L_p": False,
    "Linf": False, "L^inf": False, "L_inf": False, "L^\\infty": False, "L_\\infty": False,
    "C[0,1]": False, "C([0,1])": False, "C(K)": False,
    "R[x]": False, "R[X]": False,
    "C[x]": False, "C[X]": False,
    "R": True, "R^1": True,
    "C": True, "C^1": True,
    "R^2": True, "R2": True,
    "R^3": True, "R3": True,
    "R^n": True, "Rn": True,
    "C^n": True, "Cn": True,
}

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, NormedSpace):
            h1 = True
            neg_q = not witness.is_finite_dim
        elif isinstance(witness, str):
            w_clean = witness.replace(" ", "")
            if w_clean in KNOWN_SPACES:
                h1 = True
                neg_q = not KNOWN_SPACES[w_clean]
        elif witness in [sympy.S.Reals, sympy.S.Complexes]:
            h1 = True
            neg_q = False
        elif isinstance(witness, tuple) and len(witness) == 2:
            if witness[0] in [sympy.S.Reals, sympy.S.Complexes] and isinstance(witness[1], int):
                h1 = True
                neg_q = False
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a normed vector space over the real or complex numbers",
    "¬Q: V is not finite-dimensional"
]

N_HYP = 1
NEG_Q_INDEX = 1