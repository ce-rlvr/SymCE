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

# Top-level setup for Ring Theory
ZZ = sympy.ZZ
QQ = sympy.QQ
x, y, z = sympy.abc.x, sympy.abc.y, sympy.abc.z

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness should be a tuple (R, I, J) or a dictionary with keys 'R', 'I', 'J'.
    """
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            I = witness.get('I')
            J = witness.get('J')
        else:
            R, I, J = witness
    except Exception:
        return [False, False, False]

    # H_1: R is a commutative ring with identity
    try:
        h1 = True
        if hasattr(R, 'is_commutative') and not R.is_commutative:
            h1 = False
        
        has_id = False
        if hasattr(R, 'one') and R.one is not None:
            has_id = True
        elif hasattr(R, 'identity') and R.identity is not None:
            has_id = True
        elif hasattr(R, 'has_Identity') and R.has_Identity:
            has_id = True
            
        if not has_id:
            h1 = False
    except Exception:
        h1 = False

    # H_2: I and J are comaximal, meaning I + J = R
    try:
        sum_IJ = I + J
        h2 = False
        if sum_IJ == R:
            h2 = True
        elif hasattr(sum_IJ, 'is_whole_ring') and sum_IJ.is_whole_ring():
            h2 = True
        elif hasattr(R, 'one') and hasattr(sum_IJ, 'contains') and sum_IJ.contains(R.one):
            h2 = True
        elif hasattr(R, 'one') and hasattr(R, 'ideal') and sum_IJ == R.ideal(R.one):
            h2 = True
        elif sum_IJ == 1:
            h2 = True
        elif hasattr(R, 'one') and sum_IJ == R.one:
            h2 = True
    except Exception:
        h2 = False

    # ¬Q: The intersection I \cap J is NOT equal to the product ideal IJ
    try:
        if hasattr(I, 'intersect'):
            int_IJ = I.intersect(J)
        elif hasattr(I, 'intersection'):
            int_IJ = I.intersection(J)
        else:
            int_IJ = I & J
            
        if hasattr(I, 'mul'):
            prod_IJ = I.mul(J)
        else:
            prod_IJ = I * J
            
        neg_q = (int_IJ != prod_IJ)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are comaximal (I + J = R)",
    "¬Q: The intersection I \\cap J is NOT equal to the product ideal IJ"
]

N_HYP = 2
NEG_Q_INDEX = 2