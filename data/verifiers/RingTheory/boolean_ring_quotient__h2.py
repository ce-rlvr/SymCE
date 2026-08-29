import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

# Standard Boolean rings for witness construction
# Witness format expected: (n, add_table, mul_table, I_list)
# where n is the number of elements, add_table and mul_table are n x n matrices of indices,
# and I_list is a list of indices representing the subset I.
Z2_n = 2
Z2_add = [[0, 1], [1, 0]]
Z2_mul = [[0, 0], [0, 1]]

Z2xZ2_n = 4
Z2xZ2_add = [
    [0, 1, 2, 3],
    [1, 0, 3, 2],
    [2, 3, 0, 1],
    [3, 2, 1, 0]
]
Z2xZ2_mul = [
    [0, 0, 0, 0],
    [0, 1, 0, 1],
    [0, 0, 2, 2],
    [0, 1, 2, 3]
]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: The quotient ring R/I is not a Boolean ring"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    try:
        n, add_table, mul_table, I_list = witness
        n = int(n)
        if n <= 0:
            return [False, False]
    except Exception:
        return [False, False]

    # H_1: R is a Boolean ring
    h1_ok = False
    try:
        def check_h1():
            if len(add_table) != n or any(len(row) != n for row in add_table): return False
            if len(mul_table) != n or any(len(row) != n for row in mul_table): return False
            
            for i in range(n):
                for j in range(n):
                    val_a = add_table[i][j]
                    val_m = mul_table[i][j]
                    if not isinstance(val_a, int) or not (0 <= val_a < n): return False
                    if not isinstance(val_m, int) or not (0 <= val_m < n): return False

            # Addition commutative
            for i in range(n):
                for j in range(n):
                    if add_table[i][j] != add_table[j][i]: return False

            # Addition associative
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False

            # Additive identity
            zero = -1
            for i in range(n):
                if all(add_table[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero == -1: return False

            # Additive inverse
            for i in range(n):
                if not any(add_table[i][j] == zero for j in range(n)): return False

            # Multiplication associative
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False

            # Distributive
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                        if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False

            # Boolean property (x^2 = x)
            for i in range(n):
                if mul_table[i][i] != i: return False

            return True
        h1_ok = check_h1()
    except Exception:
        h1_ok = False

    # ¬Q: R/I is not a Boolean ring
    neg_q_ok = False
    try:
        def check_q():
            try:
                I_set = set(I_list)
            except TypeError:
                return False
                
            for i in I_set:
                if not isinstance(i, int) or i < 0 or i >= n:
                    return False
            
            zero = -1
            for i in range(n):
                if all(add_table[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero == -1: return False
            
            neg = [-1] * n
            for i in range(n):
                for j in range(n):
                    if add_table[i][j] == zero:
                        neg[i] = j
                        break
                if neg[i] == -1: return False
                
            def equiv(x, y):
                return add_table[x][neg[y]] in I_set
                
            # Check equivalence relation
            for x in range(n):
                if not equiv(x, x): return False
            for x in range(n):
                for y in range(n):
                    if equiv(x, y) != equiv(y, x): return False
            for x in range(n):
                for y in range(n):
                    for z in range(n):
                        if equiv(x, y) and equiv(y, z) and not equiv(x, z): return False
                        
            # Check well-defined operations
            for x1 in range(n):
                for y1 in range(n):
                    if not equiv(x1, y1): continue
                    for x2 in range(n):
                        for y2 in range(n):
                            if not equiv(x2, y2): continue
                            
                            sum_x = add_table[x1][x2]
                            sum_y = add_table[y1][y2]
                            if not equiv(sum_x, sum_y): return False
                            
                            mul_x = mul_table[x1][x2]
                            mul_y = mul_table[y1][y2]
                            if not equiv(mul_x, mul_y): return False
                            
            # Check Boolean property of quotient
            for x in range(n):
                if not equiv(mul_table[x][x], x): return False
                
            return True
        
        q_ok = check_q()
        neg_q_ok = not q_ok
    except Exception:
        # If an unexpected error occurs during evaluation, we conservatively return False
        # to avoid false positives in the verifier.
        neg_q_ok = False

    return [h1_ok, neg_q_ok]