import math
import itertools
import sympy
from sympy import Matrix, Rational, eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
    # Try tuple unpacking (R, I, J)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
            h1 = bool(R.is_invertible_ideal(I) and R.is_invertible_ideal(J))
            h2 = bool(R.are_comaximal(I, J))
            inter = R.intersection(I, J)
            neg_q = not bool(R.is_invertible_ideal(inter))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # Try dict with R, I, J
    try:
        if isinstance(witness, dict) and 'R' in witness and 'I' in witness and 'J' in witness:
            R = witness['R']
            I = witness['I']
            J = witness['J']
            h1 = bool(R.is_invertible_ideal(I) and R.is_invertible_ideal(J))
            h2 = bool(R.are_comaximal(I, J))
            inter = R.intersection(I, J)
            neg_q = not bool(R.is_invertible_ideal(inter))
            return [h1, h2, neg_q]
    except Exception:
        pass

    # H1: Let I and J be invertible ideals of R
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('I_is_invertible', False) and witness.get('J_is_invertible', False))
            if not h1 and 'is_invertible_ideal' in witness:
                h1 = bool(witness['is_invertible_ideal'](witness['I']) and witness['is_invertible_ideal'](witness['J']))
        else:
            h1 = bool(getattr(witness, 'I_is_invertible', False) and getattr(witness, 'J_is_invertible', False))
            if not h1 and hasattr(witness, 'is_invertible_ideal'):
                h1 = bool(witness.is_invertible_ideal(witness.I) and witness.is_invertible_ideal(witness.J))
    except Exception:
        h1 = False

    # H2: Let I and J be comaximal
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('are_comaximal', False))
            if not h2 and 'check_comaximal' in witness:
                h2 = bool(witness['check_comaximal'](witness['I'], witness['J']))
        else:
            h2 = bool(getattr(witness, 'are_comaximal', False))
            if not h2 and hasattr(witness, 'check_comaximal'):
                h2 = bool(witness.check_comaximal(witness.I, witness.J))
    except Exception:
        h2 = False

    # neg_Q: The intersection I \cap J is NOT an invertible ideal of R
    try:
        if isinstance(witness, dict):
            if 'intersection_is_invertible' in witness:
                neg_q = not bool(witness['intersection_is_invertible'])
            elif 'is_invertible_ideal' in witness and 'intersection' in witness:
                inter = witness['intersection']
                if callable(inter):
                    inter = inter(witness['I'], witness['J'])
                neg_q = not bool(witness['is_invertible_ideal'](inter))
            else:
                neg_q = False
        else:
            if hasattr(witness, 'intersection_is_invertible'):
                neg_q = not bool(witness.intersection_is_invertible)
            elif hasattr(witness, 'is_invertible_ideal'):
                if hasattr(witness, 'intersection'):
                    inter = witness.intersection
                    if callable(inter):
                        inter = inter(witness.I, witness.J)
                    neg_q = not bool(witness.is_invertible_ideal(inter))
                else:
                    neg_q = False
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are invertible ideals of R",
    "H_2: I and J are comaximal",
    "¬Q: The intersection I \\cap J is not an invertible ideal of R"
]

N_HYP = 2
NEG_Q_INDEX = 2