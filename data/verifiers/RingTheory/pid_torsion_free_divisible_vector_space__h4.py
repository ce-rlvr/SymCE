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

# Top-level setup: named object bindings for Rings, Fields, and Modules
class Ring:
    def __init__(self, name, is_PID, frac_field):
        self.name = name
        self.is_PID = is_PID
        self.frac_field = frac_field

class Field:
    def __init__(self, name):
        self.name = name

class Module:
    def __init__(self, name, ring, is_divisible, has_unique_K_vs):
        self.name = name
        self.ring = ring
        self.is_divisible = is_divisible
        self.has_unique_K_vs = has_unique_K_vs

Q = Field("Q")
R_field = Field("R")
C_field = Field("C")
Q_x = Field("Q(x)")

Z = Ring("Z", is_PID=True, frac_field=Q)
Q_ring = Ring("Q", is_PID=True, frac_field=Q)
Z_x = Ring("Z[x]", is_PID=False, frac_field=Q_x)

Q_mod_Z = Module("Q/Z", Z, is_divisible=True, has_unique_K_vs=False)
Z_p_infty = Module("Z(p^infty)", Z, is_divisible=True, has_unique_K_vs=False)
Q_module = Module("Q", Z, is_divisible=True, has_unique_K_vs=True)
R_module = Module("R", Z, is_divisible=True, has_unique_K_vs=True)
Z_module = Module("Z", Z, is_divisible=False, has_unique_K_vs=False)


def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R_obj, K_obj, M_obj = witness
        elif isinstance(witness, dict):
            R_obj = witness.get('R')
            K_obj = witness.get('K')
            M_obj = witness.get('M')
        else:
            M_obj = witness
            R_obj = M_obj.ring
            K_obj = R_obj.frac_field
            
        # H_1: R is a principal ideal domain
        h1 = False
        try:
            h1 = bool(R_obj.is_PID)
        except Exception:
            pass
            
        # H_2: K is the field of fractions of R
        h2 = False
        try:
            h2 = (K_obj == R_obj.frac_field)
        except Exception:
            pass
            
        # H_3: M is an R-module
        h3 = False
        try:
            h3 = (M_obj.ring == R_obj)
        except Exception:
            pass
            
        # H_4: M is divisible
        h4 = False
        try:
            h4 = bool(M_obj.is_divisible)
        except Exception:
            pass
            
        # ¬Q: M does NOT admit a unique K-vector space structure extending its R-module structure
        neg_q = False
        try:
            neg_q = not bool(M_obj.has_unique_K_vs)
        except Exception:
            pass
            
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]


CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "H_2: K is the field of fractions of R",
    "H_3: M is an R-module",
    "H_4: M is divisible",
    "¬Q: M does not admit a unique K-vector space structure extending its R-module structure"
]

N_HYP = 4
NEG_Q_INDEX = 4