import sympy
from sympy import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def conditions(witness) -> list[bool]:
    try:
        # We evaluate the witness in the context of R = ZZ.
        # The witness should provide a multiplicatively closed subset S of ZZ
        # and an integer P representing the ideal P*ZZ.
        if isinstance(witness, dict):
            S = witness.get('S', [])
            P = witness.get('P', 0)
        else:
            S, P = witness
            
        S = list(S)
        if isinstance(P, (list, tuple, set)):
            if len(P) == 1:
                P = list(P)[0]
            else:
                return [False, False, False]
        P = int(P)
        
        # H1: R is a commutative ring with identity
        # Since we fix R = ZZ for the evaluation, this is always True.
        h1 = True
        
        # H2: S is a multiplicatively closed subset of R
        if not S:
            h2 = False
        else:
            h2 = all((a * b) in S for a in S for b in S) and (1 in S)
            
        # Conclusion: S^-1 P is a prime ideal in S^-1 R
        if 0 in S:
            # If 0 is in S, the localized ring S^-1 R is the zero ring.
            # The zero ring has no prime ideals (prime ideals must be proper).
            is_prime = False
        else:
            # For R = ZZ, if S is finite and multiplicatively closed and 0 not in S,
            # S must be a subset of {1, -1}.
            # Thus S^-1 R is isomorphic to ZZ.
            # S^-1 P is isomorphic to P*ZZ.
            # P*ZZ is a prime ideal iff |P| is a prime number or P == 0.
            is_prime = sympy.isprime(abs(P)) or P == 0
            
        neg_q = not is_prime
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: S is a multiplicatively closed subset of R",
    "¬Q: The extended ideal S^{-1}P is not a prime ideal in S^{-1}R"
]

N_HYP = 2
NEG_Q_INDEX = 2