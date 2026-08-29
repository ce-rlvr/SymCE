import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    """
    # H_1: G admits a presentation with exactly one defining relation
    h1 = False
    try:
        if hasattr(witness, 'relators'):
            h1 = len(witness.relators) == 1
        elif hasattr(witness, 'relations'):
            h1 = len(witness.relations) == 1
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            h1 = len(witness[1]) == 1
        elif isinstance(witness, dict):
            if 'relators' in witness:
                h1 = len(witness['relators']) == 1
            elif 'relations' in witness:
                h1 = len(witness['relations']) == 1
    except Exception:
        pass

    # ¬Q: G does NOT have a solvable word problem
    neg_q = False
    try:
        if hasattr(witness, 'has_solvable_word_problem'):
            neg_q = not bool(witness.has_solvable_word_problem)
        elif hasattr(witness, 'solvable_word_problem'):
            neg_q = not bool(witness.solvable_word_problem)
        elif hasattr(witness, 'word_problem_solvable'):
            neg_q = not bool(witness.word_problem_solvable)
        elif isinstance(witness, dict):
            if 'has_solvable_word_problem' in witness:
                neg_q = not bool(witness['has_solvable_word_problem'])
            elif 'solvable_word_problem' in witness:
                neg_q = not bool(witness['solvable_word_problem'])
            elif 'word_problem_solvable' in witness:
                neg_q = not bool(witness['word_problem_solvable'])
    except Exception:
        pass

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: G admits a presentation with exactly one defining relation",
    "¬Q: G does not have a solvable word problem"
]

N_HYP = 1
NEG_Q_INDEX = 1