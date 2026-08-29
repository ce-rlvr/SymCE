import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Standard group theory objects
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

# Standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: B is a free abelian group of rank m",
    "¬Q: A \\otimes_\\mathbb{Z} B is not a free abelian group of rank nm"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    """
    Checks the remaining hypotheses and the negated conclusion.
    The witness should be a dictionary with keys 'A', 'B', 'n', 'm'.
    'A' and 'B' can be lists of integers representing the orders of cyclic factors
    of the abelian groups (where 0 represents Z), or sympy abelian PermutationGroups.
    """
    try:
        A_raw = witness['A']
        B_raw = witness['B']
        n = int(witness['n'])
        m = int(witness['m'])
        
        def get_invariants(G):
            if isinstance(G, (list, tuple)):
                return [int(x) for x in G]
            if hasattr(G, 'is_abelian') and G.is_abelian:
                if hasattr(G, 'abelian_invariants'):
                    return [int(x) for x in G.abelian_invariants()]
            raise ValueError("Not a valid abelian group representation")
            
        A = get_invariants(A_raw)
        B = get_invariants(B_raw)
        
        # Filter out trivial factors (Z_1)
        B_filtered = [x for x in B if abs(x) != 1]
        
        # H_1: B is a free abelian group of rank m
        # This means all non-trivial factors are Z (represented by 0) and there are exactly m of them.
        h1 = (len(B_filtered) == m) and all(x == 0 for x in B_filtered)
        
        # Conclusion: A \otimes B is a free abelian group of rank nm
        # The tensor product of Z_a and Z_b is Z_gcd(a,b).
        T = [math.gcd(a, b) for a in A for b in B]
        T_filtered = [x for x in T if abs(x) != 1]
        
        q = (len(T_filtered) == n * m) and all(x == 0 for x in T_filtered)
        
        neg_q = not q
        
        return [h1, neg_q]
    except Exception:
        return [False, False]