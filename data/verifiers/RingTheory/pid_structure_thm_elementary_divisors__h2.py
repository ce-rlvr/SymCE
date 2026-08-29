import sympy
from sympy import S
import math
import itertools
import functools

# Top-level setup
Z = sympy.S.Integers
Q = sympy.S.Rationals
R = sympy.S.Reals
C = sympy.S.Complexes

KNOWN_PIDS = {
    "Z", "ZZ", "Integers", "S.Integers", "Z_p",
    "Q", "QQ", "Rationals", "S.Rationals",
    "R", "RR", "Reals", "S.Reals",
    "C", "CC", "Complexes", "S.Complexes",
    "Q[x]", "R[x]", "C[x]", "F_p[x]"
}

FAILING_MODULES_Z = {
    "Q", "QQ", "Rationals", "S.Rationals", "RationalField",
    "Q/Z", "QQ/ZZ",
    "R", "RR", "Reals", "S.Reals", "RealField",
    "C", "CC", "Complexes", "S.Complexes", "ComplexField",
    "prod_{i=1}^infty Z", "Z^N", "Z^omega",
    "oplus_{i=1}^infty Z_2", "Z_2^infty", "oplus Z_2",
    "Z_p^infty", "Prüfer", "Prufer", "Prufer p-group",
    "Q[x]", "QQ[x]", "p-adic integers"
}

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        ring, module = witness
    else:
        ring = "Z"
        module = witness
        
    def to_str(obj):
        if obj == sympy.S.Integers: return "Z"
        if obj == sympy.S.Rationals: return "Q"
        if obj == sympy.S.Reals: return "R"
        if obj == sympy.S.Complexes: return "C"
        if isinstance(obj, str): return obj.strip()
        return str(obj).strip()
        
    return to_str(ring), to_str(module)

def conditions(witness) -> list[bool]:
    try:
        ring, module = parse_witness(witness)
    except Exception:
        return [False, False]
        
    # H_1: R is a principal ideal domain
    try:
        h1 = (ring in KNOWN_PIDS)
    except Exception:
        h1 = False
        
    # neg_Q: M is NOT isomorphic to a direct sum of a free R-module and finitely many cyclic modules R/(p^k)
    try:
        neg_q = False
        if ring in {"Z", "ZZ", "Integers", "S.Integers"}:
            if module in FAILING_MODULES_Z:
                neg_q = True
        elif ring == "Q[x]":
            if module in {"Q(x)", "Rationals(x)"}:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a principal ideal domain",
    "¬Q: M is NOT isomorphic to a direct sum of a free R-module and finitely many cyclic modules of the form R/(p^k)"
]

N_HYP = 1
NEG_Q_INDEX = 1