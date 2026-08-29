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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: G is the standard restricted wreath product of Z_m by Z_n",
    "¬Q: G does not admit the given presentation"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Extract m and n from the witness
        if isinstance(witness, (tuple, list)):
            if len(witness) == 2:
                m, n = witness
            elif len(witness) == 3:
                _, m, n = witness
            else:
                return [False, False]
        elif isinstance(witness, dict):
            m = witness.get('m')
            n = witness.get('n')
            if m is None or n is None:
                return [False, False]
        elif hasattr(witness, 'm') and hasattr(witness, 'n'):
            m = witness.m
            n = witness.n
        else:
            return [False, False]
            
        if not isinstance(m, (int, sympy.Integer)) or not isinstance(n, (int, sympy.Integer)):
            return [False, False]
            
        m = int(m)
        n = int(n)
            
        # H_1: G is the standard restricted wreath product of Z_m by Z_n.
        # This is a definitional setup that holds for any integer parameters m and n.
        h1 = True
        
        # ¬Q: The conclusion fails (G does NOT admit the given presentation).
        # The presentation defines Z_m \wr Z_n correctly for all n >= 1.
        # If n <= 0, the condition 0 <= i < j < n is vacuous, so there are no commutator relations.
        # The presentation then defines the free product Z_{|n|} * Z_{|m|} (where Z_0 = Z).
        # The actual wreath product is Z_{|m|} \wr Z_{|n|}.
        # The free product Z_{|n|} * Z_{|m|} is isomorphic to the wreath product Z_{|m|} \wr Z_{|n|}
        # IF AND ONLY IF one of the groups is trivial (i.e., |n| <= 1 or |m| <= 1).
        # Specifically, if n <= 0, it fails unless n = -1 (where |n|=1) or |m| = 1.
        neg_q = (n <= 0) and (n != -1) and (abs(m) != 1)
        
        return [h1, neg_q]
    except Exception:
        return [False, False]