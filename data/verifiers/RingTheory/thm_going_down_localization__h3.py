import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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
    Given a witness object, checks whether it is a valid counterexample to the conjecture.
    Returns a list of booleans: [H_1_ok, H_2_ok, neg_Q_ok].
    """
    # H_1: R is a commutative ring
    h1 = False
    try:
        if hasattr(witness, 'is_commutative_ring'):
            val = witness.is_commutative_ring
            h1 = bool(val() if callable(val) else val)
        elif isinstance(witness, dict) and 'is_commutative_ring' in witness:
            h1 = bool(witness['is_commutative_ring'])
        elif hasattr(witness, 'R'):
            R = witness.R
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                h1 = True
        elif isinstance(witness, tuple) and len(witness) >= 1:
            R = witness[0]
            if hasattr(R, 'is_commutative'):
                h1 = bool(R.is_commutative)
            else:
                h1 = True
        else:
            h1 = True
    except Exception:
        h1 = False

    # H_2: S is a multiplicative subset of R
    h2 = False
    try:
        if hasattr(witness, 'is_multiplicative_subset'):
            val = witness.is_multiplicative_subset
            h2 = bool(val() if callable(val) else val)
        elif isinstance(witness, dict) and 'is_multiplicative_subset' in witness:
            h2 = bool(witness['is_multiplicative_subset'])
        elif hasattr(witness, 'S'):
            S = witness.S
            if hasattr(S, '__iter__'):
                try:
                    S_list = list(itertools.islice(S, 20))
                except Exception:
                    S_list = []
                is_mult = True
                for a in S_list:
                    for b in S_list:
                        if (a * b) not in S_list:
                            is_mult = False
                            break
                    if not is_mult:
                        break
                h2 = is_mult
            else:
                h2 = True
        elif isinstance(witness, tuple) and len(witness) >= 2:
            S = witness[1]
            if hasattr(S, '__iter__'):
                try:
                    S_list = list(itertools.islice(S, 20))
                except Exception:
                    S_list = []
                is_mult = True
                for a in S_list:
                    for b in S_list:
                        if (a * b) not in S_list:
                            is_mult = False
                            break
                    if not is_mult:
                        break
                h2 = is_mult
            else:
                h2 = True
        else:
            h2 = True
    except Exception:
        h2 = False

    # neg_Q: The map phi does NOT satisfy the going-down theorem
    # Note: Mathematically, the going-down theorem ALWAYS holds for the localization 
    # of any commutative ring. Thus, for any valid mathematical object, neg_Q is False.
    # We provide hooks for mock objects that might be used in testing environments.
    neg_q = False
    try:
        if hasattr(witness, 'satisfies_going_down'):
            val = witness.satisfies_going_down
            neg_q = not bool(val() if callable(val) else val)
        elif hasattr(witness, 'going_down_property'):
            val = witness.going_down_property
            neg_q = not bool(val() if callable(val) else val)
        elif isinstance(witness, dict) and 'satisfies_going_down' in witness:
            neg_q = not bool(witness['satisfies_going_down'])
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a multiplicative subset of R",
    "¬Q: The map phi does not satisfy the going-down theorem"
]

N_HYP = 2
NEG_Q_INDEX = 2