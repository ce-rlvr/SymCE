import math
from sympy.combinatorics import SymmetricGroup, PermutationGroup, Permutation
from sympy.combinatorics.named_groups import AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

# Top-level setup: named object bindings
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
    witness is expected to be a tuple: (n, k, X, Y, H)
    where:
      n: int (degree of the symmetric group S_n)
      k: int (size of subset Y)
      X: set or list (the superset)
      Y: set or list (the subset)
      H: PermutationGroup (the candidate stabilizer subgroup)
    """
    try:
        n, k, X, Y, H = witness
    except Exception:
        return [False, False, False]

    # H_1: Y is a subset of X of size k
    try:
        h1 = set(Y).issubset(set(X)) and len(set(Y)) == k
    except Exception:
        h1 = False

    # H_2: H is the setwise stabilizer of Y in S_n
    try:
        if not isinstance(H, PermutationGroup):
            h2 = False
        elif n > 7 or n < 1:
            # Restrict n to keep the verifier fast (7! = 5040 is very quick)
            h2 = False
        else:
            Sn = SymmetricGroup(n)
            stabilizer_elements = set()
            
            # Find all elements in S_n that stabilize Y setwise
            for p in Sn.generate():
                mapped_Y = set()
                for y in Y:
                    # Permutations in SymPy act on 0, ..., n-1
                    if isinstance(y, int) and 0 <= y < p.size:
                        mapped_Y.add(p(y))
                    else:
                        mapped_Y.add(y)
                
                if mapped_Y == set(Y):
                    stabilizer_elements.add(p)
            
            # Normalize elements of H to degree n for accurate comparison
            H_elements = set()
            for p in H.generate():
                arr = p.array_form
                if len(arr) < n:
                    arr = arr + list(range(len(arr), n))
                H_elements.add(Permutation(arr))
                
            h2 = (H_elements == stabilizer_elements)
    except Exception:
        h2 = False

    # neg_Q: H is NOT isomorphic to S_k \times S_{n-k}
    try:
        if k < 0 or n - k < 0:
            neg_q = True
        else:
            expected_order = math.factorial(k) * math.factorial(n - k)
            if H.order() != expected_order:
                neg_q = True
            else:
                # Construct the direct product S_k \times S_{n-k}
                gens = []
                if k > 1:
                    Sk = SymmetricGroup(k)
                    for g in Sk.generators:
                        arr = g.array_form + list(range(k, n))
                        gens.append(Permutation(arr))
                if n - k > 1:
                    Snk = SymmetricGroup(n - k)
                    for g in Snk.generators:
                        arr = list(range(k)) + [i + k for i in g.array_form]
                        gens.append(Permutation(arr))
                
                if not gens:
                    gens = [Permutation(n - 1)] if n > 0 else [Permutation(0)]
                
                DP = PermutationGroup(gens)
                
                try:
                    neg_q = not H.is_isomorphic(DP)
                except AttributeError:
                    # Fallback if is_isomorphic is unavailable, though orders matched
                    neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: Y is a subset of X of size k",
    "H_2: H is the setwise stabilizer of Y in S_n",
    "¬Q: H is not isomorphic to S_k \\times S_{n-k}"
]

N_HYP = 2
NEG_Q_INDEX = 2