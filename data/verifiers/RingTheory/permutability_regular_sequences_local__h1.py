import itertools
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness expressions
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

CONDITION_LABELS = [
    "H_1: R is a local ring with maximal ideal m",
    "H_2: The sequence x_1, x_2, ..., x_n is a regular sequence in R",
    "H_3: The elements x_1, x_2, ..., x_n belong to the maximal ideal m",
    "¬Q: There exists a permutation of the sequence that is not a regular sequence in R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Evaluates the hypotheses and negated conclusion for the given witness.
    The witness can be a tuple of 4 booleans, or a dictionary/object with:
      - is_local_ring: bool or callable
      - seq: list or tuple
      - is_regular_sequence: bool or callable
      - in_maximal_ideal: bool or callable
      - is_permutability_false: bool or callable (optional, evaluated via permutations if absent)
    """
    # Support for a direct tuple witness: (is_local, is_reg, in_m, neg_q)
    if isinstance(witness, tuple) and len(witness) == 4:
        try:
            return [bool(x) for x in witness]
        except Exception:
            pass

    # H1: R is a local ring with maximal ideal m
    try:
        if isinstance(witness, dict):
            val = witness.get('is_local_ring', False)
        else:
            val = getattr(witness, 'is_local_ring', False)
        h1 = bool(val() if callable(val) else val)
    except Exception:
        h1 = False

    # H2: The sequence x_1, ..., x_n is a regular sequence in R
    try:
        if isinstance(witness, dict):
            val = witness.get('is_regular_sequence', False)
            seq = witness.get('seq', [])
        else:
            val = getattr(witness, 'is_regular_sequence', False)
            seq = getattr(witness, 'seq', [])
            
        if callable(val):
            try:
                h2 = bool(val(tuple(seq)))
            except Exception:
                h2 = bool(val(list(seq)))
        else:
            h2 = bool(val)
    except Exception:
        h2 = False

    # H3: The elements x_1, ..., x_n belong to the maximal ideal m
    try:
        if isinstance(witness, dict):
            val = witness.get('in_maximal_ideal', False)
            seq = witness.get('seq', [])
        else:
            val = getattr(witness, 'in_maximal_ideal', False)
            seq = getattr(witness, 'seq', [])
            
        if callable(val):
            try:
                h3 = bool(val(tuple(seq)))
            except Exception:
                h3 = bool(val(list(seq)))
        else:
            h3 = bool(val)
    except Exception:
        h3 = False

    # neg_Q: There exists a permutation of the sequence that is not a regular sequence
    try:
        if isinstance(witness, dict) and 'is_permutability_false' in witness:
            val = witness['is_permutability_false']
            neg_q = bool(val() if callable(val) else val)
        elif hasattr(witness, 'is_permutability_false'):
            val = witness.is_permutability_false
            neg_q = bool(val() if callable(val) else val)
        else:
            if isinstance(witness, dict):
                val = witness.get('is_regular_sequence', False)
                seq = witness.get('seq', [])
            else:
                val = getattr(witness, 'is_regular_sequence', False)
                seq = getattr(witness, 'seq', [])
                
            if callable(val):
                neg_q = False
                for p in itertools.permutations(seq):
                    try:
                        reg = bool(val(tuple(p)))
                    except Exception:
                        reg = bool(val(list(p)))
                    if not reg:
                        neg_q = True
                        break
            else:
                neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]