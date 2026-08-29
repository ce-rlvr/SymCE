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

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("bounded_domain", False) and witness.get("smooth_boundary", False))
            for key in ["Omega_bounded_smooth", "is_bounded_domain_with_smooth_boundary", "H1"]:
                if key in witness:
                    h1 = bool(witness[key])
                    
            h2 = bool(witness.get("L2_bounded", False))
            for key in ["U_0_L2_bounded", "is_L2_bounded_family", "H2"]:
                if key in witness:
                    h2 = bool(witness[key])
                    
            is_equicont = witness.get("equicontinuous", True)
            for key in ["F_t_equicontinuous", "is_uniformly_equicontinuous", "Q"]:
                if key in witness:
                    is_equicont = bool(witness[key])
            neg_q = not is_equicont
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Omega is a bounded domain with smooth boundary",
    "H_2: U_0 is a family of initial data functions bounded in L^2(Omega)",
    "¬Q: The family of functions F_t is not uniformly equicontinuous on Omega"
]

N_HYP = 2
NEG_Q_INDEX = 2