import sympy
from sympy.combinatorics.free_groups import FreeGroup

# Top-level setup
F2 = FreeGroup('x, y')
x, y = F2.generators

def cyclically_reduce(w):
    letters = list(w.letters)
    while len(letters) >= 2 and letters[0] == letters[-1]**-1:
        letters = letters[1:-1]
    res = F2.identity
    for l in letters:
        res = res * l
    return res

def is_cyclic_shift(w1, w2):
    l1 = list(w1.letters)
    l2 = list(w2.letters)
    if len(l1) != len(l2):
        return False
    if len(l1) == 0:
        return True
    for i in range(len(l1)):
        if l1[i:] + l1[:i] == l2:
            return True
    return False

def to_F2(w):
    try:
        if w in F2:
            return w
    except Exception:
        pass
    if not hasattr(w, 'letters'):
        return None
    l_F2 = []
    for l in w.letters:
        name = str(l)
        if name == 'x': 
            l_F2.append(x)
        elif name == 'x**-1': 
            l_F2.append(x**-1)
        elif name == 'y': 
            l_F2.append(y)
        elif name == 'y**-1': 
            l_F2.append(y**-1)
        else: 
            return None
    res = F2.identity
    for l in l_F2:
        res = res * l
    return res

def is_basis(u, v):
    try:
        u_F2 = to_F2(u)
        v_F2 = to_F2(v)
        if u_F2 is None or v_F2 is None:
            return False
        
        a, b = u_F2, v_F2
        if len(a) == 0 or len(b) == 0:
            return False
            
        visited = set()
        queue = [(a, b)]
        
        while queue:
            curr_a, curr_b = queue.pop(0)
            state = (curr_a, curr_b)
            if state in visited:
                continue
            visited.add(state)
            
            if len(curr_a) == 1 and len(curr_b) == 1:
                g_a = list(curr_a.letters)[0]
                g_b = list(curr_b.letters)[0]
                if g_a != g_b and g_a != g_b**-1:
                    return True
            
            current_len = len(curr_a) + len(curr_b)
            
            neighbors = [
                (curr_a**-1, curr_b),
                (curr_a, curr_b**-1),
                (curr_b, curr_a),
                (curr_a * curr_b, curr_b),
                (curr_b * curr_a, curr_b),
                (curr_a * curr_b**-1, curr_b),
                (curr_b**-1 * curr_a, curr_b),
                (curr_a, curr_a * curr_b),
                (curr_a, curr_b * curr_a),
                (curr_a, curr_a**-1 * curr_b),
                (curr_a, curr_b * curr_a**-1)
            ]
            
            for na, nb in neighbors:
                if len(na) + len(nb) <= current_len:
                    if (na, nb) not in visited:
                        queue.append((na, nb))
                        
        return False
    except Exception:
        return False

def is_conjugate(w1, w2):
    try:
        w1_F2 = to_F2(w1)
        w2_F2 = to_F2(w2)
        if w1_F2 is None or w2_F2 is None:
            return False
        cr1 = cyclically_reduce(w1_F2)
        cr2 = cyclically_reduce(w2_F2)
        return is_cyclic_shift(cr1, cr2)
    except Exception:
        return False

def conditions(witness):
    try:
        u, v = witness
    except Exception:
        return [False, False, False]
        
    h1_ok = True
    h2_ok = True
        
    try:
        basis_ok = is_basis(u, v)
    except Exception:
        basis_ok = False
        
    try:
        u_F2 = to_F2(u)
        v_F2 = to_F2(v)
        if u_F2 is None or v_F2 is None:
            conj_ok = False
        else:
            c = u_F2 * v_F2 * u_F2**-1 * v_F2**-1
            xy = x * y * x**-1 * y**-1
            yx = y * x * y**-1 * x**-1
            conj_ok = is_conjugate(c, xy) or is_conjugate(c, yx)
    except Exception:
        conj_ok = False
        
    neg_q = (basis_ok != conj_ok)
    
    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: F2 is a free group of rank 2",
    "H_2: x and y form a free basis of F2",
    "not Q: The equivalence between u, v being a free basis and their commutator being conjugate to that of x, y fails"
]

N_HYP = 2
NEG_Q_INDEX = 2