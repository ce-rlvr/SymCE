import sympy
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _unique_elements(lst):
    res = []
    for item in lst:
        if item not in res:
            res.append(item)
    return res

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 5:
                A, X, Y, act_X, act_Y = witness
            elif len(witness) == 3:
                A, X, Y = witness
                act_X = lambda a, x: a(x)
                act_Y = lambda a, y: a(y)
            else:
                return [False, False, False, False]
        else:
            A = witness.A
            X = witness.X
            Y = witness.Y
            act_X = getattr(witness, 'act_X', lambda a, x: a(x))
            act_Y = getattr(witness, 'act_Y', lambda a, y: a(y))
    except Exception:
        return [False, False, False, False]

    # H1: A is a finite group
    try:
        if hasattr(A, 'elements'):
            A_list_h1 = list(A.elements)
        else:
            A_list_h1 = list(A)
        n = len(A_list_h1)
        h1 = (n > 0)
        if h1:
            for a in A_list_h1:
                for b in A_list_h1:
                    if (a * b) not in A_list_h1:
                        h1 = False
                        break
                if not h1: break
            
            if h1:
                id_elements = [e for e in A_list_h1 if all(e * a == a and a * e == a for a in A_list_h1)]
                if not id_elements:
                    h1 = False
                else:
                    e_id = id_elements[0]
                    for a in A_list_h1:
                        if not any(a * b == e_id and b * a == e_id for b in A_list_h1):
                            h1 = False
                            break
    except Exception:
        h1 = False

    # H2: A acts on both X and Y
    try:
        if hasattr(A, 'elements'):
            A_list_h2 = list(A.elements)
        else:
            A_list_h2 = list(A)
            
        X_list_h2 = _unique_elements(list(X))
        Y_list_h2 = _unique_elements(list(Y))
        
        h2 = True
        id_elements = [e for e in A_list_h2 if all(e * a == a and a * e == a for a in A_list_h2)]
        if not id_elements:
            h2 = False
        else:
            e_id = id_elements[0]
            for a in A_list_h2:
                for x in X_list_h2:
                    if act_X(a, x) not in X_list_h2: h2 = False
                for y in Y_list_h2:
                    if act_Y(a, y) not in Y_list_h2: h2 = False
            
            if h2:
                for x in X_list_h2:
                    if act_X(e_id, x) != x: h2 = False
                for y in Y_list_h2:
                    if act_Y(e_id, y) != y: h2 = False
            
            if h2:
                for a in A_list_h2:
                    for b in A_list_h2:
                        ab = a * b
                        for x in X_list_h2:
                            if act_X(ab, x) != act_X(a, act_X(b, x)): h2 = False
                        for y in Y_list_h2:
                            if act_Y(ab, y) != act_Y(a, act_Y(b, y)): h2 = False
                        if not h2: break
                    if not h2: break
    except Exception:
        h2 = False

    # H3: For every a in A, the number of fixed points of a on X equals the number of fixed points of a on Y
    try:
        h3 = True
        if hasattr(A, 'elements'):
            A_list_h3 = list(A.elements)
        else:
            A_list_h3 = list(A)
            
        X_list_h3 = _unique_elements(list(X))
        Y_list_h3 = _unique_elements(list(Y))
        
        for a in A_list_h3:
            fix_X = sum(1 for x in X_list_h3 if act_X(a, x) == x)
            fix_Y = sum(1 for y in Y_list_h3 if act_Y(a, y) == y)
            if fix_X != fix_Y:
                h3 = False
                break
    except Exception:
        h3 = False

    # Negated Conclusion: The number of orbits of A on X is NOT equal to the number of orbits of A on Y
    try:
        if hasattr(A, 'elements'):
            A_list_q = list(A.elements)
        else:
            A_list_q = list(A)
            
        X_list_q = _unique_elements(list(X))
        Y_list_q = _unique_elements(list(Y))
        
        orbits_X = []
        for x in X_list_q:
            orb = []
            for a in A_list_q:
                val = act_X(a, x)
                if val not in orb:
                    orb.append(val)
            is_new = True
            for existing_orb in orbits_X:
                if len(existing_orb) == len(orb) and all(v in existing_orb for v in orb):
                    is_new = False
                    break
            if is_new:
                orbits_X.append(orb)
                
        orbits_Y = []
        for y in Y_list_q:
            orb = []
            for a in A_list_q:
                val = act_Y(a, y)
                if val not in orb:
                    orb.append(val)
            is_new = True
            for existing_orb in orbits_Y:
                if len(existing_orb) == len(orb) and all(v in existing_orb for v in orb):
                    is_new = False
                    break
            if is_new:
                orbits_Y.append(orb)
                
        neg_q = (len(orbits_X) != len(orbits_Y))
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: A is a finite group",
    "H_2: A acts on both X and Y",
    "H_3: For every a in A, the number of fixed points of a on X equals the number of fixed points of a on Y",
    "¬Q: The number of orbits of A on X is not equal to the number of orbits of A on Y"
]

N_HYP = 3
NEG_Q_INDEX = 3