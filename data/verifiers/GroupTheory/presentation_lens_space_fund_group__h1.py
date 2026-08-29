import math
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

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (p, q) representing the parameters
    of the lens space L(p,q).
    """
    try:
        if not isinstance(witness, (tuple, list)):
            return [False, False, False]
        if len(witness) != 2:
            return [False, False, False]
        
        p, q = witness
        
        # Ensure p and q are integers
        try:
            p_int = int(p)
            q_int = int(q)
            if p_int != p or q_int != q:
                return [False, False, False]
            p, q = p_int, q_int
        except (ValueError, TypeError):
            return [False, False, False]
            
        # H_1: Let L(p,q) be the lens space of type (p,q).
        # For the quotient space S^3 / Z_p to be defined via the standard action,
        # we require p != 0. (The dropped hypothesis is that p and q are coprime).
        h1 = (p != 0)
        
        # H_2: Let G = \pi_1(L(p,q)) be the fundamental group of L(p,q).
        # This is a definitional hypothesis, so it holds whenever L(p,q) is defined.
        h2 = h1
        
        # ¬Q: G does not admit the presentation <x | x^p = 1>, and is not isomorphic to Z/pZ.
        # The fundamental group of the quotient S^3 / Z_p with weights (1, q) is Z_{|p|/d},
        # where d = gcd(p, q). This group is isomorphic to Z_{|p|} if and only if d == 1.
        # Thus, the conclusion fails (¬Q is True) if and only if d > 1.
        if p == 0:
            neg_q = False
        else:
            d = math.gcd(p, q)
            neg_q = (d > 1)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: L(p,q) is the lens space of type (p,q)",
    "H_2: G is the fundamental group of L(p,q)",
    "¬Q: G does not admit the presentation <x | x^p = 1> or is not isomorphic to Z/pZ"
]

N_HYP = 2
NEG_Q_INDEX = 2