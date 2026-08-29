import math
import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import itertools
import functools

# Top-level setup
# (No specific named objects required for Real Analysis metric space witnesses)

def get_matrix(witness):
    if isinstance(witness, list):
        return witness
    if hasattr(witness, 'tolist'):
        return witness.tolist()
    if isinstance(witness, dict):
        keys = list(witness.keys())
        if not keys:
            return []
        if all(isinstance(k, tuple) and len(k) == 2 for k in keys):
            elements = list(set([k[0] for k in keys] + [k[1] for k in keys]))
            n = len(elements)
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            mat = [[0.0] * n for _ in range(n)]
            for (u, v), val in witness.items():
                mat[elem_to_idx[u]][elem_to_idx[v]] = float(val)
            return mat
        else:
            elements = list(witness.keys())
            n = len(elements)
            mat = [[0.0] * n for _ in range(n)]
            for i, u in enumerate(elements):
                for j, v in enumerate(elements):
                    mat[i][j] = float(witness[u][v])
            return mat
    if hasattr(witness, 'd') and hasattr(witness, 'elements'):
        elements = witness.elements
        n = len(elements)
        return [[float(witness.d(elements[i], elements[j])) for j in range(n)] for i in range(n)]
    return None

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        d = get_matrix(witness)
        if d is not None and len(d) > 0:
            n = len(d)
            h1 = True
            for i in range(n):
                if len(d[i]) != n:
                    h1 = False
                    break
                if abs(float(d[i][i])) > 1e-7:
                    h1 = False
                    break
                for j in range(n):
                    if float(d[i][j]) < -1e-7:
                        h1 = False
                        break
                    if abs(float(d[i][j]) - float(d[j][i])) > 1e-7:
                        h1 = False
                        break
                    if i != j and float(d[i][j]) < 1e-7:
                        h1 = False
                        break
                    for k in range(n):
                        if float(d[i][j]) > float(d[i][k]) + float(d[k][j]) + 1e-7:
                            h1 = False
                            break
                if not h1:
                    break
    except Exception:
        h1 = False

    try:
        if h1:
            n = len(d)
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        for l in range(n):
                            diff = abs(float(d[i][j]) - float(d[k][l]))
                            # Check if Lipschitz constant > 1 for the standard max product metric
                            if diff > max(float(d[i][k]), float(d[j][l])) + 1e-7:
                                neg_q = True
                                break
                        if neg_q: break
                    if neg_q: break
                if neg_q: break
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d) is a metric space",
    "¬Q: The metric function d is not globally Lipschitz continuous with constant 1"
]

N_HYP = 1
NEG_Q_INDEX = 1