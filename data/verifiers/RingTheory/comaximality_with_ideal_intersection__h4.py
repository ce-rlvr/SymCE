import math
import itertools
import functools
from sympy import gcd, lcm, sympify
from sympy.abc import x, y, z, a, b, c

# Top-level setup
# We provide common symbols for polynomial rings.
# The witness is expected to be a tuple of 3 generators (integers or polynomials)
# representing the principal ideals I, J, K.

def extract_gen(val):
    """Extract the single generator if the ideal is given as a list/tuple/set."""
    if isinstance(val, (list, tuple, set)):
        val_list = list(val)
        if len(val_list) == 1:
            return val_list[0]
        else:
            raise ValueError("Only principal ideals (single generator) are supported")
    return val

def is_unit(val, has_symbols):
    """
    Determine if a value is a unit in the inferred ring.
    If symbols are present, we assume a polynomial ring over a field (e.g., Q[x]),
    where any non-zero constant is a unit.
    If no symbols are present, we assume the ring of integers Z,
    where the only units are 1 and -1.
    """
    try:
        val = sympify(val)
        if has_symbols:
            if val.is_constant():
                return val != 0
            return False
        else:
            if val.is_Integer:
                return abs(val) == 1
            if val.is_Rational:
                return val != 0
            if val.is_Float:
                return val != 0
            if val.is_constant():
                return val != 0
            return False
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 3:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: I, J, K are ideals of a commutative ring R
    try:
        i = extract_gen(witness[0])
        j = extract_gen(witness[1])
        k = extract_gen(witness[2])
        i_sym = sympify(i)
        j_sym = sympify(j)
        k_sym = sympify(k)
        # Check if they are valid ring elements by inspecting free_symbols
        has_syms = len(i_sym.free_symbols | j_sym.free_symbols | k_sym.free_symbols) > 0
        h1_ok = True
    except Exception:
        h1_ok = False

    if not h1_ok:
        return [False, False, False]

    # H_2: I and J are comaximal (I + J = R)
    try:
        ij_gcd = gcd(i_sym, j_sym)
        h2_ok = is_unit(ij_gcd, has_syms)
    except Exception:
        h2_ok = False

    # neg_Q: I and J \cap K are NOT comaximal (I + (J \cap K) != R)
    try:
        jk_lcm = lcm(j_sym, k_sym)
        ijk_gcd = gcd(i_sym, jk_lcm)
        neg_q_ok = not is_unit(ijk_gcd, has_syms)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: I, J, K are ideals of a commutative ring",
    "H_2: I and J are comaximal (I + J = R)",
    "¬Q: I and J \\cap K are not comaximal (I + (J \\cap K) != R)"
]

N_HYP = 2
NEG_Q_INDEX = 2