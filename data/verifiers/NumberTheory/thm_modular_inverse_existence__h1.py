import math
import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

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
    "¬Q: The equivalence 'exists x such that ax ≡ 1 (mod m) iff gcd(a, m) = 1' fails"
]
N_HYP = 0
NEG_Q_INDEX = 0

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'a' in witness and 'm' in witness:
                a = int(witness['a'])
                m = int(witness['m'])
            elif 'm' in witness:
                m = int(witness['m'])
                a = 1
            else:
                return [False]
        elif isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                a = int(witness[0])
                m = int(witness[1])
            elif len(witness) == 1:
                m = int(witness[0])
                a = 1
            else:
                return [False]
        else:
            m = int(witness)
            a = 1
    except Exception:
        return [False]
        
    try:
        if m == 0:
            # Modulo 0 is undefined in standard programming and elementary number theory contexts,
            # meaning the congruence ax ≡ 1 (mod 0) has no valid solution.
            has_sol = False
        else:
            # For m != 0, Bezout's identity guarantees a solution exists iff gcd(a, m) == 1
            has_sol = (math.gcd(a, m) == 1)
            
        gcd_eq_1 = (math.gcd(a, m) == 1)
        
        conclusion = (has_sol == gcd_eq_1)
        neg_q = not conclusion
    except Exception:
        neg_q = False
        
    return [neg_q]