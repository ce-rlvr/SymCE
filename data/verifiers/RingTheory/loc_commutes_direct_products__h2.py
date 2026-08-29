import itertools
import sympy.abc as abc
from sympy import Rational, Integer

# Top-level setup
# (No specific named objects required for this domain, but we provide standard sympy symbols)

def get_localization_ring(R_elems, S_elems, R_list):
    def add(x, y):
        return tuple((a + b) % n for a, b, n in zip(x, y, R_list))
    def mul(x, y):
        return tuple((a * b) % n for a, b, n in zip(x, y, R_list))
    def sub(x, y):
        return tuple((a - b) % n for a, b, n in zip(x, y, R_list))
    
    zero = tuple(0 for _ in R_list)
    
    class_reps = []
    for r in R_elems:
        for s in S_elems:
            found = False
            for rep in class_reps:
                r2, s2 = rep
                diff = sub(mul(r, s2), mul(r2, s))
                equiv = False
                for t in S_elems:
                    if mul(t, diff) == zero:
                        equiv = True
                        break
                if equiv:
                    found = True
                    break
            if not found:
                class_reps.append((r, s))
                
    n_classes = len(class_reps)
    add_table = [[-1]*n_classes for _ in range(n_classes)]
    mul_table = [[-1]*n_classes for _ in range(n_classes)]
    
    for i in range(n_classes):
        r1, s1 = class_reps[i]
        for j in range(n_classes):
            r2, s2 = class_reps[j]
            
            num_add = add(mul(r1, s2), mul(r2, s1))
            den_add = mul(s1, s2)
            num_mul = mul(r1, r2)
            den_mul = mul(s1, s2)
            
            for k, rep in enumerate(class_reps):
                rk, sk = rep
                diff = sub(mul(num_add, sk), mul(rk, den_add))
                equiv = False
                for t in S_elems:
                    if mul(t, diff) == zero:
                        equiv = True
                        break
                if equiv:
                    add_table[i][j] = k
                    break
                    
            for k, rep in enumerate(class_reps):
                rk, sk = rep
                diff = sub(mul(num_mul, sk), mul(rk, den_mul))
                equiv = False
                for t in S_elems:
                    if mul(t, diff) == zero:
                        equiv = True
                        break
                if equiv:
                    mul_table[i][j] = k
                    break
                    
    for row in add_table:
        if -1 in row:
            raise ValueError("Addition not closed")
    for row in mul_table:
        if -1 in row:
            raise ValueError("Multiplication not closed")
            
    return add_table, mul_table

def get_product_ring(rings):
    sizes = [len(r[0]) for r in rings]
    elements = list(itertools.product(*[range(s) for s in sizes]))
    n_elements = len(elements)
    elem_to_idx = {elem: i for i, elem in enumerate(elements)}
    
    add_table = [[0]*n_elements for _ in range(n_elements)]
    mul_table = [[0]*n_elements for _ in range(n_elements)]
    
    for i, e1 in enumerate(elements):
        for j, e2 in enumerate(elements):
            sum_e = tuple(rings[k][0][e1[k]][e2[k]] for k in range(len(rings)))
            mul_e = tuple(rings[k][1][e1[k]][e2[k]] for k in range(len(rings)))
            add_table[i][j] = elem_to_idx[sum_e]
            mul_table[i][j] = elem_to_idx[mul_e]
            
    return add_table, mul_table

def are_isomorphic(ring1, ring2):
    add1, mul1 = ring1
    add2, mul2 = ring2
    n = len(add1)
    if len(add2) != n:
        return False
    if n == 0:
        return True
    
    if n > 8:
        # Too large to check all permutations quickly.
        # Return True to make neg_Q False, forcing the witness to be small.
        return True
        
    def find_identities(add, mul, n):
        zero = None
        one = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
            if all(mul[i][j] == j for j in range(n)):
                one = i
        return zero, one

    z1, o1 = find_identities(add1, mul1, n)
    z2, o2 = find_identities(add2, mul2, n)
    
    if (z1 is None) != (z2 is None) or (o1 is None) != (o2 is None):
        return False

    for p in itertools.permutations(range(n)):
        if z1 is not None and p[z1] != z2:
            continue
        if o1 is not None and p[o1] != o2:
            continue
            
        ok = True
        for i in range(n):
            pi = p[i]
            for j in range(n):
                if p[add1[i][j]] != add2[pi][p[j]]:
                    ok = False
                    break
                if p[mul1[i][j]] != mul2[pi][p[j]]:
                    ok = False
                    break
            if not ok:
                break
        if ok:
            return True
    return False

def conditions(witness) -> list[bool]:
    # H1: R_1, ..., R_n are commutative rings
    try:
        R_list = witness['R_list']
        h1 = isinstance(R_list, list) and len(R_list) > 0 and all(isinstance(n, int) and n >= 1 for n in R_list)
    except Exception:
        h1 = False

    # H2: S_i is a multiplicatively closed subset of R_i for each i
    try:
        R_list = witness['R_list']
        S_list = witness['S_list']
        h2 = True
        if len(S_list) != len(R_list):
            h2 = False
        else:
            for i, n in enumerate(R_list):
                S_i = S_list[i]
                if not isinstance(S_i, list) or len(S_i) == 0:
                    h2 = False
                    break
                if (1 % n) not in S_i:
                    h2 = False
                    break
                for a in S_i:
                    for b in S_i:
                        if (a * b) % n not in S_i:
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # H3: S is the direct product S_1 \times ... \times S_n
    try:
        S_list = witness['S_list']
        S = witness['S']
        expected_S = set(itertools.product(*S_list))
        h3 = set(S) == expected_S
    except Exception:
        h3 = False

    # neg_Q: S^{-1}R is NOT isomorphic to \prod S_i^{-1}R_i
    try:
        R_list = witness['R_list']
        S_list = witness['S_list']
        R = witness['R']
        S = witness['S']
        
        identity = tuple(1 % n for n in R_list)
        if identity not in R:
            neg_q = False
        else:
            R_set = set(R)
            valid_R = True
            for a in R:
                for b in R:
                    add_ab = tuple((x + y) % n for x, y, n in zip(a, b, R_list))
                    mul_ab = tuple((x * y) % n for x, y, n in zip(a, b, R_list))
                    if add_ab not in R_set or mul_ab not in R_set:
                        valid_R = False
                        break
                if not valid_R: break
            
            if not valid_R:
                neg_q = False
            elif not set(S).issubset(R_set):
                neg_q = False
            else:
                ring_S_inv_R = get_localization_ring(R, S, R_list)
                
                local_rings = []
                for i, n in enumerate(R_list):
                    R_i_elems = [(x,) for x in range(n)]
                    S_i_elems = [(x,) for x in S_list[i]]
                    l_ring = get_localization_ring(R_i_elems, S_i_elems, [n])
                    local_rings.append(l_ring)
                    
                prod_ring = get_product_ring(local_rings)
                
                neg_q = not are_isomorphic(ring_S_inv_R, prod_ring)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: R_1, ..., R_n are commutative rings",
    "H_2: S_i is a multiplicatively closed subset of R_i for each i",
    "H_3: S is the direct product S_1 \\times ... \\times S_n",
    "¬Q: S^{-1}R is not isomorphic to S_1^{-1}R_1 \\times ... \\times S_n^{-1}R_n"
]

N_HYP = 3
NEG_Q_INDEX = 3