import itertools
from sympy import eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: x is an element of R such that x^n is not equal to 0 for all positive integers n",
    "¬Q: There does not exist a prime ideal P of R such that x is not an element of P"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if isinstance(witness, tuple) and len(witness) == 4 and isinstance(witness[0], int):
            n, add, mult, x = witness
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], list):
            matrices, x_mat = witness
            n = len(matrices)
            mat_to_idx = {}
            for i, m in enumerate(matrices):
                if hasattr(m, 'tolist'):
                    t = tuple(tuple(row) for row in m.tolist())
                else:
                    t = tuple(tuple(row) for row in m)
                mat_to_idx[t] = i
            
            add = [[0]*n for _ in range(n)]
            mult = [[0]*n for _ in range(n)]
            for i, a in enumerate(matrices):
                for j, b in enumerate(matrices):
                    s = a + b
                    p = a * b
                    if hasattr(s, 'tolist'):
                        s_t = tuple(tuple(row) for row in s.tolist())
                    else:
                        s_t = tuple(tuple(row) for row in s)
                    if hasattr(p, 'tolist'):
                        p_t = tuple(tuple(row) for row in p.tolist())
                    else:
                        p_t = tuple(tuple(row) for row in p)
                    add[i][j] = mat_to_idx[s_t]
                    mult[i][j] = mat_to_idx[p_t]
            
            if hasattr(x_mat, 'tolist'):
                x_t = tuple(tuple(row) for row in x_mat.tolist())
            else:
                x_t = tuple(tuple(row) for row in x_mat)
            x = mat_to_idx[x_t]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    if n > 256:
        return [False, False]

    try:
        zero = None
        for i in range(n):
            if all(add[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None:
            return [False, False]
        
        curr = x
        seen = set()
        is_nilpotent = False
        while curr not in seen:
            if curr == zero:
                is_nilpotent = True
                break
            seen.add(curr)
            curr = mult[curr][x]
        h1 = not is_nilpotent
    except Exception:
        h1 = False

    try:
        principal_ideals = []
        for i in range(n):
            gen = {i}
            closure = set(gen)
            while True:
                new_elements = set()
                for a in closure:
                    for r in range(n):
                        p1 = mult[r][a]
                        p2 = mult[a][r]
                        if p1 not in closure and p1 not in new_elements:
                            new_elements.add(p1)
                        if p2 not in closure and p2 not in new_elements:
                            new_elements.add(p2)
                for a in closure:
                    for b in closure:
                        s = add[a][b]
                        if s not in closure and s not in new_elements:
                            new_elements.add(s)
                if not new_elements:
                    break
                closure.update(new_elements)
            principal_ideals.append(frozenset(closure))
        
        current_ideals = set(principal_ideals)
        all_ideals = set(current_ideals)
        while True:
            new_ideals = set()
            for I in current_ideals:
                for J in principal_ideals:
                    sum_IJ = set(I) | set(J)
                    closure = set(sum_IJ)
                    while True:
                        new_elems = set()
                        for a in closure:
                            for b in closure:
                                s = add[a][b]
                                if s not in closure and s not in new_elems:
                                    new_elems.add(s)
                        if not new_elems:
                            break
                        closure.update(new_elems)
                    new_ideals.add(frozenset(closure))
            new_ideals = new_ideals - all_ideals
            if not new_ideals:
                break
            all_ideals.update(new_ideals)
            current_ideals = new_ideals
        
        found_prime_avoiding_x = False
        for P in all_ideals:
            if x not in P:
                if len(P) == n:
                    continue
                is_prime = True
                for a in range(n):
                    for b in range(n):
                        if mult[a][b] in P:
                            if a not in P and b not in P:
                                is_prime = False
                                break
                    if not is_prime:
                        break
                if is_prime:
                    found_prime_avoiding_x = True
                    break
        
        neg_q = not found_prime_avoiding_x
    except Exception:
        neg_q = False

    return [h1, neg_q]