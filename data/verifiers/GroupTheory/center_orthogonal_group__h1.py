import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import Matrix, isprime, eye, zeros
from itertools import product

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
    Checks if the witness is a valid counterexample to the conjecture.
    The witness is expected to be a tuple (n, q) where n is the dimension
    and q is the order of a prime field F_q.
    """
    try:
        n, q = witness
    except Exception:
        return [False, False, False]
    
    # H_1: n >= 1
    try:
        h1 = isinstance(n, int) and n >= 1
    except Exception:
        h1 = False
        
    # H_2: G is the orthogonal group O(n, F)
    # We interpret q as the prime order of a finite field F_q
    try:
        h2 = isprime(q)
    except Exception:
        h2 = False
        
    # ¬Q: The center of G does not consist exactly of I and -I
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # To prevent timeouts, limit the size of n and q for the verifier
            if n > 4 or q > 11 or (n == 4 and q > 3) or (n == 3 and q > 5):
                neg_q = False
            else:
                # Generate all vectors in F_q^n
                vectors = [Matrix(n, 1, v) for v in product(range(q), repeat=n)]
                
                results = []
                # Backtracking to find all orthogonal matrices (columns are orthonormal)
                def backtrack(cols):
                    if len(cols) == n:
                        results.append(Matrix.hstack(*cols))
                        return
                    
                    i = len(cols)
                    for v in vectors:
                        # Check if v^T * v == 1
                        if (v.T * v)[0,0] % q != 1:
                            continue
                        ok = True
                        # Check if v is orthogonal to all previously selected columns
                        for j in range(i):
                            if (v.T * cols[j])[0,0] % q != 0:
                                ok = False
                                break
                        if ok:
                            backtrack(cols + [v])
                
                backtrack([])
                group = results
                
                # Find the center of the group
                center = []
                for g in group:
                    is_central = True
                    for h in group:
                        gh = (g * h).applyfunc(lambda x: x % q)
                        hg = (h * g).applyfunc(lambda x: x % q)
                        if gh != hg:
                            is_central = False
                            break
                    if is_central:
                        center.append(g)
                
                # Construct the expected center: {I, -I}
                I = eye(n).applyfunc(lambda x: x % q)
                minus_I = (-eye(n)).applyfunc(lambda x: x % q)
                expected_center = []
                for M in [I, minus_I]:
                    if M not in expected_center:
                        expected_center.append(M)
                
                # Check if the actual center is exactly the expected center
                if len(center) != len(expected_center):
                    neg_q = True
                else:
                    same = True
                    for c in center:
                        if c not in expected_center:
                            same = False
                            break
                    neg_q = not same
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: n >= 1",
    "H_2: G is the orthogonal group O(n, F)",
    "¬Q: The center of G does not consist exactly of I and -I"
]

N_HYP = 2
NEG_Q_INDEX = 2