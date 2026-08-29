import itertools

def make_Zn(n):
    add_table = [[(i + j) % n for j in range(n)] for i in range(n)]
    mul_table = [[(i * j) % n for j in range(n)] for i in range(n)]
    return (n, add_table, mul_table)

def make_M2_F2():
    elements = list(itertools.product([0, 1], repeat=4))
    def add_mat(x, y):
        return tuple((a+b)%2 for a, b in zip(x, y))
    def mul_mat(x, y):
        a, b, c, d = x
        e, f, g, h = y
        return (
            (a*e + b*g)%2,
            (a*f + b*h)%2,
            (c*e + d*g)%2,
            (c*f + d*h)%2
        )
    add_table = [[0]*16 for _ in range(16)]
    mul_table = [[0]*16 for _ in range(16)]
    for i, x in enumerate(elements):
        for j, y in enumerate(elements):
            add_table[i][j] = elements.index(add_mat(x, y))
            mul_table[i][j] = elements.index(mul_mat(x, y))
    return (16, add_table, mul_table)

# Top-level setup: named object bindings that the witness expression may reference.
# Rings are represented as tuples: (n, add_table, mul_table)
Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z6 = make_Zn(6)
M2_F2 = make_M2_F2()

def conditions(witness):
    try:
        if isinstance(witness, int):
            witness = make_Zn(witness)
            
        if not (isinstance(witness, tuple) and len(witness) == 3):
            return [False]
            
        n, add_table, mul_table = witness
        
        if n < 2 or n > 100:
            return [False]
            
        if len(add_table) != n or len(mul_table) != n:
            return [False]
        for row in add_table:
            if len(row) != n: return [False]
        for row in mul_table:
            if len(row) != n: return [False]
            
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None:
            return [False]
            
        def get_left_ideal_closure(generators):
            closure = set(generators)
            closure.add(zero)
            while True:
                new_elements = set()
                for x in closure:
                    for y in closure:
                        new_elements.add(add_table[x][y])
                    for r in range(n):
                        new_elements.add(mul_table[r][x])
                if new_elements.issubset(closure):
                    break
                closure.update(new_elements)
            return frozenset(closure)

        principal_left_ideals = set()
        for i in range(n):
            principal_left_ideals.add(get_left_ideal_closure([i]))
            
        left_ideals = set(principal_left_ideals)
        while True:
            new_ideals = set(left_ideals)
            for I in left_ideals:
                for J in principal_left_ideals:
                    sum_ideal = set()
                    for x in I:
                        for y in J:
                            sum_ideal.add(add_table[x][y])
                    new_ideals.add(frozenset(sum_ideal))
            if len(new_ideals) == len(left_ideals):
                break
            left_ideals = new_ideals

        def get_right_ideal_closure(generators):
            closure = set(generators)
            closure.add(zero)
            while True:
                new_elements = set()
                for x in closure:
                    for y in closure:
                        new_elements.add(add_table[x][y])
                    for r in range(n):
                        new_elements.add(mul_table[x][r])
                if new_elements.issubset(closure):
                    break
                closure.update(new_elements)
            return frozenset(closure)

        principal_right_ideals = set()
        for i in range(n):
            principal_right_ideals.add(get_right_ideal_closure([i]))
            
        right_ideals = set(principal_right_ideals)
        while True:
            new_ideals = set(right_ideals)
            for I in right_ideals:
                for J in principal_right_ideals:
                    sum_ideal = set()
                    for x in I:
                        for y in J:
                            sum_ideal.add(add_table[x][y])
                    new_ideals.add(frozenset(sum_ideal))
            if len(new_ideals) == len(right_ideals):
                break
            right_ideals = new_ideals

        def left_annihilator(S):
            ann = set()
            for x in range(n):
                if all(mul_table[x][s] == zero for s in S):
                    ann.add(x)
            return frozenset(ann)

        def right_annihilator(S):
            ann = set()
            for x in range(n):
                if all(mul_table[s][x] == zero for s in S):
                    ann.add(x)
            return frozenset(ann)

        is_qf = True
        for I in left_ideals:
            if left_annihilator(right_annihilator(I)) != I:
                is_qf = False
                break
        if is_qf:
            for J in right_ideals:
                if right_annihilator(left_annihilator(J)) != J:
                    is_qf = False
                    break

        minimal_left_ideals = []
        for I in left_ideals:
            if len(I) > 1:
                is_minimal = True
                for J in left_ideals:
                    if len(J) > 1 and J != I and J.issubset(I):
                        is_minimal = False
                        break
                if is_minimal:
                    minimal_left_ideals.append(I)
                    
        socle_is_simple = (len(minimal_left_ideals) == 1)
        
        equivalence = (is_qf == socle_is_simple)
        neg_q = not equivalence
        
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: The equivalence 'R is quasi-Frobenius iff its socle is simple' fails"]
N_HYP = 0
NEG_Q_INDEX = 0