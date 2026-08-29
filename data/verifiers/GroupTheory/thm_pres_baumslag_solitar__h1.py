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

CONDITION_LABELS = [
    "H_1: G is defined as the HNN extension of Z relative to mZ and nZ (mZ and nZ are isomorphic)",
    "¬Q: G does not admit the presentation < a, t | t a^m t^-1 = a^n >"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
        else:
            m, n = witness
            
        if not (isinstance(m, int) and isinstance(n, int)):
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: G is defined as the HNN extension of Z relative to mZ and nZ.
    # For the HNN extension to exist, the associated subgroups mZ and nZ must be isomorphic.
    # This is true if and only if both are trivial (m=0, n=0) or both are infinite (m!=0, n!=0).
    try:
        h1_ok = ((m == 0) == (n == 0))
    except Exception:
        h1_ok = False
        
    # neg_Q: G does NOT admit the presentation < a, t | t a^m t^-1 = a^n >.
    # The HNN extension of Z relative to the subgroups mZ and nZ (with the canonical 
    # isomorphism mapping the positive generator of mZ to the positive generator of nZ) 
    # yields the group BS(|m|, |n|). 
    # The conclusion claims it admits the presentation of BS(m, n).
    # BS(|m|, |n|) is isomorphic to BS(m, n) if and only if 
    # (|m|, |n|) is in {(m, n), (n, m), (-m, -n), (-n, -m)}.
    # If they are not isomorphic, the conclusion fails and neg_Q is True.
    try:
        abs_m, abs_n = abs(m), abs(n)
        isomorphic = (abs_m, abs_n) in [(m, n), (n, m), (-m, -n), (-n, -m)]
        neg_q_ok = not isomorphic
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, neg_q_ok]