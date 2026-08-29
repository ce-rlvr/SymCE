import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    if isinstance(witness, dict):
        try:
            if all(k in witness for k in ("is_subgroup", "index_finite", "H_finitely_presented")):
                return [
                    bool(witness["is_subgroup"]),
                    bool(witness["index_finite"]),
                    not bool(witness["H_finitely_presented"])
                ]
        except Exception:
            pass

    # Extract G and H
    G = None
    H = None
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            G, H = witness
        elif hasattr(witness, "G") and hasattr(witness, "H"):
            G = witness.G
            H = witness.H
        else:
            G = witness
            H = witness
    except Exception:
        pass

    # H1: H is a subgroup of G
    h1 = False
    try:
        if hasattr(witness, "is_subgroup"):
            h1 = bool(witness.is_subgroup)
        elif G is not None and H is not None:
            if G == H:
                h1 = True
            elif hasattr(H, "is_subgroup"):
                h1 = bool(H.is_subgroup(G))
            elif hasattr(G, "has_subgroup"):
                h1 = bool(G.has_subgroup(H))
    except Exception:
        pass

    # H2: index of H in G is finite
    h2 = False
    try:
        if hasattr(witness, "index_finite"):
            h2 = bool(witness.index_finite)
        elif hasattr(witness, "finite_index"):
            h2 = bool(witness.finite_index)
        elif G is not None and H is not None:
            if G == H:
                h2 = True
            elif hasattr(G, "index"):
                idx = G.index(H)
                h2 = (idx != float('inf')) and (idx != sympy.oo)
    except Exception:
        pass

    # neg_Q: H is not finitely presented
    neg_q = False
    try:
        if hasattr(witness, "H_finitely_presented"):
            neg_q = not bool(witness.H_finitely_presented)
        elif hasattr(witness, "H_is_finitely_presented"):
            neg_q = not bool(witness.H_is_finitely_presented)
        elif H is not None:
            if hasattr(H, "is_finitely_presented"):
                val = H.is_finitely_presented
                if callable(val):
                    val = val()
                neg_q = not bool(val)
            elif hasattr(H, "is_fp"):
                val = H.is_fp
                if callable(val):
                    val = val()
                neg_q = not bool(val)
            elif hasattr(H, "fp"):
                val = H.fp
                if callable(val):
                    val = val()
                neg_q = not bool(val)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: The index of H in G is finite",
    "¬Q: H is not finitely presented"
]

N_HYP = 2
NEG_Q_INDEX = 2