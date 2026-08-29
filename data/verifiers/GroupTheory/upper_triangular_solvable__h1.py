import itertools
import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "H_2: G is the group of all invertible n by n upper triangular matrices with entries in F",
    "¬Q: The group G is not solvable"
]

N_HYP = 2
NEG_Q_INDEX = 2

def is_eq(a, b):
    try:
        return bool(a == b)
    except Exception:
        return False

def to_hashable(x):
    import sympy
    if isinstance(x, sympy.MatrixBase):
        return sympy.ImmutableMatrix(x)
    elif isinstance(x, (list, tuple)):
        return tuple(to_hashable(e) for e in x)
    return x

def to_matrix_tuple(m):
    import sympy
    if isinstance(m, sympy.MatrixBase):
        m = m.tolist()
    return tuple(tuple(to_hashable(e) for e in row) for row in m)

def get_zero_one(F_list):
    zero = None
    for z in F_list:
        if all(is_eq(z + x, x) for x in F_list):
            zero = z
            break
    one = None
    for e in F_list:
        if all(is_eq(e * x, x) and is_eq(x * e, x) for x in F_list):
            one = e
            break
    return zero, one

def mat_mul(A, B, zero, n):
    C = [[zero for _ in range(n)] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            s = zero
            for k in range(n):
                s = s + A[i][k] * B[k][j]
            C[i][j] = s
    return tuple(tuple(row) for row in C)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness.get('n')
            F = witness.get('F')
            G = witness.get('G')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 3:
                n, F, G = witness
            elif len(witness) == 2:
                n, F = witness
                G = None
            else:
                return [False, False, False]
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H1: n is a positive integer
    try:
        h1 = isinstance(n, int) and n > 0
    except Exception:
        h1 = False

    # H2: G is the group of all invertible n by n upper triangular matrices with entries in F
    try:
        F_list = [to_hashable(x) for x in F]
        if not F_list:
            h2 = False
        else:
            zero, one = get_zero_one(F_list)
            if zero is None or one is None:
                h2 = False
            else:
                inv_F = set()
                for x in F_list:
                    for y in F_list:
                        if is_eq(x * y, one) and is_eq(y * x, one):
                            inv_F.add(x)
                            break
                
                All_UT = []
                for elements in itertools.product(F_list, repeat=n*(n+1)//2):
                    idx = 0
                    mat = []
                    for i in range(n):
                        row = []
                        for j in range(n):
                            if i > j:
                                row.append(zero)
                            else:
                                row.append(elements[idx])
                                idx += 1
                        mat.append(tuple(row))
                    All_UT.append(tuple(mat))
                
                I_n = []
                for i in range(n):
                    row = []
                    for j in range(n):
                        row.append(one if i == j else zero)
                    I_n.append(tuple(row))
                I_n = tuple(I_n)
                
                Invertible_UT = set()
                for A in All_UT:
                    if all(A[i][i] in inv_F for i in range(n)):
                        Invertible_UT.add(A)
                
                if G is None:
                    G = list(Invertible_UT)
                    h2 = True
                else:
                    G_set = set(to_matrix_tuple(m) for m in G)
                    h2 = (G_set == Invertible_UT)
    except Exception:
        h2 = False

    # Conclusion: G is solvable
    try:
        if not h2:
            neg_q = False
        else:
            G_set = set(to_matrix_tuple(m) for m in G)
            current_G = G_set
            is_solv = True
            
            inv = {}
            for A in current_G:
                for B in current_G:
                    if is_eq(mat_mul(A, B, zero, n), I_n):
                        inv[A] = B
                        break
            
            while len(current_G) > 1:
                next_G_gens = set()
                for A in current_G:
                    for B in current_G:
                        AB = mat_mul(A, B, zero, n)
                        A_inv = inv[A]
                        B_inv = inv[B]
                        A_inv_B_inv = mat_mul(A_inv, B_inv, zero, n)
                        comm = mat_mul(AB, A_inv_B_inv, zero, n)
                        next_G_gens.add(comm)
                
                next_G = set(next_G_gens)
                added = True
                while added:
                    added = False
                    new_elements = set()
                    for X in next_G:
                        for Y in next_G_gens:
                            XY = mat_mul(X, Y, zero, n)
                            if XY not in next_G:
                                new_elements.add(XY)
                    if new_elements:
                        next_G.update(new_elements)
                        added = True
                
                if len(next_G) == len(current_G):
                    is_solv = False
                    break
                current_G = next_G
                
            neg_q = not is_solv
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]