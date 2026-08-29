import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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
    def _g(k, default):
        try:
            return witness[k] if isinstance(witness, dict) else getattr(witness, k)
        except Exception:
            return default

    try:
        return [
            bool(_g('is_integral_domain', False)),
            bool(_g('is_R_module', False)),
            bool(_g('S_is_multiplicatively_closed', False)),
            not bool(_g('localization_commutes_with_torsion', True))
        ]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS: list[str] = [
    "H_1: R is an integral domain",
    "H_2: M is an R-module",
    "H_3: S is a multiplicatively closed subset of R",
    "¬Q: The torsion submodule of S^{-1}M over S^{-1}R is NOT isomorphic to S^{-1}T(M)"
]

N_HYP: int = 3
NEG_Q_INDEX: int = 3