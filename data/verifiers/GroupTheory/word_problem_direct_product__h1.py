import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup: named object bindings
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

def get_G_H(witness):
    if isinstance(witness, tuple) and len(witness) == 2:
        return witness[0], witness[1]
    elif hasattr(witness, 'G') and hasattr(witness, 'H'):
        return witness.G, witness.H
    elif isinstance(witness, dict) and 'G' in witness and 'H' in witness:
        return witness['G'], witness['H']
    else:
        raise ValueError("Cannot extract G and H from witness")

def has_solvable_word_problem(g):
    if hasattr(g, 'has_solvable_word_problem'):
        val = g.has_solvable_word_problem
        return val() if callable(val) else bool(val)
    if isinstance(g, dict) and 'has_solvable_word_problem' in g:
        return bool(g['has_solvable_word_problem'])
    if isinstance(g, str):
        return True
    return True

def is_finitely_generated(g):
    if hasattr(g, 'is_finitely_generated'):
        val = g.is_finitely_generated
        return val() if callable(val) else bool(val)
    if isinstance(g, dict) and 'is_finitely_generated' in g:
        return bool(g['is_finitely_generated'])
    if isinstance(g, str):
        if "inf" in g.lower() or g in ["Q", "R", "Q+", "R+", "Z[1/2]", "Q_add"]:
            return False
        return True
    return True

def conditions(witness) -> list[bool]:
    try:
        G, H = get_G_H(witness)
    except Exception:
        return [False, False, False, False]
    
    try:
        h1 = has_solvable_word_problem(G)
    except Exception:
        h1 = False

    try:
        h2 = is_finitely_generated(H)
    except Exception:
        h2 = False

    try:
        h3 = has_solvable_word_problem(H)
    except Exception:
        h3 = False

    try:
        if hasattr(witness, 'direct_product_has_solvable_word_problem'):
            val = witness.direct_product_has_solvable_word_problem
            q = val() if callable(val) else bool(val)
        elif isinstance(witness, dict) and 'direct_product_has_solvable_word_problem' in witness:
            q = bool(witness['direct_product_has_solvable_word_problem'])
        else:
            # The direct product G x H has a solvable word problem iff both G and H 
            # are finitely generated and both have solvable word problems.
            q = is_finitely_generated(G) and is_finitely_generated(H) and \
                has_solvable_word_problem(G) and has_solvable_word_problem(H)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G has a solvable word problem",
    "H_2: H is a finitely generated group",
    "H_3: H has a solvable word problem",
    "¬Q: The direct product G × H does not have a solvable word problem"
]

N_HYP = 3
NEG_Q_INDEX = 3
