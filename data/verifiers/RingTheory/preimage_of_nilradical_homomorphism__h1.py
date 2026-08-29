import sympy
import itertools
import functools
import math

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict) and 'R_size' in witness:
            R_size = witness['R_size']
            S_size = witness['S_size']
            R_add = witness['R_add']
            R_mul = witness['R_mul']
            S_add = witness['S_add']
            S_mul = witness['S_mul']
            f_map = witness['f']
        elif isinstance(witness, tuple) and len(witness) == 7:
            R_size, S_size, R_add, R_mul, S_add, S_mul, f_map = witness
        elif isinstance(witness, tuple) and len(witness) == 3:
            R_elems, S_elems, f_func = witness
            R_size = len(R_elems)
            S_size = len(S_elems)
            
            R_add = [[0]*R_size for _ in range(R_size)]
            R_mul = [[0]*R_size for _ in range(R_size)]
            for i, a in enumerate(R_elems):
                for j, b in enumerate(R_elems):
                    R_add[i][j] = R_elems.index(a + b)
                    R_mul[i][j] = R_elems.index(a * b)
                    
            S_add = [[0]*S_size for _ in range(S_size)]
            S_mul = [[0]*S_size for _ in range(S_size)]
            for i, a in enumerate(S_elems):
                for j, b in enumerate(S_elems):
                    S_add[i][j] = S_elems.index(a + b)
                    S_mul[i][j] = S_elems.index(a * b)
                    
            f_map = [0]*R_size
            for i, a in enumerate(R_elems):
                if isinstance(f_func, dict):
                    f_map[i] = S_elems.index(f_func[a])
                else:
                    f_map[i] = S_elems.index(f_func(a))
        else:
            R_size = witness.R_size
            S_size = witness.S_size
            R_add = witness.R_add
            R_mul = witness.R_mul
            S_add = witness.S_add
            S_mul = witness.S_mul
            f_map = witness.f
    except Exception:
        return [False, False]

    def is_ring(size, add, mul):
        if not isinstance(size, int) or size < 1: return False
        if len(add) != size or len(mul) != size: return False
        for row in add + mul:
            if len(row) != size: return False
        for i in range(size):
            for j in range(size):
                if not isinstance(add[i][j], int) or not (0 <= add[i][j] < size): return False
                if not isinstance(mul[i][j], int) or not (0 <= mul[i][j] < size): return False
        for i in range(size):
            for j in range(size):
                if add[i][j] != add[j][i]: return False
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if add[add[i][j]][k] != add[i][add[j][k]]: return False
        zero = None
        for i in range(size):
            if all(add[i][j] == j for j in range(size)):
                zero = i
                break
        if zero is None: return False
        for i in range(size):
            if not any(add[i][j] == zero for j in range(size)): return False
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False
        for i in range(size):
            for j in range(size):
                for k in range(size):
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False
        return True

    def is_homomorphism(R_size, S_size, R_add, R_mul, S_add, S_mul, f):
        if len(f) != R_size: return False
        for i in range(R_size):
            if not isinstance(f[i], int) or not (0 <= f[i] < S_size): return False
            for j in range(R_size):
                if f[R_add[i][j]] != S_add[f[i]][f[j]]: return False
                if f[R_mul[i][j]] != S_mul[f[i]][f[j]]: return False
        return True

    try:
        h1 = is_ring(R_size, R_add, R_mul) and is_ring(S_size, S_add, S_mul) and is_homomorphism(R_size, S_size, R_add, R_mul, S_add, S_mul, f_map)
    except Exception:
        h1 = False

    def get_nilradical(size, add, mul):
        zero = None
        for i in range(size):
            if add[i][i] == i:
                zero = i
                break
                
        def get_ideal(x):
            ideal = {x}
            while True:
                new_ideal = set(ideal)
                for a in range(size):
                    for s in ideal:
                        new_ideal.add(mul[a][s])
                        new_ideal.add(mul[s][a])
                for s1 in ideal:
                    for s2 in ideal:
                        new_ideal.add(add[s1][s2])
                for s in ideal:
                    curr = s
                    for _ in range(size + 1):
                        new_ideal.add(curr)
                        if curr == zero:
                            break
                        curr = add[curr][s]
                if len(new_ideal) == len(ideal):
                    break
                ideal = new_ideal
            return ideal

        def is_nilpotent_ideal(ideal):
            if not ideal: return True
            current_power = set(ideal)
            for _ in range(size + 1):
                if all(e == zero for e in current_power):
                    return True
                products = set()
                for a in current_power:
                    for b in ideal:
                        products.add(mul[a][b])
                sum_closed = set(products)
                while True:
                    new_closed = set(sum_closed)
                    for s1 in sum_closed:
                        for s2 in sum_closed:
                            new_closed.add(add[s1][s2])
                    if len(new_closed) == len(sum_closed):
                        break
                    sum_closed = new_closed
                current_power = sum_closed
            return all(e == zero for e in current_power)

        nilradical = set()
        for i in range(size):
            if is_nilpotent_ideal(get_ideal(i)):
                nilradical.add(i)
        return nilradical

    try:
        if not h1:
            neg_q = False
        else:
            nil_R = get_nilradical(R_size, R_add, R_mul)
            nil_S = get_nilradical(S_size, S_add, S_mul)
            
            preimage = set()
            for i in range(R_size):
                if f_map[i] in nil_S:
                    preimage.add(i)
                    
            neg_q = not nil_R.issubset(preimage)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: f: R -> S is a ring homomorphism",
    "¬Q: The preimage of the nilradical of S under f does not contain the nilradical of R"
]

N_HYP = 1
NEG_Q_INDEX = 1