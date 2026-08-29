import sympy
from sympy import Matrix
import itertools

class RingElement:
    def __init__(self, mat, mod=2):
        self.mat = mat
        self.mod = mod
        
    def __add__(self, other):
        return RingElement((self.mat + other.mat).applyfunc(lambda x: x % self.mod), self.mod)
        
    def __mul__(self, other):
        return RingElement((self.mat * other.mat).applyfunc(lambda x: x % self.mod), self.mod)
        
    def __eq__(self, other):
        if not isinstance(other, RingElement): 
            return False
        return self.mat == other.mat
        
    def __hash__(self):
        return hash(tuple(self.mat))
        
    def __repr__(self):
        return f"RingElement({self.mat.tolist()})"

# Top-level setup: Define standard non-commutative rings over Z2
# UT2_Z2: Upper triangular 2x2 matrices over Z2
UT2_Z2 = []
for a, b, c in itertools.product([0, 1], repeat=3):
    UT2_Z2.append(RingElement(Matrix(2, 2, [a, b, 0, c]), 2))

# M2_Z2: All 2x2 matrices over Z2
M2_Z2 = []
for entries in itertools.product([0, 1], repeat=4):
    M2_Z2.append(RingElement(Matrix(2, 2, entries), 2))

def conditions(witness) -> list[bool]:
    try:
        # Parse witness
        if len(witness) == 3:
            R = UT2_Z2
            I, J, K = witness
        elif len(witness) == 4:
            R, I, J, K = witness
        else:
            return [False, False]

        def contains(lst, item):
            for x in lst:
                if x == item: return True
            return False

        def is_subset(sub, sup):
            for x in sub:
                if not contains(sup, x): return False
            return True

        if not R: 
            return [False, False]

        # Hypothesis 1: I, J, and K are ideals of R
        def is_ideal(S):
            if not S: return False
            if not is_subset(S, R): return False
            # Closed under addition
            for x in S:
                for y in S:
                    if not contains(S, x + y): return False
            # Closed under left and right multiplication by R
            for s in S:
                for r in R:
                    if not contains(S, r * s): return False
                    if not contains(S, s * r): return False
            return True

        h1 = is_ideal(I) and is_ideal(J) and is_ideal(K)

        # Compute the two-sided ideal quotient (K : J)
        # (K : J) = { r in R | rJ <= K and Jr <= K }
        K_colon_J = []
        for r in R:
            is_in = True
            for j in J:
                if not contains(K, r * j):
                    is_in = False
                    break
                if not contains(K, j * r):
                    is_in = False
                    break
            if is_in:
                K_colon_J.append(r)

        I_sub_K_colon_J = is_subset(I, K_colon_J)

        # Compute the product ideal IJ
        # First, get the generators { i * j | i in I, j in J }
        IJ = []
        for i in I:
            for j in J:
                prod = i * j
                if not contains(IJ, prod):
                    IJ.append(prod)

        # Additive closure of the generators
        changed = True
        iters = 0
        while changed and iters < 100:
            changed = False
            iters += 1
            new_els = []
            for x in IJ:
                for y in IJ:
                    s = x + y
                    if not contains(IJ, s) and not contains(new_els, s):
                        new_els.append(s)
            if new_els:
                IJ.extend(new_els)
                changed = True

        IJ_sub_K = is_subset(IJ, K)

        # Conclusion: I <= (K : J) if and only if IJ <= K
        q = (I_sub_K_colon_J == IJ_sub_K)
        neg_q = not q

        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I, J, and K are ideals of R",
    "¬Q: I ⊆ (K : J) if and only if IJ ⊆ K fails"
]
N_HYP = 1
NEG_Q_INDEX = 1