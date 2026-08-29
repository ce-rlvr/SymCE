import itertools

def _make_Zn(n):
    add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

def _make_product_ring(R1, R2):
    n1, add1, mul1 = R1
    n2, add2, mul2 = R2
    n = n1 * n2
    add_table = [[0]*n for _ in range(n)]
    mul_table = [[0]*n for _ in range(n)]
    for i in range(n1):
        for j in range(n2):
            for k in range(n1):
                for l in range(n2):
                    u = i * n2 + j
                    v = k * n2 + l
                    add_table[u][v] = add1[i][k] * n2 + add2[j][l]
                    mul_table[u][v] = mul1[i][k] * n2 + mul2[j][l]
    return (n, add_table, mul_table)

Z2 = _make_Zn(2)
Z3 = _make_Zn(3)
Z4 = _make_Zn(4)
Z5 = _make_Zn(5)
Z6 = _make_Zn(6)
Z8 = _make_Zn(8)
Z2xZ2 = _make_product_ring(Z2, Z2)

def conditions(witness) -> list[bool]:
    """
    witness can be either:
      - (ring, I, J) where ring is (n, add_table, mul_table)
      - (n, add_table, mul_table, I, J)
    where add_table and mul_table are n x n lists of lists (or callable functions),
    and I, J are lists/sets of elements in 0..n-1.
    """
    try:
        if len(witness) == 3:
            ring, I, J = witness
            n, add_table, mul_table = ring
        elif len(witness) == 5:
            n, add_table, mul_table, I, J = witness
        else:
            return [False, False, False, False]
            
        if callable(add_table) and callable(mul_table):
            add_func = add_table
            mul_func = mul_table
            add_table = [[add_func(i, j) for j in range(n)] for i in range(n)]
            mul_table = [[mul_func(i, j) for j in range(n)] for i in range(n)]
            
    except Exception:
        return [False, False, False, False]

    # H1: R is a commutative ring with identity
    try:
        if not isinstance(n, int) or n <= 0:
            h1 = False
        elif len(add_table) != n or any(len(row) != n for row in add_table):
            h1 = False
        elif len(mul_table) != n or any(len(row) != n for row in mul_table):
            h1 = False
        else:
            R = list(range(n))
            add_comm = all(add_table[i][j] == add_table[j][i] for i in R for j in R)
            add_assoc = all(add_table[add_table[i][j]][k] == add_table[i][add_table[j][k]] for i in R for j in R for k in R)
            
            zeros = [z for z in R if all(add_table[z][i] == i for i in R)]
            zero = zeros[0] if zeros else None
            
            if zero is not None:
                add_inv = all(any(add_table[i][j] == zero for j in R) for i in R)
            else:
                add_inv = False
                
            mul_comm = all(mul_table[i][j] == mul_table[j][i] for i in R for j in R)
            mul_assoc = all(mul_table[mul_table[i][j]][k] == mul_table[i][mul_table[j][k]] for i in R for j in R for k in R)
            
            dist_left = all(mul_table[i][add_table[j][k]] == add_table[mul_table[i][j]][mul_table[i][k]] for i in R for j in R for k in R)
            dist_right = all(mul_table[add_table[i][j]][k] == add_table[mul_table[i][k]][mul_table[j][k]] for i in R for j in R for k in R)
            
            ones = [u for u in R if all(mul_table[u][i] == i for i in R)]
            one = ones[0] if ones else None
            
            h1 = bool(add_comm and add_assoc and zero is not None and add_inv and mul_comm and mul_assoc and dist_left and dist_right and one is not None)
    except Exception:
        h1 = False

    # H2: I + J = R
    try:
        if not h1:
            h2 = False
        else:
            I_set = set(I)
            J_set = set(J)
            if not (I_set.issubset(set(R)) and J_set.issubset(set(R))):
                h2 = False
            else:
                sums = set(add_table[i][j] for i in I_set for j in J_set)
                h2 = (sums == set(R))
    except Exception:
        h2 = False

    # H3: I \cap J = {0}
    try:
        if not h1:
            h3 = False
        else:
            I_set = set(I)
            J_set = set(J)
            h3 = (I_set.intersection(J_set) == {zero})
    except Exception:
        h3 = False

    # neg_Q: There does NOT exist a unique idempotent e such that I = <1-e> and J = <e>
    try:
        if not h1:
            neg_q = False
        else:
            I_set = set(I)
            J_set = set(J)
            
            def get_ideal(x):
                return set(mul_table[r][x] for r in R)
                
            def get_neg(x):
                for y in R:
                    if add_table[x][y] == zero:
                        return y
                return None
                
            valid_e_count = 0
            for e in R:
                if mul_table[e][e] == e:
                    neg_e = get_neg(e)
                    one_minus_e = add_table[one][neg_e]
                    if get_ideal(one_minus_e) == I_set and get_ideal(e) == J_set:
                        valid_e_count += 1
                        
            neg_q = (valid_e_count != 1)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I + J = R",
    "H_3: I \\cap J = {0}",
    "¬Q: There does not exist a unique idempotent e such that I = <1-e> and J = <e>"
]

N_HYP = 3
NEG_Q_INDEX = 3