import math
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

CONDITION_LABELS = [
    "H_1: B is a cyclic group of finite order n",
    "¬Q: The tensor product of A and B over the integers is NOT isomorphic to the cyclic group of order gcd(m,n)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def _lcm(a, b):
    if a == 0 and b == 0:
        return 0
    return abs(a * b) // math.gcd(a, b)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) >= 2:
            A, B = witness[0], witness[1]
        else:
            return [False, False]
    except Exception:
        return [False, False]
        
    # H_1: B is a cyclic group of finite order n
    try:
        h1 = False
        if getattr(B, 'is_abelian', False):
            invB = [int(x) for x in B.abelian_invariants()]
            expB = 1
            for x in invB:
                expB = _lcm(expB, x)
            orderB = int(B.order())
            if expB == orderB and orderB > 0:
                h1 = True
    except Exception:
        h1 = False

    # neg_Q: A tensor B is not isomorphic to Z_gcd(m,n)
    try:
        m = int(A.order())
        n = int(B.order())
        if m <= 0 or n <= 0:
            neg_q = False
        else:
            K = math.gcd(m, n)
            invA = [int(x) for x in A.abelian_invariants()]
            invB = [int(x) for x in B.abelian_invariants()]
            
            tensor_invs = [math.gcd(a, b) for a in invA for b in invB]
            tensor_order = 1
            for x in tensor_invs:
                tensor_order *= x
            tensor_exponent = 1
            for x in tensor_invs:
                tensor_exponent = _lcm(tensor_exponent, x)
                
            is_iso = (tensor_order == K) and (tensor_exponent == K)
            neg_q = not is_iso
    except Exception:
        neg_q = False

    return [h1, neg_q]