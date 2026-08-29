import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z

def conditions(witness):
    """
    Expects witness to be a dictionary or tuple representing a finite ring and two ideals:
    witness = {
        "n": int,
        "add": [[int, ...], ...],  # n x n addition table
        "mul": [[int, ...], ...],  # n x n multiplication table
        "M1": [int, ...],          # elements of ideal M1
        "M2": [int, ...]           # elements of ideal M2
    }
    or witness = (n, add_table, mul_table, M1, M2)
    """
    try:
        if isinstance(witness, dict):
            n = int(witness["n"])
            add_table = witness["add"]
            mul_table = witness["mul"]
            M1 = set(witness["M1"])
            M2 = set(witness["M2"])
        elif isinstance(witness, tuple) and len(witness) == 5:
            n = int(witness[0])
            add_table = witness[1]
            mul_table = witness[2]
            M1 = set(witness[3])
            M2 = set(witness[4])
        else:
            return [False, False, False, False]
            
        if not isinstance(n, int) or n <= 0:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    def is_ring(n, add_table, mul_table):
        if len(add_table) != n or len(mul_table) != n: return False
        for row in add_table:
            if len(row) != n: return False
            for val in row:
                if not (0 <= val < n): return False
        for row in mul_table:
            if len(row) != n: return False
            for val in row:
                if not (0 <= val < n): return False
        
        # Check abelian group under addition
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False
        
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False
        
        for i in range(n):
            if not any(add_table[i][j] == zero for j in range(n)): return False
            
        # Check associative multiplication
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False
                    
        # Check distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False
                    
        return True

    def is_ideal(n, add_table, mul_table, subset):
        if not subset: return False
        for x in subset:
            if not (0 <= x < n): return False
            for y in subset:
                if add_table[x][y] not in subset:
                    return False
        for x in subset:
            for r in range(n):
                if mul_table[r][x] not in subset:
                    return False
                if mul_table[x][r] not in subset:
                    return False
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None or zero not in subset:
            return False
        for x in subset:
            has_inv = False
            for y in subset:
                if add_table[x][y] == zero:
                    has_inv = True
                    break
            if not has_inv:
                return False
        return True

    def is_maximal_ideal(n, add_table, mul_table, subset):
        if not is_ideal(n, add_table, mul_table, subset):
            return False
        if len(subset) == n:
            return False
        
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
                
        for x in range(n):
            if x in subset:
                continue
            
            gen_set = set(subset)
            gen_set.add(x)
            queue = [x]
            
            while queue:
                curr = queue.pop(0)
                
                new_elements = []
                for a in list(gen_set):
                    val = add_table[curr][a]
                    if val not in gen_set:
                        new_elements.append(val)
                        
                for r in range(n):
                    val = mul_table[r][curr]
                    if val not in gen_set:
                        new_elements.append(val)
                    val = mul_table[curr][r]
                    if val not in gen_set:
                        new_elements.append(val)
                        
                for b in range(n):
                    if add_table[curr][b] == zero:
                        if b not in gen_set:
                            new_elements.append(b)
                        break
                        
                for val in new_elements:
                    if val not in gen_set:
                        gen_set.add(val)
                        queue.append(val)
                        
            if len(gen_set) < n:
                return False
                
        return True

    try:
        ring_valid = is_ring(n, add_table, mul_table)
        h1 = ring_valid and is_maximal_ideal(n, add_table, mul_table, M1)
    except Exception:
        h1 = False

    try:
        ring_valid = is_ring(n, add_table, mul_table)
        h2 = ring_valid and is_maximal_ideal(n, add_table, mul_table, M2)
    except Exception:
        h2 = False

    try:
        h3 = (M1 != M2)
    except Exception:
        h3 = False

    try:
        sum_ideal = set()
        for x in M1:
            for y in M2:
                sum_ideal.add(add_table[x][y])
        neg_q = (len(sum_ideal) != n)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M1 is a maximal ideal of R",
    "H_2: M2 is a maximal ideal of R",
    "H_3: M1 != M2",
    "¬Q: M1 + M2 != R"
]

N_HYP = 3
NEG_Q_INDEX = 3