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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: M is an R-module",
    "H_3: k is a non-negative integer",
    "¬Q: Sym^k_{S^{-1}R}(S^{-1}M) is not naturally isomorphic to S^{-1}Sym^k_R(M)"
]

def conditions(witness) -> list[bool]:
    h1, h2, h3, neg_q = False, False, False, False
    
    try:
        if callable(witness):
            witness = witness()
            
        if isinstance(witness, dict):
            h1 = bool(witness.get('R_is_commutative', witness.get('h1', False)))
            h2 = bool(witness.get('M_is_R_module', witness.get('h2', False)))
            h3 = bool(witness.get('k_is_non_negative_integer', witness.get('h3', False)))
            neg_q = bool(witness.get('neg_q', not witness.get('is_isomorphic', True)))
            return [h1, h2, h3, neg_q]
            
        if hasattr(witness, 'R_is_commutative') or hasattr(witness, 'h1'):
            h1 = bool(getattr(witness, 'R_is_commutative', getattr(witness, 'h1', False)))
            h2 = bool(getattr(witness, 'M_is_R_module', getattr(witness, 'h2', False)))
            h3 = bool(getattr(witness, 'k_is_non_negative_integer', getattr(witness, 'h3', False)))
            neg_q = bool(getattr(witness, 'neg_q', not getattr(witness, 'is_isomorphic', True)))
            return [h1, h2, h3, neg_q]
            
        if isinstance(witness, tuple) and len(witness) >= 3:
            R, M, k = witness[0], witness[1], witness[2]
            
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                h1 = True
                
            if hasattr(M, 'is_module'):
                h2 = bool(M.is_module)
            else:
                h2 = True
                
            h3 = isinstance(k, int) and k >= 0
            
            # Mathematically, localization always commutes with symmetric powers.
            # If a tuple is provided, we assume it's not a valid counterexample unless specified.
            neg_q = False
            return [h1, h2, h3, neg_q]
            
        if isinstance(witness, str):
            s = witness.lower()
            h1 = "commutative" in s or "h1: true" in s
            h2 = "module" in s or "h2: true" in s
            h3 = ("k" in s and "integer" in s) or "h3: true" in s
            neg_q = "not isomorphic" in s or "neg_q: true" in s or "false" in s
            return [h1, h2, h3, neg_q]
            
    except Exception:
        pass

    return [h1, h2, h3, neg_q]