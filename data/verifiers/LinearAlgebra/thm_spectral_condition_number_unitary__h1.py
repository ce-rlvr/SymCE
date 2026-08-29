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

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        # Check if witness is a matrix-like object
        if not hasattr(witness, 'H') or not hasattr(witness, 'shape'):
            return [False]
        
        # Condition number is typically defined for non-empty matrices
        if len(witness.shape) != 2 or witness.shape[0] != witness.shape[1]:
            neg_q = True
        elif witness.shape[0] == 0:
            neg_q = True
        else:
            # The 2-norm condition number of a matrix A is exactly 1 
            # if and only if A^H * A = c * I for some real c > 0.
            AHA = witness.H * witness
            n = witness.shape[0]
            c = AHA[0, 0]
            
            c_re = sympy.simplify(sympy.re(c))
            c_im = sympy.simplify(sympy.im(c))
            
            if c_im != 0 or c_re <= 0:
                neg_q = True
            else:
                is_cI = True
                for i in range(n):
                    for j in range(n):
                        if i == j:
                            if sympy.simplify(AHA[i, j] - c) != 0:
                                is_cI = False
                                break
                        else:
                            if sympy.simplify(AHA[i, j]) != 0:
                                is_cI = False
                                break
                    if not is_cI:
                        break
                
                # neg_q is True if the condition number is NOT exactly 1
                neg_q = not is_cI
                
    except Exception:
        neg_q = False
        
    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The condition number of U with respect to the operator 2-norm is not exactly 1"
]

N_HYP = 0
NEG_Q_INDEX = 0