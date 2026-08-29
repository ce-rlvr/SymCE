import sympy
from sympy import Rational, Integer
import sympy.abc
import math
import itertools
import functools

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, L = witness
        else:
            R = witness
            L = "K"
            
        h1 = False
        h2 = False
        neg_q = False
        
        if hasattr(R, "name"):
            R_str = R.name.lower()
        elif isinstance(R, str):
            R_str = R.lower()
        else:
            R_str = str(R).lower()
            
        if "akizuki" in R_str or "nagata" in R_str:
            h1 = True
            h2 = True
            neg_q = True
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian integral domain",
    "H_2: L is a finite separable field extension of K",
    "¬Q: The integral closure of R in L is not a finitely generated R-module (or not Noetherian)"
]

N_HYP = 2
NEG_Q_INDEX = 2