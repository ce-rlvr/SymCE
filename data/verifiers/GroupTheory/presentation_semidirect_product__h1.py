import sympy
from sympy.combinatorics.free_groups import free_group
from sympy.combinatorics.fp_groups import FpGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def is_valid_group(table):
    n = len(table)
    if any(len(row) != n for row in table): return False
    for i in range(n):
        if table[0][i] != i or table[i][0] != i: return False
    for i in range(n):
        has_inv = False
        for j in range(n):
            if table[i][j] == 0 and table[j][i] == 0:
                has_inv = True
                break
        if not has_inv: return False
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if table[table[i][j]][k] != table[i][table[j][k]]:
                    return False
    return True

def generates(elements, n, table):
    closure = set(elements)
    closure.add(0)
    added = True
    while added:
        added = False
        new_elements = set()
        for a in closure:
            for b in closure:
                c = table[a][b]
                if c not in closure:
                    new_elements.add(c)
        if new_elements:
            closure.update(new_elements)
            added = True
    return len(closure) == n

def eval_word(word, mapping, table):
    res = 0
    for gen, exp in word:
        val = mapping[gen]
        if exp == 0:
            continue
        elif exp > 0:
            step = val
            for _ in range(exp - 1):
                step = table[step][val]
            res = table[res][step]
        else:
            inv = 0
            for i in range(len(table)):
                if table[val][i] == 0 and table[i][val] == 0:
                    inv = i
                    break
            step = inv
            for _ in range(-exp - 1):
                step = table[step][inv]
            res = table[res][step]
    return res

def word_inv(word):
    return [(g, -e) for g, e in reversed(word)]

def check_fp_group_order(gens, rels, expected_order):
    if not gens:
        return expected_order == 1
    
    res = free_group(",".join(str(g) for g in gens))
    F = res[0]
    gen_map = {str(g): F.generators[i] for i, g in enumerate(gens)}
    
    F_rels = []
    for rel in rels:
        word = F.identity
        for g, e in rel:
            if e != 0:
                word = word * (gen_map[str(g)] ** e)
        F_rels.append(word)
    
    G = FpGroup(F, F_rels)
    try:
        return G.order() == expected_order
    except Exception:
        return False

def conditions(witness) -> list[bool]:
    try:
        N_table = witness['N_table']
        H_table = witness['H_table']
        X = witness['X']
        Y = witness['Y']
        S = witness['S']
        R = witness['R']
        phi = witness['phi']
        w = witness['w']
    except KeyError:
        return [False, False, False, False]

    if not set(X.keys()).isdisjoint(set(Y.keys())):
        return [False, False, False, False]

    def check_h1():
        if not is_valid_group(H_table): return False
        if not generates(list(Y.values()), len(H_table), H_table): return False
        for rel in S:
            if eval_word(rel, Y, H_table) != 0: return False
        if not check_fp_group_order(list(Y.keys()), S, len(H_table)): return False
        return True

    def check_h2():
        if not is_valid_group(N_table): return False
        if len(phi) != len(H_table): return False
        n_len = len(N_table)
        for h in range(len(H_table)):
            p = phi[h]
            if len(p) != n_len or set(p) != set(range(n_len)): return False
            for a in range(n_len):
                for b in range(n_len):
                    if p[N_table[a][b]] != N_table[p[a]][p[b]]: return False
        for h1 in range(len(H_table)):
            for h2 in range(len(H_table)):
                h3 = H_table[h1][h2]
                for a in range(n_len):
                    if phi[h3][a] != phi[h1][phi[h2][a]]: return False
        return True

    def check_h3():
        for y_name, y_val in Y.items():
            for x_name, x_val in X.items():
                word = w.get((y_name, x_name))
                if word is None: return False
                if eval_word(word, X, N_table) != phi[y_val][x_val]: return False
        return True

    def check_neg_q():
        expected_order = len(N_table) * len(H_table)
        gens = list(X.keys()) + list(Y.keys())
        rels = list(R) + list(S)
        for y_name in Y.keys():
            for x_name in X.keys():
                word = w.get((y_name, x_name))
                if word is None: return False
                rel = [(y_name, 1), (x_name, 1), (y_name, -1)] + word_inv(word)
                rels.append(rel)
        try:
            matches = check_fp_group_order(gens, rels, expected_order)
            return not matches
        except Exception:
            return True

    try:
        h1 = check_h1()
    except Exception:
        h1 = False

    try:
        h2 = check_h2()
    except Exception:
        h2 = False

    try:
        h3 = check_h3()
    except Exception:
        h3 = False

    try:
        nq = check_neg_q()
    except Exception:
        nq = False

    return [h1, h2, h3, nq]

CONDITION_LABELS = [
    "H_1: H is a group generated by a set Y with defining relations S",
    "H_2: phi: H -> Aut(N) is a group homomorphism",
    "H_3: For each x in X and y in Y, w_{y,x} is a word in X representing phi_y(x) in N",
    "not Q: The presentation does NOT define the external semidirect product N rtimes_phi H"
]

N_HYP = 3
NEG_Q_INDEX = 3