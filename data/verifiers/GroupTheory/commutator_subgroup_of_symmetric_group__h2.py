import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.combinatorics.permutations import Permutation

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

def conditions(witness) -> list[bool]:
    n = None
    S_n = None
    A_n_wit = None
    
    if isinstance(witness, dict):
        n = witness.get('n')
        S_n = witness.get('S_n', witness.get('Sn'))
        A_n_wit = witness.get('A_n', witness.get('An'))
    elif hasattr(witness, 'n'):
        n = getattr(witness, 'n')
        S_n = getattr(witness, 'S_n', getattr(witness, 'Sn', None))
        A_n_wit = getattr(witness, 'A_n', getattr(witness, 'An', None))
    elif isinstance(witness, (tuple, list)):
        if len(witness) >= 3:
            n = witness[0]
            S_n = witness[1]
            A_n_wit = witness[2]
        elif len(witness) == 2:
            n = witness[0]
            S_n = witness[1]
        elif len(witness) == 1:
            n = witness[0]
    else:
        n = witness

    try:
        n_val = int(n)
        h1 = (n_val >= 2 and n_val == n)
    except Exception:
        h1 = False

    A_n_obj = None
    try:
        if not h1:
            h2 = False
        else:
            An_true = AlternatingGroup(n_val)
            if A_n_wit is None:
                h2 = True
                A_n_obj = An_true
            else:
                A_n_obj = A_n_wit
                h2 = A_n_wit.is_subgroup(An_true) and A_n_wit.order() == An_true.order()
    except Exception:
        h2 = False

    if A_n_obj is None:
        try:
            A_n_obj = AlternatingGroup(n_val) if h1 else AlternatingGroup(2)
        except Exception:
            pass

    try:
        if not h1:
            neg_q = False
        else:
            if S_n is None:
                S_n_obj = SymmetricGroup(n_val)
            else:
                S_n_obj = S_n
                
            derived = S_n_obj.derived_subgroup()
            is_equal = derived.is_subgroup(A_n_obj) and derived.order() == A_n_obj.order()
            neg_q = not is_equal
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 2",
    "H_2: A_n is the alternating group of degree n",
    "¬Q: The commutator subgroup of S_n is not equal to A_n"
]

N_HYP = 2
NEG_Q_INDEX = 2