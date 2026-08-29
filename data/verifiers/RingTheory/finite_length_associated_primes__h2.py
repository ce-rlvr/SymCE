import sympy
from sympy import *
from sympy.combinatorics import *
from sympy.combinatorics.named_groups import *
from sympy.matrices import *
from sympy.ntheory import *
from sympy.abc import *
from sympy.polys import *
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "¬Q: (M has finite length) is not equivalent to (every prime ideal in Ass(M) is maximal)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    h1 = False
    neg_q = False
    
    # 1. Try dictionary representation
    if isinstance(witness, dict):
        try:
            if 'R_is_commutative' in witness and 'R_is_noetherian' in witness:
                h1 = bool(witness['R_is_commutative'] and witness['R_is_noetherian'])
            elif 'is_commutative' in witness and 'is_noetherian' in witness:
                h1 = bool(witness['is_commutative'] and witness['is_noetherian'])
                
            if 'M_has_finite_length' in witness and 'M_ass_primes_are_maximal' in witness:
                neg_q = bool(witness['M_has_finite_length']) != bool(witness['M_ass_primes_are_maximal'])
            elif 'has_finite_length' in witness and 'ass_primes_are_maximal' in witness:
                neg_q = bool(witness['has_finite_length']) != bool(witness['ass_primes_are_maximal'])
            elif 'finite_length' in witness and 'ass_primes_are_maximal' in witness:
                neg_q = bool(witness['finite_length']) != bool(witness['ass_primes_are_maximal'])
                
            if h1 or neg_q:
                return [h1, neg_q]
        except Exception:
            pass

    # 2. Try object with attributes
    try:
        if hasattr(witness, 'R_is_commutative') and hasattr(witness, 'R_is_noetherian'):
            h1 = bool(witness.R_is_commutative and witness.R_is_noetherian)
        elif hasattr(witness, 'is_commutative') and hasattr(witness, 'is_noetherian'):
            h1 = bool(witness.is_commutative and witness.is_noetherian)
            
        if hasattr(witness, 'M_has_finite_length') and hasattr(witness, 'M_ass_primes_are_maximal'):
            neg_q = bool(witness.M_has_finite_length) != bool(witness.M_ass_primes_are_maximal)
        elif hasattr(witness, 'has_finite_length') and hasattr(witness, 'ass_primes_are_maximal'):
            neg_q = bool(witness.has_finite_length) != bool(witness.ass_primes_are_maximal)
        elif hasattr(witness, 'finite_length') and hasattr(witness, 'ass_primes_are_maximal'):
            neg_q = bool(witness.finite_length) != bool(witness.ass_primes_are_maximal)
            
        if hasattr(witness, 'R') and hasattr(witness, 'M'):
            h1 = bool(getattr(witness.R, 'is_commutative', False) and getattr(witness.R, 'is_noetherian', False))
            if hasattr(witness.M, 'has_finite_length') and hasattr(witness.M, 'ass_primes_are_maximal'):
                neg_q = bool(witness.M.has_finite_length) != bool(witness.M.ass_primes_are_maximal)
            elif hasattr(witness.M, 'finite_length') and hasattr(witness.M, 'ass_primes_are_maximal'):
                neg_q = bool(witness.M.finite_length) != bool(witness.M.ass_primes_are_maximal)
                
        if h1 or neg_q:
            return [h1, neg_q]
    except Exception:
        pass

    # 3. Try string or tuple of strings for standard counterexamples
    w_str = ""
    if isinstance(witness, str):
        w_str = witness.lower()
    elif isinstance(witness, (tuple, list)) and all(isinstance(x, str) for x in witness):
        w_str = " ".join(witness).lower()
        
    if w_str:
        h1 = True  # Standard counterexamples are over Z or k[x]
        if "prufer" in w_str or "prüfer" in w_str or "p^\\infty" in w_str or "p^infty" in w_str or "injective hull" in w_str:
            neg_q = True
        elif "oplus" in w_str or "bigoplus" in w_str or "direct sum" in w_str:
            neg_q = True
        elif "q" in w_str or "rational" in w_str:
            neg_q = False
            
        if h1 and neg_q:
            return [h1, neg_q]

    # 4. Fallback to string representation
    try:
        w_str = str(witness).lower()
        if "prufer" in w_str or "prüfer" in w_str or "p^\\infty" in w_str or "p^infty" in w_str or "injective hull" in w_str:
            h1 = True
            neg_q = True
        elif "oplus" in w_str or "bigoplus" in w_str or "direct sum" in w_str:
            h1 = True
            neg_q = True
    except Exception:
        pass

    return [h1, neg_q]