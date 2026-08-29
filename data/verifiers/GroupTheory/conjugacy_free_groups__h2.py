import sympy
from sympy.combinatorics import free_group

# Top-level setup
F, x, y = free_group('x, y')

def to_letters(w):
    letters = []
    for gen, exp in w.array_form:
        sign = 1 if exp > 0 else -1
        letters.extend([(gen, sign)] * abs(exp))
    return letters

def cyclically_reduce(w):
    let = to_letters(w)
    while len(let) > 1:
        if let[0][0] == let[-1][0] and let[0][1] == -let[-1][1]:
            let = let[1:-1]
        else:
            break
    return let

def are_conjugate(u, v):
    if u.group != v.group: 
        return False
    cr_u = cyclically_reduce(u)
    cr_v = cyclically_reduce(v)
    if len(cr_u) != len(cr_v):
        return False
    if len(cr_u) == 0:
        return True
    double_v = cr_v + cr_v
    n = len(cr_u)
    for i in range(n):
        if double_v[i:i+n] == cr_u:
            return True
    return False

def is_cyclic_permutation(u, v):
    let_u = to_letters(u)
    let_v = to_letters(v)
    if len(let_u) != len(let_v):
        return False
    if len(let_u) == 0:
        return True
    double_v = let_v + let_v
    n = len(let_u)
    for i in range(n):
        if double_v[i:i+n] == let_u:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        u, v = witness
        H1 = hasattr(u, 'group') and hasattr(v, 'group') and type(u.group).__name__ == 'FreeGroup' and u.group == v.group
    except Exception:
        H1 = False

    try:
        conj = are_conjugate(u, v)
        cyclic = is_cyclic_permutation(u, v)
        neg_Q = (conj != cyclic)
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: F is a free group and u, v are elements of F",
    "¬Q: u and v are conjugate in F if and only if u is a cyclic permutation of v (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1