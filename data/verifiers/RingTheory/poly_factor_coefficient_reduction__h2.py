import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def conditions(witness):
    """
    Checks whether the given witness satisfies the hypotheses and falsifies the conclusion.
    """
    h1, h2, neg_q = False, False, False
    
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R, I = witness
            
            # Case 1: R is an integer n representing Z_n
            if isinstance(R, int) and R >= 2:
                h1 = True
                I_set = set(I)
                h2 = all(isinstance(e, int) and 0 <= e < R for e in I_set)
                
                is_ideal = True
                if 0 not in I_set:
                    is_ideal = False
                else:
                    for a in I_set:
                        for b in I_set:
                            if (a - b) % R not in I_set:
                                is_ideal = False
                        for r in range(R):
                            if (r * a) % R not in I_set:
                                is_ideal = False
                neg_q = not is_ideal
                return [h1, h2, neg_q]
                
            # Case 2: R is a collection of integers representing Z_n
            if isinstance(R, (list, set, tuple)) and all(isinstance(e, int) for e in R):
                R_set = set(R)
                n = len(R_set)
                if R_set == set(range(n)) and n >= 2:
                    h1 = True
                    I_set = set(I)
                    h2 = I_set.issubset(R_set)
                    
                    is_ideal = True
                    if 0 not in I_set:
                        is_ideal = False
                    else:
                        for a in I_set:
                            for b in I_set:
                                if (a - b) % n not in I_set:
                                    is_ideal = False
                            for r in R_set:
                                if (r * a) % n not in I_set:
                                    is_ideal = False
                    neg_q = not is_ideal
                    return [h1, h2, neg_q]
                    
        # Case 3: witness is just I (assume R = Z)
        if isinstance(witness, (list, set, tuple)):
            I_set = set(witness)
            if all(isinstance(e, int) for e in I_set):
                h1 = True
                h2 = True
                is_ideal = (I_set == {0})
                neg_q = not is_ideal
                return [h1, h2, neg_q]
                
    except Exception:
        pass

    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I(x) is the ideal of R(x) consisting of all polynomials with coefficients in I",
    "not Q: The factor ring R(x)/I(x) is not isomorphic to the polynomial ring (R/I)(x)"
]

N_HYP = 2
NEG_Q_INDEX = 2