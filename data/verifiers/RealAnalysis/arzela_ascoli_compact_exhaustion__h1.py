import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
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
    "H_1: {f_n} is a sequence of real-valued functions on X",
    "H_2: {f_n} is pointwise bounded on X",
    "H_3: {f_n} is an equicontinuous family on X",
    "¬Q: No subsequence of {f_n} converges uniformly on every compact subset of X"
]

def conditions(witness) -> list[bool]:
    # 1. Fallback for tuple/list witness
    if isinstance(witness, (list, tuple)) and len(witness) >= 4:
        try:
            h1 = bool(witness[0])
            h2 = bool(witness[1])
            h3 = bool(witness[2])
            neg_q = not bool(witness[3])
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Dictionary with exact labels
    if isinstance(witness, dict):
        try:
            if CONDITION_LABELS[0] in witness:
                h1 = bool(witness[CONDITION_LABELS[0]])
                h2 = bool(witness[CONDITION_LABELS[1]])
                h3 = bool(witness[CONDITION_LABELS[2]])
                neg_q = bool(witness[CONDITION_LABELS[3]])
                return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 3. Property extraction
    def get_prop(names):
        for name in names:
            if isinstance(witness, dict) and name in witness:
                val = witness[name]
                return bool(val()) if callable(val) else bool(val)
            if hasattr(witness, name):
                val = getattr(witness, name)
                return bool(val()) if callable(val) else bool(val)
        return None

    try:
        h1_val = get_prop([
            'is_sequence_of_real_valued_functions',
            'is_real_valued_sequence',
            'real_valued',
            'is_real_valued'
        ])
        h1 = False if h1_val is None else h1_val
    except Exception:
        h1 = False

    try:
        h2_val = get_prop([
            'is_pointwise_bounded',
            'pointwise_bounded'
        ])
        h2 = False if h2_val is None else h2_val
    except Exception:
        h2 = False

    try:
        h3_val = get_prop([
            'is_equicontinuous',
            'equicontinuous',
            'is_equicontinuous_family'
        ])
        h3 = False if h3_val is None else h3_val
    except Exception:
        h3 = False

    try:
        q_val = get_prop([
            'has_convergent_subsequence_on_compact_subsets',
            'has_uniformly_convergent_subsequence',
            'converges_uniformly_on_compact_subsets',
            'has_convergent_subsequence'
        ])
        neg_q = True if q_val is False else False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]