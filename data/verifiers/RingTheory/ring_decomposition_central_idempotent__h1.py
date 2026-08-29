import itertools
import math

# Top-level setup
# The witness is expected to be a tuple: (n, add_table, mul_table, e)
# where n is the size of the ring, add_table and mul_table are n x n lists of lists
# representing the addition and multiplication operations, and e is an integer 0 <= e < n.

def conditions(witness):
    try:
        n, add_table, mul_table, e = witness
        n = int(n)
        e = int(e)
    except Exception:
        return [False, False, False, False, False]

    # H_1: R is a valid ring (rng)
    def is_rng():
        if n <= 0: return False
        if len(add_table) != n or len(mul_table) != n: return False
        for row in add_table:
            if len(row) != n: return False
        for row in mul_table:
            if len(row) != n: return False
            
        # Closure
        for i in range(n):
            for j in range(n):
                if not (0 <= add_table[i][j] < n): return False
                if not (0 <= mul_table[i][j] < n): return False

        # Addition commutativity
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False

        # Addition associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return False

        # Additive identity
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False

        # Additive inverses
        for i in range(n):
            has_inv = False
            for j in range(n):
                if add_table[i][j] == zero:
                    has_inv = True
                    break
            if not has_inv: return False

        # Multiplication associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return False

        # Distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return False
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return False

        return True

    try:
        h1 = is_rng()
    except Exception:
        h1 = False

    # H_2: e is an element of R
    try:
        h2 = (0 <= e < n)
    except Exception:
        h2 = False

    # H_3: e is idempotent (e^2 = e)
    try:
        h3 = (mul_table[e][e] == e)
    except Exception:
        h3 = False

    # H_4: e is central (ex = xe for all x in R)
    try:
        h4 = all(mul_table[e][x] == mul_table[x][e] for x in range(n))
    except Exception:
        h4 = False

    # ¬Q: R is not isomorphic to eR x (1-e)R
    # The theorem holds unconditionally for any ring WITH a multiplicative identity.
    # The conjecture fails (and thus ¬Q is True) iff R lacks a multiplicative identity,
    # which makes the expression "1-e" undefined and the conclusion invalid.
    try:
        identity = None
        for i in range(n):
            is_id = True
            for j in range(n):
                if mul_table[i][j] != j or mul_table[j][i] != j:
                    is_id = False
                    break
            if is_id:
                identity = i
                break
        
        q = (identity is not None)
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: R is a valid ring (rng)",
    "H_2: e is an element of R",
    "H_3: e is idempotent (e^2 = e)",
    "H_4: e is central (ex = xe for all x in R)",
    "¬Q: R is not isomorphic to eR x (1-e)R (e.g., 1-e is undefined because R lacks an identity)"
]

N_HYP = 4
NEG_Q_INDEX = 4