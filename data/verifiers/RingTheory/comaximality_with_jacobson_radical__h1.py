import itertools
import math

# Top-level setup
# Witnesses for this conjecture are expected to be finite rings represented as a tuple:
# (n, add_table, mul_table, I_elements)
# where n is the number of elements (0 to n-1),
# add_table and mul_table are n x n lists of lists representing the operations,
# and I_elements is a list of elements in the ideal I.

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: I is an ideal of R",
    "H_3: I and J(R) are comaximal",
    "¬Q: I is not the entire ring R"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            n, add, mul, I = witness
        else:
            n = witness.n
            add = witness.add
            mul = witness.mul
            I = witness.I
            
        n = int(n)
        if n <= 0:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: R is a ring
    h1 = False
    zero = None
    try:
        if len(add) == n and all(len(row) == n for row in add) and \
           len(mul) == n and all(len(row) == n for row in mul):
            
            # Find the additive identity
            zeros = [e for e in range(n) if all(add[e][x] == x for x in range(n)) and all(add[x][e] == x for x in range(n))]
            if zeros:
                zero = zeros[0]
                is_group = True
                
                # Check commutativity of addition
                for i in range(n):
                    for j in range(n):
                        if add[i][j] != add[j][i]: 
                            is_group = False
                            break
                    if not is_group: break
                
                # Check existence of additive inverses
                if is_group:
                    for i in range(n):
                        if not any(add[i][j] == zero for j in range(n)):
                            is_group = False
                            break
                
                # Check associativity and distributivity
                if is_group:
                    for i in range(n):
                        for j in range(n):
                            for k in range(n):
                                if add[add[i][j]][k] != add[i][add[j][k]]: is_group = False
                                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: is_group = False
                                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: is_group = False
                                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: is_group = False
                                if not is_group: break
                            if not is_group: break
                        if not is_group: break
                
                h1 = is_group
    except Exception:
        h1 = False

    # H2: I is an ideal of R
    h2 = False
    try:
        if h1 and zero is not None:
            I_set = set(I)
            if all(isinstance(x, int) and 0 <= x < n for x in I_set) and len(I_set) > 0:
                is_id = True
                for x in I_set:
                    inv_x = next((y for y in range(n) if add[x][y] == zero), None)
                    if inv_x is None or inv_x not in I_set: 
                        is_id = False
                        break
                    for y in I_set:
                        if add[x][y] not in I_set: 
                            is_id = False
                            break
                    for r in range(n):
                        if mul[r][x] not in I_set: 
                            is_id = False
                            break
                        if mul[x][r] not in I_set: 
                            is_id = False
                            break
                    if not is_id: break
                h2 = is_id
    except Exception:
        h2 = False

    # H3: I and J(R) are comaximal (I + J(R) = R)
    h3 = False
    try:
        if h1 and h2:
            # An element z is left quasi-regular if there exists w such that w + z - wz = 0.
            # In our table notation, this means w + z = wz, or add[w][z] == mul[w][z].
            def is_lqr(z):
                for w in range(n):
                    if add[w][z] == mul[w][z]:
                        return True
                return False

            # The Jacobson radical J(R) is the set of all x such that for all y, yx is left quasi-regular.
            J = []
            for x in range(n):
                in_J = True
                for y in range(n):
                    yx = mul[y][x]
                    if not is_lqr(yx):
                        in_J = False
                        break
                if in_J:
                    J.append(x)
            
            # Check if I + J(R) = R
            sums = set()
            for x in I:
                for y in J:
                    sums.add(add[x][y])
            h3 = (len(sums) == n)
    except Exception:
        h3 = False

    # neg_Q: I is not the entire ring R
    neg_q = False
    try:
        if h1 and h2:
            neg_q = (len(set(I)) != n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]