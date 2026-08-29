import sympy
from sympy import Matrix, eye, zeros, isprime
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

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
        # witness is expected to be a tuple: (p, G, B_0)
        # where p is a prime (defining the field GF(p)),
        # G is a list of matrices representing the group of linear transformations,
        # and B_0 is the matrix of the bilinear form.
        p, G, B_0 = witness
    except Exception:
        return [False, False, False]
        
    # H1: V is a finite-dimensional vector space over a field F
    # We verify this by checking that p is prime, B_0 is a square matrix,
    # and G is a valid group of invertible matrices of the same dimension over GF(p).
    try:
        h1 = False
        if isprime(p) and isinstance(B_0, Matrix) and B_0.shape[0] == B_0.shape[1]:
            n = B_0.shape[0]
            if n > 0 and isinstance(G, list):
                all_inv = True
                for M in G:
                    if not isinstance(M, Matrix) or M.shape != (n, n):
                        all_inv = False
                        break
                    if M.det() % p == 0:
                        all_inv = False
                        break
                if all_inv:
                    # Check if G is a group under matrix multiplication mod p
                    G_set = set(tuple(M[i, j] % p for i in range(n) for j in range(n)) for M in G)
                    is_group = True
                    I_elem = tuple(1 if i == j else 0 for i in range(n) for j in range(n))
                    if I_elem not in G_set:
                        is_group = False
                    else:
                        for M1 in G:
                            for M2 in G:
                                M3 = M1 * M2
                                elem3 = tuple(M3[i, j] % p for i in range(n) for j in range(n))
                                if elem3 not in G_set:
                                    is_group = False
                                    break
                            if not is_group:
                                break
                    if is_group:
                        h1 = True
    except Exception:
        h1 = False

    # H2: B_0 is a non-degenerate symmetric bilinear form on V
    try:
        h2 = False
        if h1:
            n = B_0.shape[0]
            is_sym = True
            for i in range(n):
                for j in range(n):
                    if (B_0[i, j] - B_0[j, i]) % p != 0:
                        is_sym = False
                        break
            is_nondeg = (B_0.det() % p != 0)
            h2 = is_sym and is_nondeg
    except Exception:
        h2 = False

    # neg_Q: The stabilizer of B_0 in G is NOT exactly the orthogonal group O(V, B_0)
    try:
        neg_q = False
        if h1 and h2:
            n = B_0.shape[0]
            
            # Find O(V, B_0) over GF(p)
            elements = itertools.product(range(p), repeat=n*n)
            O_V_B0 = set()
            for elem in elements:
                M = Matrix(n, n, elem)
                if M.det() % p != 0:
                    LHS = (M.T * B_0 * M)
                    is_ortho = True
                    for i in range(n):
                        for j in range(n):
                            if (LHS[i, j] - B_0[i, j]) % p != 0:
                                is_ortho = False
                                break
                        if not is_ortho:
                            break
                    if is_ortho:
                        O_V_B0.add(tuple(elem))
            
            # Find Stab_G(B_0)
            Stab_G_B0 = set()
            for M in G:
                LHS = (M.T * B_0 * M)
                is_stab = True
                for i in range(n):
                    for j in range(n):
                        if (LHS[i, j] - B_0[i, j]) % p != 0:
                            is_stab = False
                            break
                    if not is_stab:
                        break
                if is_stab:
                    elem = tuple(M[i, j] % p for i in range(n) for j in range(n))
                    Stab_G_B0.add(elem)
            
            neg_q = (Stab_G_B0 != O_V_B0)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F and G is a group of linear transformations",
    "H_2: B_0 is a non-degenerate symmetric bilinear form on V",
    "¬Q: The stabilizer of B_0 in G is not exactly the orthogonal group O(V, B_0)"
]

N_HYP = 2
NEG_Q_INDEX = 2