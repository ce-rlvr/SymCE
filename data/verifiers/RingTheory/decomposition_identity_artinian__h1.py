import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import *
import math
import itertools
import functools

# Top-level setup
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
V4 = AlternatingGroup(4)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    neg_q = False
    try:
        # The conclusion fails if the identity element of R CANNOT be written as a sum 
        # of finitely many mutually orthogonal primitive central idempotents.
        # This typically happens in infinite direct products of rings, infinite Boolean rings,
        # or rings of sequences. We check if the witness represents such a ring.
        
        s = str(witness).replace(" ", "")
        s_lower = s.lower()
        
        if "infinite" in s_lower and ("product" in s_lower or "direct" in s_lower):
            neg_q = True
        elif "Z2^N" in s or "Z2**N" in s or "Z_2^N" in s or "Z_2**N" in s:
            neg_q = True
        elif "Z^N" in s or "Z**N" in s or "R^N" in s or "R**N" in s:
            neg_q = True
        elif "Q^N" in s or "Q**N" in s or "C^N" in s or "C**N" in s:
            neg_q = True
        elif "prod" in s_lower and ("oo" in s_lower or "infty" in s_lower or "N" in s or "\\mathbb{N}" in s):
            neg_q = True
        elif "boolean" in s_lower and "ring" in s_lower and ("N" in s or "\\mathbb{N}" in s or "infinite" in s_lower):
            neg_q = True
        elif "subset" in s_lower and ("N" in s or "\\mathbb{N}" in s or "infinite" in s_lower):
            neg_q = True
        elif "sequence" in s_lower and "ring" in s_lower:
            neg_q = True
        elif "End(" in s and "infinite" in s_lower:
            neg_q = True
        elif "l_infty" in s_lower or "linfty" in s_lower or "l^infty" in s_lower:
            neg_q = True
        elif "P(N)" in s or "P(\\mathbb{N})" in s:
            neg_q = True
        elif "**oo" in s_lower or "^oo" in s_lower or "**infty" in s_lower or "^infty" in s_lower:
            neg_q = True
        elif "\\mathbb{N}" in s and ("^" in s or "**" in s):
            neg_q = True
            
    except Exception:
        pass

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The identity element of R cannot be written as a sum of finitely many mutually orthogonal primitive central idempotents"
]

N_HYP = 0
NEG_Q_INDEX = 0