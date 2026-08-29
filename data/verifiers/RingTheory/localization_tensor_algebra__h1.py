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

# Top-level setup
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

def _check_prop(witness, prop_names, default=False):
    try:
        if isinstance(witness, dict):
            for p in prop_names:
                if p in witness:
                    return bool(witness[p])
        else:
            for p in prop_names:
                if hasattr(witness, p):
                    return bool(getattr(witness, p))
    except Exception:
        pass
    return default

def conditions(witness) -> list[bool]:
    if isinstance(witness, str):
        w = witness.lower()
        h1 = "module" in w or "m" in w
        h2 = "multiplicatively closed" in w or "s" in w
        q = "not isomorphic" not in w and "fails" not in w and "not defined" not in w and "bimodule" not in w
        return [h1, h2, not q]

    # H1: M is an R-module
    h1 = _check_prop(witness, ["is_R_module", "is_module", "M_is_R_module"], False)
    
    # H2: S is a multiplicatively closed subset of R
    h2 = _check_prop(witness, ["is_multiplicatively_closed", "S_is_multiplicatively_closed", "is_mult_closed"], False)
    
    # Q: The tensor algebra T_{S^{-1}R}(S^{-1}M) is naturally isomorphic to S^{-1}T_R(M)
    q = _check_prop(witness, ["is_naturally_isomorphic", "tensor_algebra_isomorphic", "localization_commutes", "isomorphic"], True)
    
    return [h1, h2, not q]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The tensor algebra T_{S^{-1}R}(S^{-1}M) is not naturally isomorphic to S^{-1}T_R(M) as S^{-1}R-algebras"
]

N_HYP = 2
NEG_Q_INDEX = 2