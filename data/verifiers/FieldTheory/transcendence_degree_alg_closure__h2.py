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

# Top-level setup: named object bindings
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

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    Since SymPy does not natively support algebraic closures and transcendence degrees,
    the witness is expected to be a mock object or dictionary exposing these properties.
    """
    h1 = False
    h2 = False
    neg_q = False

    # H_1: K is a field
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('K_is_field', witness.get('is_field', False)))
        else:
            if hasattr(witness, 'K_is_field'):
                h1 = bool(witness.K_is_field)
            elif hasattr(witness, 'is_field'):
                h1 = bool(witness.is_field)
            elif hasattr(witness, 'K') and hasattr(witness.K, 'is_Field'):
                h1 = bool(witness.K.is_Field)
            elif hasattr(witness, 'K') and hasattr(witness.K, 'is_field'):
                h1 = bool(witness.K.is_field)
    except Exception:
        pass

    # H_2: K_bar is the algebraic closure of K
    try:
        if isinstance(witness, dict):
            h2 = bool(witness.get('K_bar_is_algebraic_closure', witness.get('is_algebraic_closure', False)))
        else:
            if hasattr(witness, 'K_bar_is_algebraic_closure'):
                h2 = bool(witness.K_bar_is_algebraic_closure)
            elif hasattr(witness, 'is_algebraic_closure'):
                h2 = bool(witness.is_algebraic_closure)
            elif hasattr(witness, 'K_bar_is_alg_closure'):
                h2 = bool(witness.K_bar_is_alg_closure)
    except Exception:
        pass

    # ¬Q: The transcendence degree of K_bar over P is NOT equal to the transcendence degree of K over P
    try:
        if isinstance(witness, dict):
            if 'trdeg_K_bar_P' in witness and 'trdeg_K_P' in witness:
                neg_q = witness['trdeg_K_bar_P'] != witness['trdeg_K_P']
            elif 'trdeg_K_bar' in witness and 'trdeg_K' in witness:
                neg_q = witness['trdeg_K_bar'] != witness['trdeg_K']
        else:
            if hasattr(witness, 'trdeg_K_bar_P') and hasattr(witness, 'trdeg_K_P'):
                neg_q = witness.trdeg_K_bar_P != witness.trdeg_K_P
            elif hasattr(witness, 'trdeg_K_bar') and hasattr(witness, 'trdeg_K'):
                neg_q = witness.trdeg_K_bar != witness.trdeg_K
            elif hasattr(witness, 'K_bar') and hasattr(witness, 'K') and hasattr(witness, 'P'):
                if hasattr(witness.K_bar, 'transcendence_degree') and hasattr(witness.K, 'transcendence_degree'):
                    neg_q = witness.K_bar.transcendence_degree(witness.P) != witness.K.transcendence_degree(witness.P)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: K is a field",
    "H_2: K_bar is the algebraic closure of K",
    "¬Q: The transcendence degree of K_bar over P is NOT equal to the transcendence degree of K over P"
]

N_HYP = 2
NEG_Q_INDEX = 2