import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import math
import itertools
import functools

# Top-level setup
S3 = sympy.combinatorics.named_groups.SymmetricGroup(3)
S4 = sympy.combinatorics.named_groups.SymmetricGroup(4)
A4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
D4 = sympy.combinatorics.named_groups.DihedralGroup(4)
C4 = sympy.combinatorics.named_groups.CyclicGroup(4)
V4 = sympy.combinatorics.named_groups.AlternatingGroup(4)
Z2 = sympy.combinatorics.named_groups.CyclicGroup(2)
Z3 = sympy.combinatorics.named_groups.CyclicGroup(3)
Z4 = sympy.combinatorics.named_groups.CyclicGroup(4)
Z6 = sympy.combinatorics.named_groups.CyclicGroup(6)
trivial = sympy.combinatorics.named_groups.CyclicGroup(1)

I2 = sympy.matrices.eye(2)
I3 = sympy.matrices.eye(3)
O2 = sympy.matrices.zeros(2, 2)
O3 = sympy.matrices.zeros(3, 3)

def conditions(witness):
    # H1: (X, d) is a connected space
    try:
        if hasattr(witness, 'is_connected'):
            h1 = witness.is_connected() if callable(witness.is_connected) else witness.is_connected
        elif hasattr(witness, 'connected'):
            h1 = witness.connected() if callable(witness.connected) else witness.connected
        elif hasattr(witness, 'topology'):
            X_list = list(witness.X)
            open_sets = []
            for u in witness.topology:
                open_sets.append([x for x in X_list if x in u])
            
            h1 = True
            for u in open_sets:
                if len(u) > 0 and len(u) < len(X_list):
                    comp = [x for x in X_list if x not in u]
                    comp_is_open = False
                    for v in open_sets:
                        if len(v) == len(comp) and all(cx in v for cx in comp):
                            comp_is_open = True
                            break
                    if comp_is_open:
                        h1 = False
                        break
        else:
            h1 = False
    except Exception:
        h1 = False

    # H2: epsilon is a strictly positive real number
    try:
        h2 = float(witness.epsilon) > 0
    except Exception:
        h2 = False

    # H3: x and y are points in X
    try:
        X_list = list(witness.X)
        h3 = (witness.x in X_list) and (witness.y in X_list)
    except Exception:
        h3 = False

    # neg_Q: There is NO finite sequence of points forming an epsilon-chain
    try:
        if hasattr(witness, 'has_epsilon_chain'):
            if callable(witness.has_epsilon_chain):
                found = witness.has_epsilon_chain(witness.x, witness.y, witness.epsilon)
            else:
                found = witness.has_epsilon_chain
        else:
            reachable = [witness.x]
            queue = [witness.x]
            found = False
            max_iters = 10000
            iters = 0
            
            def get_d(u, v):
                if callable(witness.d):
                    return witness.d(u, v)
                elif isinstance(witness.d, dict):
                    if (u, v) in witness.d:
                        return witness.d[(u, v)]
                    else:
                        return float('inf')
                else:
                    return witness.d[u][v]

            while queue and iters < max_iters:
                curr = queue.pop(0)
                if curr == witness.y:
                    found = True
                    break
                for node in witness.X:
                    if node not in reachable:
                        if bool(get_d(curr, node) < witness.epsilon):
                            reachable.append(node)
                            queue.append(node)
                iters += 1
            
        neg_q = not found
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: (X, d) is a connected space",
    "H_2: epsilon is a strictly positive real number",
    "H_3: x and y are points in X",
    "¬Q: There is no finite epsilon-chain between x and y"
]

N_HYP = 3
NEG_Q_INDEX = 3