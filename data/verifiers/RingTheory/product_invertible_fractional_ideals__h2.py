import sympy
import sympy.abc
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def call_or_get(obj, attr, *args):
    """Helper to safely get an attribute and call it if it's a method."""
    val = getattr(obj, attr)
    if callable(val):
        try:
            return val(*args)
        except TypeError:
            return val()
    return val

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    Returns [H_1, H_2, H_3, neg_Q].
    """
    # 1. Check if witness is a dictionary (mocked witness)
    if isinstance(witness, dict):
        try:
            h1 = bool(witness["R_is_integral_domain"])
            h2 = bool(witness["I_is_nonzero_invertible_fractional_ideal"])
            h3 = bool(witness["J_is_nonzero_invertible_fractional_ideal"])
            ij_inv = bool(witness.get("IJ_is_invertible_fractional_ideal", True))
            inv_eq = bool(witness.get("IJ_inverse_equals_I_inv_J_inv", True))
            neg_q = not (ij_inv and inv_eq)
            return [h1, h2, h3, neg_q]
        except KeyError:
            pass

    # 2. Check if witness is a tuple (R, I, J) or an object with R, I, J attributes
    witness_tuple = None
    if hasattr(witness, 'R') and hasattr(witness, 'I') and hasattr(witness, 'J'):
        witness_tuple = (witness.R, witness.I, witness.J)
    elif isinstance(witness, tuple) and len(witness) == 3:
        witness_tuple = witness

    if witness_tuple is not None:
        R, I, J = witness_tuple
        
        try:
            h1 = bool(call_or_get(R, 'is_integral_domain'))
        except Exception:
            h1 = False
            
        try:
            try:
                i_nz = bool(call_or_get(I, 'is_nonzero'))
            except AttributeError:
                i_nz = bool(I != 0)
            i_inv = bool(call_or_get(I, 'is_invertible', R))
            i_frac = bool(call_or_get(I, 'is_fractional_ideal', R))
            h2 = i_nz and i_inv and i_frac
        except Exception:
            h2 = False
            
        try:
            try:
                j_nz = bool(call_or_get(J, 'is_nonzero'))
            except AttributeError:
                j_nz = bool(J != 0)
            j_inv = bool(call_or_get(J, 'is_invertible', R))
            j_frac = bool(call_or_get(J, 'is_fractional_ideal', R))
            h3 = j_nz and j_inv and j_frac
        except Exception:
            h3 = False
            
        try:
            IJ = I * J
            ij_inv = bool(call_or_get(IJ, 'is_invertible', R))
            ij_frac = bool(call_or_get(IJ, 'is_fractional_ideal', R))
            
            I_inv = call_or_get(I, 'inverse')
            J_inv = call_or_get(J, 'inverse')
            IJ_inv = call_or_get(IJ, 'inverse')
            
            inv_eq = (IJ_inv == I_inv * J_inv)
            
            neg_q = not (ij_inv and ij_frac and inv_eq)
        except Exception:
            neg_q = False
            
        return [h1, h2, h3, neg_q]

    # 3. Check if witness is an object with the specific boolean properties
    try:
        h1 = bool(call_or_get(witness, 'R_is_integral_domain'))
        h2 = bool(call_or_get(witness, 'I_is_nonzero_invertible_fractional_ideal'))
        h3 = bool(call_or_get(witness, 'J_is_nonzero_invertible_fractional_ideal'))
        
        try:
            ij_inv = bool(call_or_get(witness, 'IJ_is_invertible_fractional_ideal'))
        except AttributeError:
            ij_inv = True
            
        try:
            inv_eq = bool(call_or_get(witness, 'IJ_inverse_equals_I_inv_J_inv'))
        except AttributeError:
            inv_eq = True
            
        neg_q = not (ij_inv and inv_eq)
        return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "H_2: I is a non-zero invertible fractional ideal of R",
    "H_3: J is a non-zero invertible fractional ideal of R",
    "¬Q: The product ideal IJ is not an invertible fractional ideal, or its inverse is not the product of the inverses of I and J"
]

N_HYP = 3
NEG_Q_INDEX = 3