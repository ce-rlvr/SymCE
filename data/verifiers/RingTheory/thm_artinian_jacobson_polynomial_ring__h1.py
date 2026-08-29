import sympy
import sympy.combinatorics
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        # H_1: J(R) is the Jacobson radical of R
        # This is a definitional hypothesis, so it holds for any valid ring witness.
        h1 = True
        
        # ¬Q: The Jacobson radical of the polynomial ring over R is not exactly the polynomial ring over J(R)
        # For any ring R, J(R[x]) = N(R)[x] where N(R) is the nilradical.
        # Thus, J(R[x]) != J(R)[x] if and only if J(R) != N(R).
        if isinstance(witness, str):
            s = witness.replace(" ", "").lower()
            # Known counterexamples where J(R) != N(R)
            if "powerseries" in s or "local" in s or "p-adic" in s or "z_p" in s:
                neg_q = True
        elif hasattr(witness, "jacobson_radical") and hasattr(witness, "nilradical"):
            if callable(witness.jacobson_radical):
                neg_q = witness.jacobson_radical() != witness.nilradical()
            else:
                neg_q = witness.jacobson_radical != witness.nilradical
        elif hasattr(witness, "J") and hasattr(witness, "N"):
            neg_q = witness.J != witness.N
        elif isinstance(witness, dict) and "J" in witness and "N" in witness:
            neg_q = witness["J"] != witness["N"]
        elif isinstance(witness, tuple) and len(witness) >= 2:
            neg_q = witness[0] != witness[1]
            
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: J(R) is the Jacobson radical of R",
    "¬Q: The Jacobson radical of the polynomial ring over R is not exactly the polynomial ring over J(R)"
]

N_HYP = 1
NEG_Q_INDEX = 1