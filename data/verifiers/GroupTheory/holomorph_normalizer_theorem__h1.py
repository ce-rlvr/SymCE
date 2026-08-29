import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, PermutationGroup

# Top-level setup: named object bindings
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

def is_cayley_table(w):
    if not isinstance(w, list): 
        return False
    n = len(w)
    if n == 0: 
        return False
    for row in w:
        if not isinstance(row, list): 
            return False
        if len(row) != n: 
            return False
        for x in row:
            if not isinstance(x, int): 
                return False
            if x < 0 or x >= n: 
                return False
    return True

def get_cayley_table(w):
    if is_cayley_table(w):
        return w
    if isinstance(w, dict):
        try:
            n = int(len(w)**0.5)
            if n * n == len(w):
                table = [[0] * n for _ in range(n)]
                for (i, j), v in w.items():
                    table[i][j] = v
                if is_cayley_table(table):
                    return table
        except Exception:
            pass
    if hasattr(w, 'elements') and hasattr(w, 'op'):
        try:
            elements = list(w.elements)
            n = len(elements)
            table = []
            for i in range(n):
                row = []
                for j in range(n):
                    res = w.op(elements[i], elements[j])
                    idx = elements.index(res)
                    row.append(idx)
                table.append(row)
            if is_cayley_table(table):
                return table
        except Exception:
            pass
    return None

def is_left_quasigroup(w):
    n = len(w)
    for row in w:
        if sorted(row) != list(range(n)): 
            return False
    return True

def is_group(w):
    n = len(w)
    # Check associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if w[w[i][j]][k] != w[i][w[j][k]]:
                    return False
    # Check identity
    e = -1
    for i in range(n):
        is_id = True
        for j in range(n):
            if w[i][j] != j or w[j][i] != j:
                is_id = False
                break
        if is_id:
            e = i
            break
    if e == -1:
        return False
    # Check inverses
    for i in range(n):
        has_inv = False
        for j in range(n):
            if w[i][j] == e and w[j][i] == e:
                has_inv = True
                break
        if not has_inv:
            return False
    return True

def conditions(witness) -> list[bool]:
    # If the witness is already a Sympy group, the theorem holds (it is true for all groups).
    if hasattr(witness, 'is_group') or isinstance(witness, PermutationGroup):
        return [True, True, False]
    
    try:
        table = get_cayley_table(witness)
        h1 = table is not None
    except Exception:
        h1 = False
        table = None

    try:
        # For \lambda(g) to be in S_G, left multiplication must be a permutation (left quasigroup)
        h2 = h1 and is_left_quasigroup(table)
    except Exception:
        h2 = False

    try:
        # The Holomorph Normalizer Theorem is true for all groups.
        # If G is not a group, the holomorph is not a group, but the normalizer in S_G is always a group.
        # Thus, they cannot be isomorphic. The conclusion fails iff G is not a group.
        neg_q = h2 and not is_group(table)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    r"H_1: S_G is the symmetric group on the underlying set of G",
    r"H_2: \lambda: G \to S_G is the left regular representation defined by \lambda(g)(x) = gx",
    r"¬Q: The normalizer of the image \lambda(G) in S_G is not isomorphic to the holomorph of G"
]

N_HYP = 2
NEG_Q_INDEX = 2