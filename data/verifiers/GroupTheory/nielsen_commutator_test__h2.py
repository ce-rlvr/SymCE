import sympy
from sympy.combinatorics import free_group

F2, a, b = free_group('a, b')

def get_letters(w):
    letters = []
    for gen_idx, power in w.array_form:
        sign = 1 if power > 0 else -1
        for _ in range(abs(power)):
            letters.append((gen_idx, sign))
    return letters

def cyclic_reduction(letters):
    l = list(letters)
    while len(l) >= 2 and l[0][0] == l[-1][0] and l[0][1] == -l[-1][1]:
        l = l[1:-1]
    return l

def is_conjugate(w1, w2):
    l1 = cyclic_reduction(get_letters(w1))
    l2 = cyclic_reduction(get_letters(w2))
    if len(l1) != len(l2):
        return False
    if len(l1) == 0:
        return True
    for shift in range(len(l1)):
        if l1 == l2[shift:] + l2[:shift]:
            return True
    return False

def is_free_basis(u, v, F_2):
    gen_a, gen_b = F_2.generators
    comm_ab = gen_a**-1 * gen_b**-1 * gen_a * gen_b
    comm_uv = u**-1 * v**-1 * u * v
    return is_conjugate(comm_uv, comm_ab) or is_conjugate(comm_uv, comm_ab**-1)

def conditions(witness):
    try:
        if len(witness) == 4:
            u, v, x, y = witness
            F_2 = u.group
        elif len(witness) == 5:
            F_2, u, v, x, y = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (type(F_2).__name__ == 'FreeGroup' and len(F_2.generators) == 2)
    except Exception:
        h1 = False
        
    try:
        h2 = (u.group == F_2) and (v.group == F_2) and (x.group == F_2) and (y.group == F_2)
    except Exception:
        h2 = False
        
    try:
        comm_uv = u**-1 * v**-1 * u * v
        comm_xy = x**-1 * y**-1 * x * y
        
        basis_uv = is_free_basis(u, v, F_2)
        conj_xy = is_conjugate(comm_uv, comm_xy) or is_conjugate(comm_uv, comm_xy**-1)
        
        neg_q = (basis_uv != conj_xy)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: F2 is a free group of rank 2",
    "H_2: u and v are elements of F2",
    "¬Q: The conclusion fails (u, v is a free basis iff comm(u, v) is conjugate to comm(x, y) or its inverse)"
]

N_HYP = 2
NEG_Q_INDEX = 2