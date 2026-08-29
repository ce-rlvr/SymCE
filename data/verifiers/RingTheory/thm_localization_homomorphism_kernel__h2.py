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
    """
    Checks if the given witness is a valid counterexample.
    The witness is expected to be a tuple (n, S) representing the ring R = Z/nZ
    and a subset S of R.
    """
    try:
        if hasattr(witness, 'n') and hasattr(witness, 'S'):
            n_val = witness.n
            S_val = witness.S
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            n_val, S_val = witness
        else:
            return [False, False, False]
            
        n = int(n_val)
        S = [int(x) % n for x in S_val]
        
        # H_1: R is a commutative ring
        h1 = (n >= 1)
        
        # H_2: f: R -> S^{-1}R is the natural ring homomorphism defined by f(r) = r/1
        # This is true by definition of the setup.
        h2 = True
        
        # Compute the multiplicative closure of S modulo n (which is \bar{S})
        S_bar = {1 % n}
        queue = [1 % n]
        while queue:
            curr = queue.pop(0)
            for s in S:
                nxt = (curr * s) % n
                if nxt not in S_bar:
                    S_bar.add(nxt)
                    queue.append(nxt)
                    
        # K_prime is the set {r \in R | sr = 0 for some s \in S}
        K_prime = set()
        for r in range(n):
            for s in S:
                if (s * r) % n == 0:
                    K_prime.add(r)
                    break
                    
        # K is the actual kernel of f: R -> S^{-1}R
        # K = {r \in R | tr = 0 for some t \in \bar{S}}
        K = set()
        for r in range(n):
            for t in S_bar:
                if (t * r) % n == 0:
                    K.add(r)
                    break
                    
        # neg_Q: The kernel of f is NOT {r \in R | sr = 0 for some s \in S}
        neg_q = (K != K_prime)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: f: R -> S^{-1}R is the natural ring homomorphism defined by f(r) = r/1",
    "¬Q: The kernel of f is not {r in R | sr = 0 for some s in S}"
]

N_HYP = 2
NEG_Q_INDEX = 2