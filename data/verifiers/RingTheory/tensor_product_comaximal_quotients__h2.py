import sympy
from sympy import Matrix
from sympy.matrices.normalforms import smith_normal_form

# Expected witness format:
# witness = (n, add, mul, I, J)
# where:
#   n: int, number of elements in the ring (elements are 0, 1, ..., n-1)
#   add: n x n list of lists, addition table
#   mul: n x n list of lists, multiplication table
#   I: list of ints, elements of ideal I
#   J: list of ints, elements of ideal J

def conditions(witness):
    try:
        n, add, mul, I, J = witness
        if not isinstance(n, int) or n <= 0:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring
    try:
        h1 = True
        if not isinstance(add, list) or not isinstance(mul, list):
            h1 = False
        if h1 and (len(add) != n or len(mul) != n):
            h1 = False
            
        if h1:
            for i in range(n):
                if not isinstance(add[i], list) or len(add[i]) != n: h1 = False
                if not isinstance(mul[i], list) or len(mul[i]) != n: h1 = False
                
        if h1:
            for i in range(n):
                for j in range(n):
                    if not isinstance(add[i][j], int) or not (0 <= add[i][j] < n): h1 = False
                    if not isinstance(mul[i][j], int) or not (0 <= mul[i][j] < n): h1 = False
                    
        if h1:
            # add is commutative
            for i in range(n):
                for j in range(n):
                    if add[i][j] != add[j][i]: h1 = False
                    
        if h1:
            # add is associative
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if add[add[i][j]][k] != add[i][add[j][k]]: h1 = False
                        
        if h1:
            # exists zero
            zero = None
            for i in range(n):
                if all(add[i][j] == j for j in range(n)):
                    zero = i
                    break
            if zero is None: h1 = False
            
        if h1:
            # exists neg
            for i in range(n):
                if not any(add[i][j] == zero for j in range(n)): h1 = False
                
        if h1:
            # mul is commutative
            for i in range(n):
                for j in range(n):
                    if mul[i][j] != mul[j][i]: h1 = False
                    
        if h1:
            # mul is associative
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul[mul[i][j]][k] != mul[i][mul[j][k]]: h1 = False
                        
        if h1:
            # distributive
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: h1 = False
    except Exception:
        h1 = False

    # H_2: I and J are comaximal ideals
    try:
        h2 = True
        if not isinstance(I, list) or not isinstance(J, list):
            h2 = False
        if h2 and (not I or not J):
            h2 = False
            
        if h2:
            for x in I:
                if not isinstance(x, int) or x < 0 or x >= n: h2 = False
            for x in J:
                if not isinstance(x, int) or x < 0 or x >= n: h2 = False
                
        if h2:
            # I is ideal
            for x in I:
                for y in I:
                    if add[x][y] not in I: h2 = False
                for r in range(n):
                    if mul[r][x] not in I: h2 = False
                    
            # J is ideal
            for x in J:
                for y in J:
                    if add[x][y] not in J: h2 = False
                for r in range(n):
                    if mul[r][x] not in J: h2 = False
                    
        if h2:
            # I + J == R
            sums = set()
            for i in I:
                for j in J:
                    sums.add(add[i][j])
            if len(sums) != n:
                h2 = False
    except Exception:
        h2 = False

    # neg_Q: R/I \otimes_R R/J is not isomorphic to the zero module
    try:
        neg_q = False
        if h1 and h2:
            active_gens = []
            gen_idx = {}
            for x in range(n):
                for y in range(n):
                    if x not in I and y not in J:
                        gen_idx[(x, y)] = len(active_gens)
                        active_gens.append((x, y))
            
            num_vars = len(active_gens)
            if num_vars == 0:
                neg_q = False
            else:
                relations = set()
                
                def add_relation(terms):
                    row = [0] * num_vars
                    for coeff, x, y in terms:
                        if (x, y) in gen_idx:
                            row[gen_idx[(x, y)]] += coeff
                    if any(row):
                        relations.add(tuple(row))

                for x1 in range(n):
                    for x2 in range(n):
                        for y in range(n):
                            add_relation([
                                (1, add[x1][x2], y),
                                (-1, x1, y),
                                (-1, x2, y)
                            ])
                            
                for x in range(n):
                    for y1 in range(n):
                        for y2 in range(n):
                            add_relation([
                                (1, x, add[y1][y2]),
                                (-1, x, y1),
                                (-1, x, y2)
                            ])
                            
                for r in range(n):
                    for x in range(n):
                        for y in range(n):
                            add_relation([
                                (1, mul[r][x], y),
                                (-1, x, mul[r][y])
                            ])
                            
                if not relations:
                    neg_q = True
                else:
                    M = Matrix(list(relations))
                    S = smith_normal_form(M)
                    is_zero_module = True
                    for i in range(num_vars):
                        if i >= S.rows:
                            is_zero_module = False
                            break
                        if S[i, i] != 1 and S[i, i] != -1:
                            is_zero_module = False
                            break
                    neg_q = not is_zero_module
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals (I + J = R)",
    "¬Q: R/I \\otimes_R R/J is not isomorphic to the zero module"
]

N_HYP = 2
NEG_Q_INDEX = 2