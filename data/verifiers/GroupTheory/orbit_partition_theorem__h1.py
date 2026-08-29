import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False, False]
        X, G = witness
    except Exception:
        return [False, False, False, False]

    X_list = []
    # H1: X is a set
    try:
        H1 = isinstance(X, (list, tuple, set))
        if H1:
            X_list = list(X)
            unique = True
            for i in range(len(X_list)):
                for j in range(i + 1, len(X_list)):
                    if X_list[i] == X_list[j]:
                        unique = False
                        break
                if not unique:
                    break
            H1 = unique
    except Exception:
        H1 = False

    G_list = []
    # H2: G acts on X
    try:
        H2 = True
        if not hasattr(G, '__iter__'):
            H2 = False
        elif not H1:
            H2 = False
        else:
            G_list = list(G)
            for g in G_list:
                for x in X_list:
                    if isinstance(g, dict):
                        if x not in g:
                            H2 = False
                            break
                        y = g[x]
                    elif callable(g):
                        try:
                            y = g(x)
                        except Exception:
                            H2 = False
                            break
                    elif isinstance(g, (list, tuple)):
                        if not isinstance(x, int) or x < 0 or x >= len(g):
                            H2 = False
                            break
                        y = g[x]
                    else:
                        try:
                            y = g * x
                        except Exception:
                            H2 = False
                            break
                    
                    found = False
                    for x_elem in X_list:
                        if y == x_elem:
                            found = True
                            break
                    if not found:
                        H2 = False
                        break
                if not H2:
                    break
    except Exception:
        H2 = False

    # H3: Relation ~ is defined such that x ~ y if there exists g in G such that g.x = y
    # This is a definitional hypothesis, so it holds as long as H1 and H2 hold.
    H3 = H1 and H2

    # neg_Q: The relation ~ is NOT an equivalence relation on X
    try:
        if not (H1 and H2):
            neg_Q = False
        else:
            sim = {i: set() for i in range(len(X_list))}
            for i, x in enumerate(X_list):
                for g in G_list:
                    if isinstance(g, dict):
                        y = g[x]
                    elif callable(g):
                        y = g(x)
                    elif isinstance(g, (list, tuple)):
                        y = g[x]
                    else:
                        y = g * x
                    
                    y_idx = -1
                    for j, x_elem in enumerate(X_list):
                        if y == x_elem:
                            y_idx = j
                            break
                    if y_idx != -1:
                        sim[i].add(y_idx)
            
            is_equiv = True
            n = len(X_list)
            
            # Check Reflexivity
            for i in range(n):
                if i not in sim[i]:
                    is_equiv = False
                    break
                    
            # Check Symmetry
            if is_equiv:
                for i in range(n):
                    for j in sim[i]:
                        if i not in sim[j]:
                            is_equiv = False
                            break
                    if not is_equiv:
                        break
                        
            # Check Transitivity
            if is_equiv:
                for i in range(n):
                    for j in sim[i]:
                        for k in sim[j]:
                            if k not in sim[i]:
                                is_equiv = False
                                break
                        if not is_equiv:
                            break
                    if not is_equiv:
                        break
                        
            neg_Q = not is_equiv
    except Exception:
        neg_Q = False

    return [H1, H2, H3, neg_Q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: Relation ~ is defined by the action of G",
    "¬Q: The relation ~ is not an equivalence relation"
]

N_HYP = 3
NEG_Q_INDEX = 3