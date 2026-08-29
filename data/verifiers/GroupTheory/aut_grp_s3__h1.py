import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.combinatorics.permutations import Permutation

S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    try:
        E = list(witness.generate())
        n = len(E)
        if n == 1:
            return [True]
        M = [[E.index(x * y) for y in E] for x in E]
        g_idx = [E.index(g) for g in witness.generators]
        A = []
        for t in itertools.product(range(n), repeat=len(g_idx)):
            m = {g_idx[i]: t[i] for i in range(len(g_idx))}
            id_idx = E.index(witness.identity)
            if id_idx not in m:
                m[id_idx] = id_idx
            elif m[id_idx] != id_idx:
                continue
            q = list(m.keys())
            v = True
            h = 0
            while h < len(q) and v:
                c = q[h]
                h += 1
                for i in range(n):
                    if i in m:
                        p1, v1 = M[c][i], M[m[c]][m[i]]
                        if p1 in m:
                            if m[p1] != v1:
                                v = False
                                break
                        else:
                            m[p1] = v1
                            q.append(p1)
                        p2, v2 = M[i][c], M[m[i]][m[c]]
                        if p2 in m:
                            if m[p2] != v2:
                                v = False
                                break
                        else:
                            m[p2] = v2
                            q.append(p2)
            if v and len(m) == n and len(set(m.values())) == n:
                A.append(tuple(m[i] for i in range(n)))
        is_S3 = (len(A) == 6 and any(a[b[i]] != b[a[i]] for a in A for b in A for i in range(n)))
        return [not is_S3]
    except Exception:
        return [False]

CONDITION_LABELS = ["¬Q: Aut(G) is not isomorphic to S_3"]
N_HYP = 0
NEG_Q_INDEX = 0