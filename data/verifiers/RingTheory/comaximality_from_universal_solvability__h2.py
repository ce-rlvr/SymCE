import itertools
import sympy
from sympy import Rational, Integer, Symbol
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: For every a, b in R, there exists x in R such that x = a mod I and x = b mod J",
    "¬Q: The ideals I and J are not comaximal"
]
N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        if isinstance(witness[0], (int, Integer)):
            n, add_table, mul_table, I_elements, J_elements = witness
            n = int(n)
            I = list(I_elements)
            J = list(J_elements)
            if any(val < 0 or val >= n for val in I) or any(val < 0 or val >= n for val in J):
                return [False] * 3
        else:
            elements, add_func, mul_func, I_elements, J_elements = witness
            n = len(elements)
            def get_idx(val):
                for i, e in enumerate(elements):
                    if e == val: return i
                return -1
            add_table = [[-1]*n for _ in range(n)]
            mul_table = [[-1]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    add_table[i][j] = get_idx(add_func(elements[i], elements[j]))
                    mul_table[i][j] = get_idx(mul_func(elements[i], elements[j]))
            I = [get_idx(val) for val in I_elements]
            J = [get_idx(val) for val in J_elements]
            if any(val == -1 for val in I) or any(val == -1 for val in J):
                return [False] * 3
            for row in add_table:
                if -1 in row: return [False] * 3
            for row in mul_table:
                if -1 in row: return [False] * 3
    except Exception:
        return [False] * 3

    # H1: R is a ring
    h1 = True
    id_add = -1
    try:
        if len(add_table) != n or len(mul_table) != n:
            h1 = False
        else:
            for e in range(n):
                if all(add_table[e][val] == val and add_table[val][e] == val for val in range(n)):
                    id_add = e
                    break
            if id_add == -1:
                h1 = False
            
            if h1:
                for a in range(n):
                    if not any(add_table[a][b] == id_add and add_table[b][a] == id_add for b in range(n)):
                        h1 = False
                        break
                for a, b in itertools.product(range(n), repeat=2):
                    if add_table[a][b] != add_table[b][a]:
                        h1 = False
                        break
                for a, b, c in itertools.product(range(n), repeat=3):
                    if add_table[add_table[a][b]][c] != add_table[a][add_table[b][c]]:
                        h1 = False
                        break
                    if mul_table[mul_table[a][b]][c] != mul_table[a][mul_table[b][c]]:
                        h1 = False
                        break
                    if mul_table[a][add_table[b][c]] != add_table[mul_table[a][b]][mul_table[a][c]]:
                        h1 = False
                        break
                    if mul_table[add_table[a][b]][c] != add_table[mul_table[a][c]][mul_table[b][c]]:
                        h1 = False
                        break
    except Exception:
        h1 = False

    # H2: For every a, b in R, there exists x in R such that x = a mod I and x = b mod J
    h2 = False
    try:
        if h1:
            h2 = True
            I_set = set(I)
            J_set = set(J)
            for a in range(n):
                for b in range(n):
                    a_I = {add_table[a][i] for i in I_set}
                    b_J = {add_table[b][j] for j in J_set}
                    if not a_I.intersection(b_J):
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: The ideals I and J are not comaximal
    neg_q = False
    try:
        if h1:
            def is_ideal(S):
                if not S: return False
                if id_add not in S: return False
                for x_val in S:
                    for y_val in S:
                        if add_table[x_val][y_val] not in S: return False
                    inv_x = -1
                    for y_val in range(n):
                        if add_table[x_val][y_val] == id_add:
                            inv_x = y_val
                            break
                    if inv_x not in S: return False
                    for r in range(n):
                        if mul_table[r][x_val] not in S: return False
                        if mul_table[x_val][r] not in S: return False
                return True

            I_set = set(I)
            J_set = set(J)
            I_is_ideal = is_ideal(I_set)
            J_is_ideal = is_ideal(J_set)
            I_plus_J = {add_table[i][j] for i in I_set for j in J_set}
            
            if not (I_is_ideal and J_is_ideal and len(I_plus_J) == n):
                neg_q = True
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]