import sympy
import sympy.combinatorics
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.SymmetricGroup(3)
S4 = sympy.combinatorics.SymmetricGroup(4)
A4 = sympy.combinatorics.AlternatingGroup(4)
D4 = sympy.combinatorics.DihedralGroup(4)
C4 = sympy.combinatorics.CyclicGroup(4)
V4 = sympy.combinatorics.AlternatingGroup(4)
Z2 = sympy.combinatorics.CyclicGroup(2)
Z3 = sympy.combinatorics.CyclicGroup(3)
Z4 = sympy.combinatorics.CyclicGroup(4)
Z6 = sympy.combinatorics.CyclicGroup(6)
trivial = sympy.combinatorics.CyclicGroup(1)
I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness.get('R')
            M = witness.get('M')
            S = witness.get('S')
            k = witness.get('k')
        elif isinstance(witness, tuple) and len(witness) == 4:
            R, M, S, k = witness
        else:
            R = getattr(witness, 'R', None)
            M = getattr(witness, 'M', None)
            S = getattr(witness, 'S', None)
            k = getattr(witness, 'k', None)
    except Exception:
        R, M, S, k = None, None, None, None

    # H1: M is an R-module
    try:
        if hasattr(witness, 'is_R_module'):
            h1 = witness.is_R_module()
        elif hasattr(M, 'is_module'):
            h1 = M.is_module(R)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: S is a multiplicatively closed subset of R
    try:
        if hasattr(witness, 'is_multiplicatively_closed'):
            h2 = witness.is_multiplicatively_closed()
        elif hasattr(S, 'is_multiplicatively_closed'):
            h2 = S.is_multiplicatively_closed(R)
        else:
            h2 = False
    except Exception:
        h2 = False

    # H3: k is a non-negative integer
    try:
        if hasattr(witness, 'is_valid_k'):
            h3 = witness.is_valid_k()
        else:
            h3 = (isinstance(k, int) or isinstance(k, sympy.Integer)) and int(k) >= 0
    except Exception:
        h3 = False

    # neg_Q: Sym^k_{S^{-1}R}(S^{-1}M) is not naturally isomorphic to S^{-1}Sym^k_R(M)
    try:
        if hasattr(witness, 'conclusion_holds'):
            neg_q = not witness.conclusion_holds()
        elif hasattr(witness, 'is_isomorphic'):
            neg_q = not witness.is_isomorphic()
        elif hasattr(M, 'localize') and hasattr(M, 'symmetric_power'):
            sym_loc = M.localize(S).symmetric_power(k)
            loc_sym = M.symmetric_power(k).localize(S)
            neg_q = not sym_loc.is_isomorphic(loc_sym)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: M is an R-module",
    "H_2: S is a multiplicatively closed subset of R",
    "H_3: k is a non-negative integer",
    "¬Q: Sym^k_{S^-1 R}(S^-1 M) is not naturally isomorphic to S^-1 Sym^k_R(M)"
]

N_HYP = 3
NEG_Q_INDEX = 3