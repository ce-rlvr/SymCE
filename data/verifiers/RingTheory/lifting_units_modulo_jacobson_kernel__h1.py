import itertools
import math
from functools import reduce

# Top-level setup
# We provide valid counterexample witnesses as dictionaries of Cayley tables.
# The conjecture fails because the hypothesis that R is a ring WITH IDENTITY was dropped.
# Without an identity in R, x cannot be a unit in R, even if f(x) is a unit in S.

# Counterexample 1: R is the ring of matrices [a b; 0 0] over Z/2Z. S is Z/2Z.
counterexample_witness = {
    "R_add": [[0, 1, 2, 3], [1, 0, 3, 2], [2, 3, 0, 1], [3, 2, 1, 0]],
    "R_mul": [[0, 0, 0, 0], [0, 1, 2, 3], [0, 0, 0, 0], [0, 1, 2, 3]],
    "S_add": [[0, 1], [1, 0]],
    "S_mul": [[0, 0], [0, 1]],
    "f": [0, 1, 0, 1],
    "x": 1
}

# Counterexample 2: R has zero multiplication, S is the zero ring.
trivial_counterexample = {
    "R_add": [[0, 1], [1, 0]],
    "R_mul": [[0, 0], [0, 0]],
    "S_add": [[0]],
    "S_mul": [[0]],
    "f": [0, 0],
    "x": 1
}

def is_ring(add, mul):
    n = len(add)
    if any(len(row) != n for row in add) or len(mul) != n or any(len(row) != n for row in mul):
        return False
    for i in range(n):
        for j in range(n):
            if not (0 <= add[i][j] < n) or not (0 <= mul[i][j] < n):
                return False
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]:
                return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]:
                    return False
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1:
        return False
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)):
            return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]:
                    return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]:
                    return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]:
                    return False
    return True

def get_zero(add):
    n = len(add)
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            return i
    return -1

def get_J_R(add, mul):
    n = len(add)
    zero = get_zero(add)
    neg = [-1] * n
    for i in range(n):
        for j in range(n):
            if add[i][j] == zero:
                neg[i] = j
                break
                
    def sub(a, b):
        return add[a][neg[b]]
        
    def circ(z, w):
        return sub(add[z][w], mul[z][w])
        
    rqr = []
    for z in range(n):
        is_rqr = False
        for w in range(n):
            if circ(z, w) == zero:
                is_rqr = True
                break
        rqr.append(is_rqr)
        
    J = []
    for x in range(n):
        if all(rqr[mul[x][y]] for y in range(n)):
            J.append(x)
    return J

def get_identity(mul):
    n = len(mul)
    for i in range(n):
        if all(mul[i][j] == j and mul[j][i] == j for j in range(n)):
            return i
    return -1

def is_unit(add, mul, u):
    ident = get_identity(mul)
    if ident == -1:
        return False
    n = len(mul)
    for v in range(n):
        if mul[u][v] == ident and mul[v][u] == ident:
            return True
    return False

def conditions(witness):
    try:
        if isinstance(witness, dict) and "R_add" in witness:
            R_add = witness["R_add"]
            R_mul = witness["R_mul"]
            S_add = witness["S_add"]
            S_mul = witness["S_mul"]
            f = witness["f"]
            x = witness["x"]
        elif hasattr(witness, "R_add"):
            R_add = witness.R_add
            R_mul = witness.R_mul
            S_add = witness.S_add
            S_mul = witness.S_mul
            f = witness.f
            x = witness.x
        elif isinstance(witness, tuple) and len(witness) == 4:
            R, S, f_map, x_val = witness
            R_add = []
            R_mul = []
            for a in R:
                row_add = []
                row_mul = []
                for b in R:
                    row_add.append(R.index(a + b))
                    row_mul.append(R.index(a * b))
                R_add.append(row_add)
                R_mul.append(row_mul)
            S_add = []
            S_mul = []
            for a in S:
                row_add = []
                row_mul = []
                for b in S:
                    row_add.append(S.index(a + b))
                    row_mul.append(S.index(a * b))
                S_add.append(row_add)
                S_mul.append(row_mul)
            if callable(f_map):
                f = [S.index(f_map(a)) for a in R]
            else:
                f = [S.index(f_map[a]) for a in R]
            x = R.index(x_val)
        else:
            return [False, False, False, False]
            
        # H1: f is a surjective ring homomorphism from R to S
        h1 = False
        if is_ring(R_add, R_mul) and is_ring(S_add, S_mul):
            if set(f) == set(range(len(S_add))):
                is_hom = True
                for i in range(len(R_add)):
                    for j in range(len(R_add)):
                        if f[R_add[i][j]] != S_add[f[i]][f[j]]:
                            is_hom = False
                        if f[R_mul[i][j]] != S_mul[f[i]][f[j]]:
                            is_hom = False
                h1 = is_hom
                
        # H2: ker f is contained in J(R)
        h2 = False
        if h1:
            zero_S = get_zero(S_add)
            ker_f = [i for i in range(len(R_add)) if f[i] == zero_S]
            J_R = get_J_R(R_add, R_mul)
            h2 = all(k in J_R for k in ker_f)
            
        # H3: f(x) is a unit in S
        h3 = False
        if h1:
            fx = f[x]
            h3 = is_unit(S_add, S_mul, fx)
            
        # Negated Conclusion: x is NOT a unit in R
        neg_q = False
        if is_ring(R_add, R_mul):
            neg_q = not is_unit(R_add, R_mul, x)
            
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: f is a surjective ring homomorphism from R to S",
    "H_2: the kernel of f is contained in the Jacobson radical of R",
    "H_3: f(x) is a unit in S",
    "¬Q: x is not a unit in R"
]

N_HYP = 3
NEG_Q_INDEX = 3