import sympy
import sympy.combinatorics
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy does not have a built-in abstract module theory or localization,
    this verifier relies on the witness providing its own evaluation methods
    or being a dictionary with pre-evaluated boolean flags.
    """
    h1_ok = False
    h2_ok = False
    neg_q_ok = False

    # H_1: R is a commutative ring
    try:
        if hasattr(witness, 'is_commutative_ring'):
            h1_ok = witness.is_commutative_ring()
        elif hasattr(witness, 'check_h1'):
            h1_ok = witness.check_h1()
        elif isinstance(witness, dict) and 'H1' in witness:
            h1_ok = witness['H1']
        elif hasattr(witness, 'R') and hasattr(witness.R, 'is_commutative'):
            h1_ok = witness.R.is_commutative
        elif isinstance(witness, tuple) and len(witness) >= 1 and hasattr(witness[0], 'is_commutative'):
            h1_ok = witness[0].is_commutative
    except Exception:
        h1_ok = False

    # H_2: {M_i}_{i \in I} is a family of R-modules indexed by an arbitrary set I
    try:
        if hasattr(witness, 'is_family_of_modules'):
            h2_ok = witness.is_family_of_modules()
        elif hasattr(witness, 'check_h2'):
            h2_ok = witness.check_h2()
        elif isinstance(witness, dict) and 'H2' in witness:
            h2_ok = witness['H2']
    except Exception:
        h2_ok = False

    # ¬Q: The localized module S^{-1}(\bigoplus_{i \in I} M_i) is NOT isomorphic to \bigoplus_{i \in I} (S^{-1}M_i)
    try:
        if hasattr(witness, 'conclusion_holds'):
            neg_q_ok = not witness.conclusion_holds()
        elif hasattr(witness, 'is_isomorphic'):
            neg_q_ok = not witness.is_isomorphic()
        elif hasattr(witness, 'check_neg_q'):
            neg_q_ok = witness.check_neg_q()
        elif isinstance(witness, dict) and 'neg_Q' in witness:
            neg_q_ok = witness['neg_Q']
    except Exception:
        neg_q_ok = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q_ok)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: {M_i}_{i \\in I} is a family of R-modules indexed by an arbitrary set I",
    "¬Q: The localized module S^{-1}(\\bigoplus_{i \\in I} M_i) is NOT isomorphic to \\bigoplus_{i \\in I} (S^{-1}M_i) as S^{-1}R-modules"
]

N_HYP = 2
NEG_Q_INDEX = 2