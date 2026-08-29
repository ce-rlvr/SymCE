import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros

# Standard group theory objects that might be referenced in a witness expression
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
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
    try:
        if isinstance(witness, dict):
            p = int(witness['p'])
            q = int(witness['q'])
        elif hasattr(witness, 'p') and hasattr(witness, 'q'):
            p = int(witness.p)
            q = int(witness.q)
        else:
            p, q = witness
            p = int(p)
            q = int(q)
    except Exception:
        return [False, False]
        
    try:
        h1 = sympy.isprime(p) and sympy.isprime(q) and p != q
    except Exception:
        h1 = False
        
    try:
        # A semidirect product of C_p by C_q is determined by a homomorphism C_q -> Aut(C_p).
        # Since Aut(C_p) is cyclic of order p-1, there is a non-trivial homomorphism 
        # (and thus a non-abelian semidirect product) if and only if q divides p-1.
        # If q divides p-1, all non-trivial homomorphisms yield isomorphic semidirect products,
        # so there is exactly 1 non-abelian semidirect product up to isomorphism.
        # If q does not divide p-1, there are 0 non-abelian semidirect products.
        # The conclusion states there is EXACTLY ONE.
        # Therefore, the conclusion fails (neg_Q is True) if and only if q does not divide p-1.
        neg_q = ((p - 1) % q != 0)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: p and q are distinct prime numbers",
    "¬Q: There is not exactly one non-abelian semidirect product of C_p by C_q (there are 0)"
]

N_HYP = 1
NEG_Q_INDEX = 1