import sympy

# Top-level setup
# Witnesses for this conjecture are expected to be finite rings represented as tuples:
# (n_elements, add_table, mult_table, I, J, m, n)
# where elements are integers 0 to n_elements - 1.

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I and J are comaximal ideals (I + J = R)",
    "H_3: m and n are positive integers",
    "¬Q: I^m and J^n are not comaximal (I^m + J^n != R)"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        if len(witness) != 7:
            return [False, False, False, False]
        n_elements, add_table, mult_table, I, J, m, n = witness
    except Exception:
        return [False, False, False, False]

    zero = None
    elements = []
    
    # H1: R is a commutative ring
    h1 = False
    try:
        if isinstance(n_elements, int) and n_elements > 0:
            elements = list(range(n_elements))
            
            valid_tables = True
            if len(add_table) != n_elements or any(len(row) != n_elements for row in add_table):
                valid_tables = False
            if len(mult_table) != n_elements or any(len(row) != n_elements for row in mult_table):
                valid_tables = False
                
            if valid_tables:
                # Commutativity and associativity of addition
                add_comm = all(add_table[x][y] == add_table[y][x] for x in elements for y in elements)
                add_assoc = all(add_table[add_table[x][y]][z] == add_table[x][add_table[y][z]] 
                                for x in elements for y in elements for z in elements)
                                
                # Additive identity
                zeros = [e for e in elements if all(add_table[e][x] == x and add_table[x][e] == x for x in elements)]
                
                if add_comm and add_assoc and zeros:
                    zero = zeros[0]
                    # Additive inverses
                    add_inv = all(any(add_table[x][y] == zero for y in elements) for x in elements)
                    
                    # Commutativity and associativity of multiplication
                    mult_comm = all(mult_table[x][y] == mult_table[y][x] for x in elements for y in elements)
                    mult_assoc = all(mult_table[mult_table[x][y]][z] == mult_table[x][mult_table[y][z]] 
                                     for x in elements for y in elements for z in elements)
                                     
                    # Distributivity
                    dist = all(mult_table[x][add_table[y][z]] == add_table[mult_table[x][y]][mult_table[x][z]] 
                               for x in elements for y in elements for z in elements)
                               
                    if add_inv and mult_comm and mult_assoc and dist:
                        h1 = True
    except Exception:
        h1 = False

    # H2: I and J are comaximal ideals
    h2 = False
    try:
        if h1 and zero is not None:
            I_set = set(I)
            J_set = set(J)
            
            if I_set.issubset(elements) and J_set.issubset(elements):
                def is_ideal(S):
                    if zero not in S:
                        return False
                    for x in S:
                        for y in S:
                            if add_table[x][y] not in S:
                                return False
                    for x in S:
                        inv_x = next((y for y in elements if add_table[x][y] == zero), None)
                        if inv_x not in S:
                            return False
                    for r in elements:
                        for x in S:
                            if mult_table[r][x] not in S:
                                return False
                    return True
                    
                if is_ideal(I_set) and is_ideal(J_set):
                    sum_IJ = {add_table[x][y] for x in I_set for y in J_set}
                    if sum_IJ == set(elements):
                        h2 = True
    except Exception:
        h2 = False

    # H3: m and n are positive integers
    h3 = False
    try:
        if isinstance(m, int) and m > 0 and isinstance(n, int) and n > 0:
            h3 = True
    except Exception:
        h3 = False

    # ¬Q: I^m + J^n != R
    neg_q = False
    try:
        if h1 and h3 and zero is not None:
            I_set = set(I)
            J_set = set(J)
            
            def ideal_product(A, B):
                base = {mult_table[a][b] for a in A for b in B}
                closure = set(base)
                if not closure:
                    closure.add(zero)
                while True:
                    new_elements = set()
                    for x in closure:
                        for y in closure:
                            z = add_table[x][y]
                            if z not in closure:
                                new_elements.add(z)
                    if not new_elements:
                        break
                    closure.update(new_elements)
                return closure

            def ideal_power(A, power):
                if power == 1:
                    return set(A)
                res = set(A)
                for _ in range(power - 1):
                    res = ideal_product(res, A)
                return res
                
            Im = ideal_power(I_set, m)
            Jn = ideal_power(J_set, n)
            
            sum_Im_Jn = {add_table[x][y] for x in Im for y in Jn}
            
            if sum_Im_Jn != set(elements):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]