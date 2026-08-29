import itertools

def conditions(witness) -> list[bool]:
    try:
        R, add, mul, M = witness
        R_set = set(R)
        M_set = set(M)
    except Exception:
        return [False, False]

    def is_ring():
        if any(add[i][j] != add[j][i] for i in R for j in R): return False
        if any(add[add[i][j]][k] != add[i][add[j][k]] for i in R for j in R for k in R): return False
        zeros = [e for e in R if all(add[e][x] == x for x in R)]
        if not zeros: return False
        z = zeros[0]
        if any(not any(add[x][y] == z for y in R) for x in R): return False
        if any(mul[mul[i][j]][k] != mul[i][mul[j][k]] for i in R for j in R for k in R): return False
        if any(mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]] for i in R for j in R for k in R): return False
        if any(mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]] for i in R for j in R for k in R): return False
        return True

    def is_ideal(I_set):
        if not I_set: return False
        z = next((e for e in R if all(add[e][x] == x for x in R)), None)
        if z not in I_set: return False
        if any(add[i][j] not in I_set for i in I_set for j in I_set): return False
        if any(next((y for y in R if add[x][y] == z), None) not in I_set for x in I_set): return False
        if any(mul[i][r] not in I_set for i in I_set for r in R): return False
        if any(mul[r][i] not in I_set for i in I_set for r in R): return False
        return True

    all_ideals = []
    try:
        if is_ring():
            for k in range(1, len(R) + 1):
                for sub in itertools.combinations(R, k):
                    if is_ideal(set(sub)):
                        all_ideals.append(set(sub))
    except Exception:
        pass

    try:
        h1 = False
        if is_ring() and is_ideal(M_set) and M_set != R_set:
            maximal = True
            for I in all_ideals:
                if M_set.issubset(I) and I != M_set and I != R_set:
                    maximal = False
                    break
            h1 = maximal
    except Exception:
        h1 = False

    try:
        neg_q = False
        if is_ring() and is_ideal(M_set):
            for A in all_ideals:
                for B in all_ideals:
                    if not A.issubset(M_set) and not B.issubset(M_set):
                        if all(mul[a][b] in M_set for a in A for b in B):
                            neg_q = True
                            break
                if neg_q:
                    break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: M is a maximal ideal of R",
    "¬Q: M is not a prime ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1