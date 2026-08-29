import sympy
from sympy.combinatorics import free_group

# Top-level setup
F, x, y, z = free_group("x, y, z")
FreeGroupType = type(F)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                F_wit, u, v = witness
            elif len(witness) == 2:
                u, v = witness
                F_wit = getattr(u, 'group', None)
            else:
                F_wit, u, v = None, None, None
        else:
            F_wit, u, v = None, None, None
            
        h1 = isinstance(F_wit, FreeGroupType) and hasattr(u, 'group') and u.group == F_wit and hasattr(v, 'group') and v.group == F_wit
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            def get_letters(w):
                letters = []
                for idx, exp in w.array_form:
                    sign = 1 if exp > 0 else -1
                    for _ in range(abs(exp)):
                        letters.append((idx, sign))
                return letters

            def cyclic_reduction_letters(letters):
                l = list(letters)
                while len(l) >= 2 and l[0][0] == l[-1][0] and l[0][1] == -l[-1][1]:
                    l.pop(0)
                    l.pop(-1)
                return l

            def is_cyclic_permutation(l1, l2):
                if len(l1) != len(l2):
                    return False
                if len(l1) == 0:
                    return True
                n = len(l1)
                for i in range(n):
                    if l1 == l2[i:] + l2[:i]:
                        return True
                return False

            u_letters = get_letters(u)
            v_letters = get_letters(v)

            u_reduced = cyclic_reduction_letters(u_letters)
            v_reduced = cyclic_reduction_letters(v_letters)

            are_conjugate = is_cyclic_permutation(u_reduced, v_reduced)
            is_cyclic_perm = is_cyclic_permutation(u_letters, v_letters)

            neg_q = (are_conjugate != is_cyclic_perm)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: F is a free group on a set X",
    "¬Q: Conjugacy of u and v is not equivalent to u being a cyclic permutation of v"
]

N_HYP = 1
NEG_Q_INDEX = 1