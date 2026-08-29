import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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

def conditions(witness):
    """
    Given a witness (G, N, x, y), checks whether it is a valid counterexample
    to the false conjecture.
    """
    try:
        G, N, x, y = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: G is a group and x, y are elements of G
    try:
        h1 = (isinstance(G, PermutationGroup) and 
              isinstance(x, Permutation) and 
              isinstance(y, Permutation) and 
              x in G and y in G)
    except Exception:
        h1 = False
        
    # H_2: N is a normal subgroup of G
    try:
        h2 = False
        if h1:
            h2 = N.is_subgroup(G) and G.is_normal(N)
    except Exception:
        h2 = False
        
    # H_3: xN and yN are conjugate in G/N
    # This means there exists g in G such that g * x * g^-1 * N == y * N
    # Equivalently, y^-1 * g * x * g^-1 is in N
    try:
        h3 = False
        if h1 and h2:
            y_inv = ~y
            for g in G.elements:
                conj = g * x * (~g)
                if (y_inv * conj) in N:
                    h3 = True
                    break
    except Exception:
        h3 = False
        
    # ¬Q: For all n in N, x is NOT conjugate to y^n in G
    # (Note: 'yn' in the prompt refers to the conjugate y^n = n^-1 * y * n)
    try:
        neg_Q = False
        if h1 and h2:
            all_not_conjugate = True
            for n in N.elements:
                yn = (~n) * y * n
                
                # Check if x is conjugate to yn in G
                is_conj = False
                for g in G.elements:
                    if g * x * (~g) == yn:
                        is_conj = True
                        break
                
                if is_conj:
                    all_not_conjugate = False
                    break
                    
            neg_Q = all_not_conjugate
    except Exception:
        neg_Q = False
        
    return [h1, h2, h3, neg_Q]

CONDITION_LABELS = [
    "H_1: G is a group and x, y are elements of G",
    "H_2: N is a normal subgroup of G",
    "H_3: xN and yN are conjugate in G/N",
    "¬Q: For all n in N, x is not conjugate to y^n in G"
]

N_HYP = 3
NEG_Q_INDEX = 3