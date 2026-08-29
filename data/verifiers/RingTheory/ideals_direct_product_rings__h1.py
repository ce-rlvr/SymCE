import itertools

def ZeroRing(n):
    """Returns a ring with zero multiplication: (n, add_table, mul_table)"""
    add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul_table = [[0 for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

def ZnRing(n):
    """Returns the ring of integers modulo n: (n, add_table, mul_table)"""
    add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

def conditions(witness):
    try:
        R1, R2, I = witness
    except Exception:
        return [False, False, False]

    def is_ring(R):
        try:
            if hasattr(R, 'n') and hasattr(R, 'add_table') and hasattr(R, 'mul_table'):
                n = int(R.n)
                add = R.add_table
                mul = R.mul_table
            else:
                n, add, mul = R
                n = int(n)
                
            if n <= 0: return False
            if len(add) != n or any(len(row) != n for row in add): return False
            if len(mul) != n or any(len(row) != n for row in mul): return False
            
            add = [[int(add[i][j]) for j in range(n)] for i in range(n)]
            mul = [[int(mul[i][j]) for j in range(n)] for i in range(n)]
            
            for i in range(n):
                for j in range(n):
                    if not (0 <= add[i][j] < n): return False
                    if not (0 <= mul[i][j] < n): return False
                    
            for i in range(n):
                for j in range(n):
                    if add[i][j] != add[j][i]: return False
                    
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if add[i][add[j][k]] != add[add[i][j]][k]: return False
                        
            id_add = -1
            for e in range(n):
                if all(add[e][i] == i for i in range(n)):
                    id_add = e
                    break
            if id_add == -1: return False
            
            for i in range(n):
                if not any(add[i][j] == id_add for j in range(n)): return False
                
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul[i][mul[j][k]] != mul[mul[i][j]][k]: return False
                        
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                        if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
                        
            return True
        except Exception:
            return False

    h1 = False
    try:
        h1 = is_ring(R1) and is_ring(R2)
    except Exception:
        pass

    def is_ideal(R1, R2, I):
        try:
            if hasattr(R1, 'n'):
                n1 = int(R1.n)
                add1 = [[int(x) for x in row] for row in R1.add_table]
                mul1 = [[int(x) for x in row] for row in R1.mul_table]
            else:
                n1, add1, mul1 = R1
                n1 = int(n1)
                add1 = [[int(x) for x in row] for row in add1]
                mul1 = [[int(x) for x in row] for row in mul1]
                
            if hasattr(R2, 'n'):
                n2 = int(R2.n)
                add2 = [[int(x) for x in row] for row in R2.add_table]
                mul2 = [[int(x) for x in row] for row in R2.mul_table]
            else:
                n2, add2, mul2 = R2
                n2 = int(n2)
                add2 = [[int(x) for x in row] for row in add2]
                mul2 = [[int(x) for x in row] for row in mul2]
                
            I_set = set()
            for e in I:
                if len(e) != 2: return False
                x, y = int(e[0]), int(e[1])
                if not (0 <= x < n1 and 0 <= y < n2): return False
                I_set.add((x, y))
                
            if not I_set: return False
            
            for (x1, y1) in I_set:
                for (x2, y2) in I_set:
                    if (add1[x1][x2], add2[y1][y2]) not in I_set: return False
                    
            id1 = next(e for e in range(n1) if all(add1[e][i] == i for i in range(n1)))
            id2 = next(e for e in range(n2) if all(add2[e][i] == i for i in range(n2)))
            
            for (x, y) in I_set:
                inv_x = next(i for i in range(n1) if add1[x][i] == id1)
                inv_y = next(i for i in range(n2) if add2[y][i] == id2)
                if (inv_x, inv_y) not in I_set: return False
                
            for (x, y) in I_set:
                for r1 in range(n1):
                    for r2 in range(n2):
                        if (mul1[r1][x], mul2[r2][y]) not in I_set: return False
                        if (mul1[x][r1], mul2[y][r2]) not in I_set: return False
                        
            return True
        except Exception:
            return False

    h2 = False
    try:
        if h1:
            h2 = is_ideal(R1, R2, I)
    except Exception:
        pass

    neg_q = False
    try:
        if h1 and h2:
            I_set = set()
            for e in I:
                I_set.add((int(e[0]), int(e[1])))
            I1 = set(x for x, y in I_set)
            I2 = set(y for x, y in I_set)
            expected_I = set(itertools.product(I1, I2))
            neg_q = (I_set != expected_I)
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings",
    "H_2: I is a two-sided ideal of R1 x R2",
    "¬Q: I is not of the form I1 x I2"
]

N_HYP = 2
NEG_Q_INDEX = 2