import itertools
from sympy import ImmutableMatrix, eye, zeros
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

CONDITION_LABELS = [
    "H_1: n is an integer such that n >= 3",
    "H_2: G is the group of n x n upper unitriangular matrices over F",
    "¬Q: The center Z(G) does not consist exactly of those matrices in G whose non-diagonal entries are zero except possibly the entry in the first row and n-th column"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if len(witness) == 3:
            n = witness[0]
            # Try to identify G and F based on their structure
            if isinstance(witness[1], (list, tuple, set)) and len(witness[1]) > 0 and hasattr(list(witness[1])[0], 'shape') and list(witness[1])[0].shape == (n, n):
                G, F = witness[1], witness[2]
            elif isinstance(witness[2], (list, tuple, set)) and len(witness[2]) > 0 and hasattr(list(witness[2])[0], 'shape') and list(witness[2])[0].shape == (n, n):
                F, G = witness[1], witness[2]
            else:
                n, F, G = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
    
    # H_1: n is an integer such that n >= 3
    try:
        h1 = isinstance(n, int) and n >= 3
    except Exception:
        h1 = False
        
    # H_2: G is the group of n x n upper unitriangular matrices over F
    try:
        h2 = False
        F_list = list(F)
        if F_list and G:
            # Find the additive identity (zero) in F
            zero = None
            for x in F_list:
                is_zero = True
                for y in F_list:
                    if not (x + y == y):
                        is_zero = False
                        break
                if is_zero:
                    zero = x
                    break
            
            if zero is not None:
                G_immut = [ImmutableMatrix(m) for m in G]
                one = G_immut[0][0, 0]
                
                positions = [(i, j) for i in range(n) for j in range(i+1, n)]
                
                # Check if G has exactly the right number of matrices
                if len(G_immut) == len(F_list)**len(positions):
                    h2 = True
                    for A in G_immut:
                        # Check diagonal entries
                        for i in range(n):
                            if not (A[i, i] == one):
                                h2 = False
                                break
                        if not h2: break
                        
                        # Check strictly lower triangular entries
                        for i in range(n):
                            for j in range(i):
                                if not (A[i, j] == zero):
                                    h2 = False
                                    break
                            if not h2: break
                        if not h2: break
                        
                        # Check strictly upper triangular entries
                        for i, j in positions:
                            found = False
                            for x in F_list:
                                if A[i, j] == x:
                                    found = True
                                    break
                            if not found:
                                h2 = False
                                break
                        if not h2: break
                    
                    # Ensure all matrices in G are distinct
                    if h2:
                        if len(set(G_immut)) != len(G_immut):
                            h2 = False
    except Exception:
        h2 = False
        
    # ¬Q: The center Z(G) does not consist exactly of the expected matrices
    try:
        neg_q = False
        if h2:
            # Compute the actual center Z(G)
            Z_G = []
            for A in G_immut:
                is_center = True
                for B in G_immut:
                    if not (A * B == B * A):
                        is_center = False
                        break
                if is_center:
                    Z_G.append(A)
            
            # Compute the expected center based on the conclusion
            expected_Z = []
            for A in G_immut:
                is_expected = True
                for i in range(n):
                    for j in range(n):
                        if i != j and (i, j) != (0, n-1):
                            if not (A[i, j] == zero):
                                is_expected = False
                                break
                    if not is_expected:
                        break
                if is_expected:
                    expected_Z.append(A)
            
            # The conclusion fails if the actual center is not exactly the expected center
            neg_q = set(Z_G) != set(expected_Z)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]