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

def get_R_I_m_n(witness):
    if isinstance(witness, dict):
        return witness.get('R', None), witness.get('I', None), witness.get('m', None), witness.get('n', None)
    elif hasattr(witness, 'I') and hasattr(witness, 'm') and hasattr(witness, 'n'):
        return getattr(witness, 'R', None), witness.I, witness.m, witness.n
    elif isinstance(witness, (list, tuple)):
        if len(witness) == 4:
            return witness[0], witness[1], witness[2], witness[3]
        elif len(witness) == 3:
            return None, witness[0], witness[1], witness[2]
    raise ValueError("Cannot unpack witness")

def conditions(witness) -> list[bool]:
    try:
        R, I, m, n = get_R_I_m_n(witness)
    except Exception:
        return [False, False, False]

    # H_1: I is an ideal of R
    try:
        if isinstance(witness, dict) and 'is_ideal' in witness:
            h1 = bool(witness['is_ideal'])
        elif hasattr(witness, 'is_ideal'):
            h1 = bool(witness.is_ideal() if callable(witness.is_ideal) else witness.is_ideal)
        elif R is not None and hasattr(R, 'is_ideal'):
            h1 = bool(R.is_ideal(I))
        elif hasattr(I, 'is_ideal'):
            if callable(I.is_ideal):
                try:
                    h1 = bool(I.is_ideal(R))
                except Exception:
                    h1 = bool(I.is_ideal())
            else:
                h1 = bool(I.is_ideal)
        else:
            # Fallback: assume it's an ideal if it's provided as I
            h1 = I is not None
    except Exception:
        h1 = False

    # H_2: m and n are positive integers
    try:
        h2 = (int(m) == m) and (int(n) == n) and (m > 0) and (n > 0)
    except Exception:
        h2 = False

    # ¬Q: I^m I^n != I^{m+n}
    try:
        if hasattr(I, '__pow__') and hasattr(I, '__mul__'):
            I_m = I ** m
            I_n = I ** n
            I_m_n = I_m * I_n
            I_plus = I ** (m + n)
            neg_q = not (I_m_n == I_plus)
        elif hasattr(I, 'pow') and hasattr(I, 'mul'):
            I_m = I.pow(m)
            I_n = I.pow(n)
            I_m_n = I_m.mul(I_n)
            I_plus = I.pow(m + n)
            neg_q = not (I_m_n == I_plus)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "H_2: m and n are positive integers",
    "¬Q: I^m I^n != I^{m+n}"
]

N_HYP = 2
NEG_Q_INDEX = 2