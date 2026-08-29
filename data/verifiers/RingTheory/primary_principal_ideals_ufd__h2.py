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

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "In a UFD R, (a) is a primary ideal if and only if a is associate to p^n 
    for some prime element p in R and some integer n >= 1."
    
    The dropped hypothesis from the true theorem is that a != 0.
    In any UFD, (0) is a prime (and thus primary) ideal, but 0 is not 
    associate to any prime power p^n. Thus a = 0 is a counterexample.
    We evaluate the witness in the UFD R = Z.
    """
    try:
        # H_1: R is a UFD. We fix R = Z and check if the witness is an element of Z.
        if isinstance(witness, bool):
            H1 = False
        elif witness == 0:
            H1 = True
        elif isinstance(witness, (int, sympy.Integer)):
            H1 = True
        else:
            H1 = False
    except Exception:
        H1 = False

    try:
        if not H1:
            neg_Q = False
        else:
            if witness == 0:
                # In Z, (0) is a primary ideal.
                left = True
                # 0 is not associate to p^n for any prime p.
                right = False
            else:
                a = abs(int(witness))
                if a == 1:
                    # (1) = Z is not a proper ideal, so not primary.
                    left = False
                    # 1 is not a prime power.
                    right = False
                else:
                    # For a > 1 in Z, (a) is primary iff a = p^n.
                    f = sympy.factorint(a)
                    left = (len(f) == 1)
                    # a is associate to p^n iff |a| = p^n.
                    right = (len(f) == 1)
            
            # neg_Q is True when the conclusion FAILS (i.e., left != right)
            neg_Q = (left != right)
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a unique factorization domain (witness in Z)",
    "¬Q: (a) is primary iff a is associate to p^n FAILS"
]

N_HYP = 1
NEG_Q_INDEX = 1