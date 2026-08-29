import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

def get_bool_attr(obj, *names):
    for name in names:
        if hasattr(obj, name):
            try:
                val = getattr(obj, name)
                if callable(val):
                    return bool(val())
                return bool(val)
            except Exception:
                pass
    raise AttributeError

def conditions(witness) -> list[bool]:
    # H_1: R is a commutative Artinian ring
    h1_ok = False
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            R = witness[0]
        elif hasattr(witness, 'R'):
            R = witness.R
        elif hasattr(witness, 'ring'):
            R = witness.ring
        else:
            R = witness

        if isinstance(R, dict):
            comm = R.get('is_commutative', False)
            art = R.get('is_artinian', False)
            h1_ok = bool(comm and art)
        else:
            try:
                comm = get_bool_attr(R, 'is_commutative')
                art = get_bool_attr(R, 'is_artinian')
                h1_ok = comm and art
            except AttributeError:
                try:
                    h1_ok = get_bool_attr(R, 'is_commutative_artinian', 'is_commutative_artinian_ring')
                except AttributeError:
                    h1_ok = False
    except Exception:
        h1_ok = False

    # ¬Q: I cannot be written as a finite product of primary ideals
    neg_q_ok = False
    try:
        if isinstance(witness, tuple) and len(witness) == 2:
            I = witness[1]
        elif hasattr(witness, 'I'):
            I = witness.I
        else:
            I = witness

        if isinstance(I, dict):
            if 'is_finite_product_of_primary_ideals' in I:
                prod = I['is_finite_product_of_primary_ideals']
            elif 'is_product_of_primary_ideals' in I:
                prod = I['is_product_of_primary_ideals']
            else:
                prod = True
            neg_q_ok = not bool(prod)
        else:
            try:
                prod = get_bool_attr(I, 'is_finite_product_of_primary_ideals', 
                                     'is_product_of_primary_ideals', 
                                     'can_be_written_as_finite_product_of_primary_ideals')
                neg_q_ok = not prod
            except AttributeError:
                neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a commutative Artinian ring",
    "¬Q: I cannot be written as a finite product of primary ideals"
]

N_HYP = 1
NEG_Q_INDEX = 1