import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def get_op(op_obj):
    if isinstance(op_obj, dict):
        return lambda x, y: op_obj.get((x, y))
    return op_obj

def get_action(act_obj):
    if isinstance(act_obj, dict):
        return lambda g, a: act_obj.get((g, a))
    return act_obj

def extract_group(obj):
    if hasattr(obj, 'elements') and hasattr(obj, 'identity'):
        return list(obj.elements), (lambda x, y: x * y), obj.identity
    if hasattr(obj, 'generate') and hasattr(obj, 'identity'):
        return list(obj.generate()), (lambda x, y: x * y), obj.identity
    if isinstance(obj, list):
        if not obj:
            raise ValueError("Empty list")
        
        if all(isinstance(x, int) for x in obj):
            n = len(obj)
            op = lambda x, y: (x + y) % n
            if 0 in obj and all(op(x, y) in obj for x in obj for y in obj):
                return obj, op, 0
            
            try:
                mod = max(obj) + 1
                op = lambda x, y: (x * y) % mod
                for e in obj:
                    if all(op(e, x) == x for x in obj) and all(op(x, y) in obj for x in obj for y in obj):
                        return obj, op, e
            except Exception:
                pass
                
        if all(isinstance(x, tuple) for x in obj):
            try:
                n_coords = len(obj[0])
                max_vals = [max(x[i] for x in obj) + 1 for i in range(n_coords)]
                op = lambda x, y: tuple((x[i] + y[i]) % max_vals[i] for i in range(n_coords))
                for e in obj:
                    if all(op(e, x) == x for x in obj) and all(op(x, y) in obj for x in obj for y in obj):
                        return obj, op, e
            except Exception:
                pass
            try:
                op = lambda x, y: tuple((x[i] * y[i]) for i in range(len(x)))
                for e in obj:
                    if all(op(e, x) == x for x in obj) and all(op(x, y) in obj for x in obj for y in obj):
                        return obj, op, e
            except Exception:
                pass

        try:
            op = lambda x, y: x + y
            for e in obj:
                if all(op(e, x) == x for x in obj) and all(op(x, y) in obj for x in obj for y in obj):
                    return obj, op, e
        except Exception:
            pass
            
        try:
            op = lambda x, y: x * y
            for e in obj:
                if all(op(e, x) == x for x in obj) and all(op(x, y) in obj for x in obj for y in obj):
                    return obj, op, e
        except Exception:
            pass

    raise ValueError("Cannot extract group")

def conditions(witness):
    try:
        if isinstance(witness, dict) and 'G_mult' in witness:
            G = list(witness['G'])
            G_mult = get_op(witness['G_mult'])
            G_id = witness['G_id']
            A = list(witness['A'])
            A_add = get_op(witness['A_add'])
            A_zero = witness['A_zero']
            action = get_action(witness['action'])
        elif isinstance(witness, dict):
            G, G_mult, G_id = extract_group(witness['G'])
            A, A_add, A_zero = extract_group(witness['A'])
            action = get_action(witness['action'])
        elif isinstance(witness, tuple) and len(witness) == 3:
            G, G_mult, G_id = extract_group(witness[0])
            A, A_add, A_zero = extract_group(witness[1])
            action = get_action(witness[2])
        elif hasattr(witness, 'G') and hasattr(witness, 'A') and hasattr(witness, 'action'):
            if hasattr(witness, 'G_mult'):
                G = list(witness.G)
                G_mult = get_op(witness.G_mult)
                G_id = witness.G_id
                A = list(witness.A)
                A_add = get_op(witness.A_add)
                A_zero = witness.A_zero
                action = get_action(witness.action)
            else:
                G, G_mult, G_id = extract_group(witness.G)
                A, A_add, A_zero = extract_group(witness.A)
                action = get_action(witness.action)
        else:
            return [False, False, False, False]
            
        G_unique = []
        for g in G:
            if g not in G_unique:
                G_unique.append(g)
        G = G_unique
        
        A_unique = []
        for a in A:
            if a not in A_unique:
                A_unique.append(a)
        A = A_unique
    except Exception:
        return [False, False, False, False]

    try:
        h1 = True
        if not G: h1 = False
        elif G_id not in G: h1 = False
        else:
            for g in G:
                if G_mult(g, G_id) != g or G_mult(G_id, g) != g:
                    h1 = False
                    break
                has_inv = False
                for h in G:
                    if G_mult(g, h) == G_id and G_mult(h, g) == G_id:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                for h in G:
                    gh = G_mult(g, h)
                    if gh not in G:
                        h1 = False
                        break
                    for k in G:
                        if G_mult(gh, k) != G_mult(g, G_mult(h, k)):
                            h1 = False
                            break
    except Exception:
        h1 = False

    try:
        h2 = True
        if not A: h2 = False
        elif A_zero not in A: h2 = False
        else:
            for a in A:
                if A_add(a, A_zero) != a or A_add(A_zero, a) != a:
                    h2 = False
                    break
                has_inv = False
                for b in A:
                    if A_add(a, b) == A_zero and A_add(b, a) == A_zero:
                        has_inv = True
                        break
                if not has_inv:
                    h2 = False
                    break
                for b in A:
                    ab = A_add(a, b)
                    if ab not in A:
                        h2 = False
                        break
                    if ab != A_add(b, a):
                        h2 = False
                        break
                    for c in A:
                        if A_add(ab, c) != A_add(a, A_add(b, c)):
                            h2 = False
                            break
    except Exception:
        h2 = False

    try:
        h3 = True
        for a in A:
            if action(G_id, a) != a:
                h3 = False
                break
            for g in G:
                ga = action(g, a)
                if ga not in A:
                    h3 = False
                    break
                for h in G:
                    if action(G_mult(g, h), a) != action(g, action(h, a)):
                        h3 = False
                        break
                for b in A:
                    if action(g, A_add(a, b)) != A_add(ga, action(g, b)):
                        h3 = False
                        break
    except Exception:
        h3 = False

    try:
        C_A = []
        for a in A:
            is_fixed = True
            for g in G:
                if action(g, a) != a:
                    is_fixed = False
                    break
            if is_fixed:
                C_A.append(a)
                
        def A_inv(a):
            for b in A:
                if A_add(a, b) == A_zero:
                    return b
            return None
            
        commutators = []
        for g in G:
            for a in A:
                c = A_add(action(g, a), A_inv(a))
                if c not in commutators:
                    commutators.append(c)
                    
        G_A = [A_zero]
        added = True
        while added:
            added = False
            new_elements = []
            for c in commutators:
                for x in G_A:
                    y = A_add(c, x)
                    if y not in G_A and y not in new_elements:
                        new_elements.append(y)
                    y_inv = A_inv(c)
                    z = A_add(y_inv, x)
                    if z not in G_A and z not in new_elements:
                        new_elements.append(z)
            if new_elements:
                G_A.extend(new_elements)
                added = True
                
        intersection = [x for x in C_A if x in G_A]
        is_direct_sum = True
        if len(intersection) > 1:
            is_direct_sum = False
            
        sum_set = []
        for c in C_A:
            for d in G_A:
                s = A_add(c, d)
                if s not in sum_set:
                    sum_set.append(s)
        if len(sum_set) != len(A):
            is_direct_sum = False
            
        neg_q = not is_direct_sum
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: A is a finite abelian group",
    "H_3: G acts on A by group automorphisms",
    "¬Q: A does not decompose as the direct sum C_A(G) and the commutator subgroup"
]

N_HYP = 3
NEG_Q_INDEX = 3