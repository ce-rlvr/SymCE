import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_attr_or_key(witness, name, default=None):
    if isinstance(witness, dict):
        return witness.get(name, default)
    return getattr(witness, name, default)

def get_elements_and_op(witness, name_prefix):
    elements = get_attr_or_key(witness, name_prefix)
    op = get_attr_or_key(witness, name_prefix + '_op')
    
    if elements is None:
        return None, None
        
    if hasattr(elements, 'elements') and hasattr(elements, 'identity'):
        group_elements = list(elements.elements)
        if op is None:
            op = lambda x, y: x * y
        return group_elements, op
    
    return list(elements), op

def make_callable(func):
    if isinstance(func, dict):
        return lambda x: func[x]
    return func

def is_group(elements, op):
    if not elements:
        return False
    elements = list(elements)
    n = len(elements)
    
    # closure
    for i in range(n):
        for j in range(n):
            try:
                res = op(elements[i], elements[j])
                if res not in elements:
                    return False
            except Exception:
                return False
                
    # associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                try:
                    if op(elements[i], op(elements[j], elements[k])) != op(op(elements[i], elements[j]), elements[k]):
                        return False
                except Exception:
                    return False
                    
    # identity
    id_elem = None
    for i in range(n):
        e = elements[i]
        is_id = True
        for j in range(n):
            x = elements[j]
            try:
                if op(e, x) != x or op(x, e) != x:
                    is_id = False
                    break
            except Exception:
                is_id = False
                break
        if is_id:
            id_elem = e
            break
            
    if id_elem is None:
        return False
        
    # inverses
    for i in range(n):
        x = elements[i]
        has_inv = False
        for j in range(n):
            y = elements[j]
            try:
                if op(x, y) == id_elem and op(y, x) == id_elem:
                    has_inv = True
                    break
            except Exception:
                pass
        if not has_inv:
            return False
            
    return True

def conditions(witness) -> list[bool]:
    try:
        G, G_op = get_elements_and_op(witness, 'G')
        H, H_op = get_elements_and_op(witness, 'H')
        f_raw = get_attr_or_key(witness, 'f')
        g_raw = get_attr_or_key(witness, 'g')
        
        if G is None or G_op is None or H is None or H_op is None or f_raw is None or g_raw is None:
            return [False, False, False]
            
        f = make_callable(f_raw)
        g = make_callable(g_raw)
    except Exception:
        return [False, False, False]

    # H1: f is a group homomorphism
    try:
        h1_ok = is_group(G, G_op)
        if h1_ok:
            for x in G:
                fx = f(x)
                if fx not in H:
                    h1_ok = False
                    break
                for y in G:
                    if f(G_op(x, y)) != H_op(fx, f(y)):
                        h1_ok = False
                        break
                if not h1_ok:
                    break
    except Exception:
        h1_ok = False

    # H2: g is a group homomorphism
    try:
        h2_ok = is_group(G, G_op)
        if h2_ok:
            for x in G:
                gx = g(x)
                if gx not in H:
                    h2_ok = False
                    break
                for y in G:
                    if g(G_op(x, y)) != H_op(gx, g(y)):
                        h2_ok = False
                        break
                if not h2_ok:
                    break
    except Exception:
        h2_ok = False

    # neg_Q: E is NOT a subgroup of G
    try:
        E = [x for x in G if f(x) == g(x)]
        neg_q = not is_group(E, G_op)
    except Exception:
        neg_q = False

    return [bool(h1_ok), bool(h2_ok), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: f: G \\to H is a group homomorphism",
    "H_2: g: G \\to H is a group homomorphism",
    "¬Q: The set E = {x \\in G \\mid f(x) = g(x)} is not a subgroup of G"
]

N_HYP = 2
NEG_Q_INDEX = 2