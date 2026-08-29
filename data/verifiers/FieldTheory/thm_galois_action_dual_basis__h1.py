import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        T_raw, E_raw, E_star_raw, G_raw = witness
        T = sp.Matrix(T_raw)
        E = [sp.Matrix(e) for e in E_raw]
        E_star = [sp.Matrix(e) for e in E_star_raw]
        G_matrices = [sp.Matrix(g) for g in G_raw]
    except Exception:
        return [False, False, False, False]

    try:
        h1 = T.is_square and T.det() != 0
    except Exception:
        h1 = False

    try:
        E_mat = sp.Matrix.hstack(*E)
        h2 = E_mat.is_square and E_mat.det() != 0
    except Exception:
        h2 = False

    try:
        n = len(E)
        h3 = True
        for i in range(n):
            for j in range(n):
                val = (E[i].T * T * E_star[j])[0, 0]
                expected = 1 if i == j else 0
                if sp.simplify(val - expected) != 0:
                    h3 = False
                    break
            if not h3:
                break
    except Exception:
        h3 = False

    try:
        n = len(E)
        conclusion_holds = True
        for sigma in G_matrices:
            for i in range(n):
                for j in range(n):
                    f_i = sigma * E[i]
                    g_j = sigma * E_star[j]
                    val = (f_i.T * T * g_j)[0, 0]
                    expected = 1 if i == j else 0
                    if sp.simplify(val - expected) != 0:
                        conclusion_holds = False
                        break
                if not conclusion_holds:
                    break
            if not conclusion_holds:
                break
        neg_q = not conclusion_holds
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: The trace pairing is non-degenerate",
    "H_2: {e_1, ..., e_n} is a K-basis for L",
    "H_3: {e_1^*, ..., e_n^*} is the dual basis of L with respect to the trace pairing",
    "¬Q: There exists sigma in G and i such that sigma(e_i^*) != (sigma(e_i))^*"
]

N_HYP = 3
NEG_Q_INDEX = 3