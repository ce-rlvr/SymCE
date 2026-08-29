import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

class ValuedField:
    def __init__(self, name, is_valuation, residue_field_alg_closed):
        self.name = name
        self.is_valuation = is_valuation
        self.residue_field_alg_closed = residue_field_alg_closed

# Standard valued fields for witness expressions
Q_p = ValuedField("Q_p", True, False)
R_t = ValuedField("R((t))", True, False)
C_t = ValuedField("C((t))", True, True)
Fp_t = ValuedField("F_p((t))", True, False)
Q_trivial = ValuedField("Q_trivial", True, False)
C_trivial = ValuedField("C_trivial", True, True)

def conditions(witness) -> list[bool]:
    if isinstance(witness, str):
        mapping = {
            "Q_p": Q_p,
            "R((t))": R_t,
            "C((t))": C_t,
            "F_p((t))": Fp_t,
            "Q_trivial": Q_trivial,
            "C_trivial": C_trivial
        }
        witness = mapping.get(witness, witness)

    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get("is_valuation", False))
        else:
            h1 = bool(witness.is_valuation)
    except Exception:
        h1 = False

    try:
        if isinstance(witness, dict):
            neg_q = not bool(witness.get("residue_field_alg_closed", True))
        else:
            neg_q = not bool(witness.residue_field_alg_closed)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: v is a valuation on K with valuation ring O_v and maximal ideal m_v",
    "¬Q: The residue field O_v / m_v is not an algebraically closed field"
]

N_HYP = 1
NEG_Q_INDEX = 1