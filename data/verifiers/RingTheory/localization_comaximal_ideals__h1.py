import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    The conjecture is true for all commutative rings, so a valid counterexample must be 
    a non-commutative ring. Since SymPy does not natively support non-commutative 
    localization at prime ideals, the witness is expected to be a custom object or 
    a dictionary providing the necessary properties.
    """
    h1, h2, neg_q = False, False, False

    # Case 1: Witness is a dictionary
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('h1', witness.get('is_comaximal', False)))
            h2 = bool(witness.get('h2', witness.get('is_prime_ideal', False)))
            neg_q = bool(witness.get('neg_q', witness.get('conclusion_fails', False)))
            return [h1, h2, neg_q]
        except Exception:
            pass

    # Case 2: Witness is a tuple (R, I, J, P) representing the ring and ideals
    if isinstance(witness, tuple) and len(witness) == 4:
        R, I, J, P = witness
        try:
            h1 = bool(R.is_comaximal(I, J))
        except Exception:
            pass
        try:
            h2 = bool(R.is_prime_ideal(P))
        except Exception:
            pass
        try:
            I_P = R.localize(I, P)
            J_P = R.localize(J, P)
            R_P = R.localize(R, P)
            q = R.is_equal(I_P, R_P) or R.is_equal(J_P, R_P)
            neg_q = not q
        except Exception:
            pass
        if h1 or h2 or neg_q:
            return [h1, h2, neg_q]

    # Case 3: Witness is a tuple (I, J, P) representing the ideals
    if isinstance(witness, tuple) and len(witness) == 3:
        I, J, P = witness
        try:
            h1 = bool(I.is_comaximal(J))
        except Exception:
            pass
        try:
            h2 = bool(P.is_prime_ideal())
        except Exception:
            pass
        try:
            I_P = I.localize(P)
            J_P = J.localize(P)
            R_P = I.ring.localize(P)
            q = I_P.is_equal(R_P) or J_P.is_equal(R_P)
            neg_q = not q
        except Exception:
            pass
        if h1 or h2 or neg_q:
            return [h1, h2, neg_q]

    # Case 4: Witness is a custom object with properties/methods
    try:
        if hasattr(witness, 'is_comaximal'):
            h1 = bool(witness.is_comaximal())
        else:
            h1 = bool(getattr(witness, 'h1', False))
    except Exception:
        pass

    try:
        if hasattr(witness, 'is_prime_ideal'):
            h2 = bool(witness.is_prime_ideal())
        else:
            h2 = bool(getattr(witness, 'h2', False))
    except Exception:
        pass

    try:
        if hasattr(witness, 'conclusion_fails'):
            neg_q = bool(witness.conclusion_fails())
        elif hasattr(witness, 'conclusion_holds'):
            neg_q = not bool(witness.conclusion_holds())
        else:
            neg_q = bool(getattr(witness, 'neg_q', False))
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: I and J are comaximal ideals of R",
    "H_2: P is a prime ideal of R",
    "¬Q: In the localization R_P, neither I_P nor J_P is equal to R_P"
]

N_HYP = 2
NEG_Q_INDEX = 2