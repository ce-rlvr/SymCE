import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: I is a nilpotent ideal of R",
    "H_2: e_bar is an idempotent element in R/I",
    "¬Q: There is no idempotent element e in R such that e + I = e_bar"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            n = witness['n']
            add = witness['add']
            mul = witness['mul']
            I = witness['I']
            e_bar = witness['e_bar']
        else:
            n, add, mul, I, e_bar = witness
            
        if not (isinstance(n, int) and n > 0):
            return [False, False, False]
            
        for a in range(n):
            for b in range(n):
                if add[a][b] != add[b][a]:
                    return [False, False, False]
                for c in range(n):
                    if add[add[a][b]][c] != add[a][add[b][c]]:
                        return [False, False, False]
                    if mul[a][add[b][c]] != add[mul[a][b]][mul[a][c]]:
                        return [False, False, False]
                    if mul[add[a][b]][c] != add[mul[a][c]][mul[b][c]]:
                        return [False, False, False]
                        
        zeros_list = [z for z in range(n) if all(add[x][z] == x for x in range(n))]
        if not zeros_list:
            return [False, False, False]
        zero = zeros_list[0]
        
        for a in range(n):
            if not any(add[a][b] == zero for b in range(n)):
                return [False, False, False]

        h1 = True
        if not I or zero not in I:
            h1 = False
        else:
            for i in I:
                for j in I:
                    if add[i][j] not in I:
                        h1 = False
            for r in range(n):
                for i in I:
                    if mul[r][i] not in I:
                        h1 = False
                    if mul[i][r] not in I:
                        h1 = False
            if h1:
                current_I = set(I)
                is_nilpotent = False
                for _ in range(n + 1):
                    if all(x == zero for x in current_I):
                        is_nilpotent = True
                        break
                    next_gens = set()
                    for x in current_I:
                        for y in I:
                            next_gens.add(mul[x][y])
                            next_gens.add(mul[y][x])
                    next_I = set(next_gens)
                    added = True
                    while added:
                        added = False
                        for a in list(next_I):
                            for b in list(next_I):
                                s = add[a][b]
                                if s not in next_I:
                                    next_I.add(s)
                                    added = True
                    current_I = next_I
                if not is_nilpotent:
                    h1 = False

        h2 = False
        if isinstance(e_bar, int) and 0 <= e_bar < n:
            e_bar_sq = mul[e_bar][e_bar]
            coset = set(add[e_bar][i] for i in I)
            if e_bar_sq in coset:
                h2 = True

        neg_q = True
        if isinstance(e_bar, int) and 0 <= e_bar < n:
            coset = set(add[e_bar][i] for i in I)
            for e in coset:
                if mul[e][e] == e:
                    neg_q = False
                    break
        else:
            neg_q = False

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]