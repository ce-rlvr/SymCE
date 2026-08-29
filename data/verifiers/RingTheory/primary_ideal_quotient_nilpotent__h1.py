import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import itertools
import functools
import math

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

def get_ring_ops(witness):
    if isinstance(witness, tuple):
        if len(witness) == 4:
            if isinstance(witness[0], int):
                n, add, mul, q_list = witness
                elements = list(range(n))
                q = list(q_list)
                def add_f(x, y): return add[x][y]
                def mul_f(x, y): return mul[x][y]
                def eq(x, y): return x == y
            elif isinstance(witness[0], list) or isinstance(witness[0], tuple):
                elements, add, mul, q_list = witness
                elements = list(elements)
                q = list(q_list)
                if callable(add) and callable(mul):
                    def add_f(x, y): return add(x, y)
                    def mul_f(x, y): return mul(x, y)
                else:
                    def add_f(x, y):
                        i = elements.index(x)
                        j = elements.index(y)
                        return add[i][j]
                    def mul_f(x, y):
                        i = elements.index(x)
                        j = elements.index(y)
                        return mul[i][j]
                def eq(x, y): return x == y
            else:
                raise ValueError("Unknown witness format")
        elif len(witness) == 2:
            R, q_list = witness
            elements = list(R)
            q = list(q_list)
            def add_f(x, y): return x + y
            def mul_f(x, y): return x * y
            def eq(x, y): return x == y
        else:
            raise ValueError("Unknown witness format")
    elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'q'):
        elements = list(witness.elements)
        q = list(witness.q)
        def add_f(x, y): return witness.add(x, y)
        def mul_f(x, y): return witness.mul(x, y)
        def eq(x, y): return x == y
    else:
        raise ValueError("Unknown witness format")
        
    unique_elements = []
    for x in elements:
        if not any(eq(x, y) for y in unique_elements):
            unique_elements.append(x)
            
    unique_q = []
    for x in q:
        if not any(eq(x, y) for y in unique_q):
            unique_q.append(x)
            
    return unique_elements, add_f, mul_f, eq, unique_q

def is_ring(elements, add_f, mul_f, eq):
    n = len(elements)
    if n == 0: return False
    
    for x in elements:
        for y in elements:
            try:
                s = add_f(x, y)
                p = mul_f(x, y)
            except Exception:
                return False
            if not any(eq(s, z) for z in elements): return False
            if not any(eq(p, z) for z in elements): return False
            
    zero = None
    for x in elements:
        if all(eq(add_f(x, y), y) for y in elements) and all(eq(add_f(y, x), y) for y in elements):
            zero = x
            break
    if zero is None: return False
    
    for x in elements:
        if not any(eq(add_f(x, y), zero) and eq(add_f(y, x), zero) for y in elements): return False
        
    if n <= 50:
        subset = elements
    else:
        subset = elements[:10]
        
    for x in subset:
        for y in subset:
            for z in subset:
                if not eq(add_f(x, add_f(y, z)), add_f(add_f(x, y), z)): return False
                if not eq(mul_f(x, mul_f(y, z)), mul_f(mul_f(x, y), z)): return False
                if not eq(mul_f(x, add_f(y, z)), add_f(mul_f(x, y), mul_f(x, z))): return False
                if not eq(mul_f(add_f(x, y), z), add_f(mul_f(x, z), mul_f(y, z))): return False
                
    return True

def is_proper_ideal(elements, add_f, mul_f, eq, q):
    if not is_ring(elements, add_f, mul_f, eq): return False
    
    for x in q:
        if not any(eq(x, y) for y in elements): return False
        
    if len(q) == len(elements): return False
    if len(q) == 0: return False
    
    zero = None
    for x in elements:
        if all(eq(add_f(x, y), y) for y in elements):
            zero = x
            break
    if zero is None: return False
    
    if not any(eq(zero, y) for y in q): return False
    
    for x in q:
        for y in q:
            if not any(eq(add_f(x, y), z) for z in q): return False
            
    for x in q:
        has_inv = False
        for y in q:
            if eq(add_f(x, y), zero):
                has_inv = True
                break
        if not has_inv: return False
        
    for x in q:
        for r in elements:
            xr = mul_f(x, r)
            rx = mul_f(r, x)
            if not any(eq(xr, z) for z in q): return False
            if not any(eq(rx, z) for z in q): return False
            
    return True

def is_primary(elements, add_f, mul_f, eq, q):
    right_primary = True
    for a in elements:
        for b in elements:
            ab = mul_f(a, b)
            if any(eq(ab, z) for z in q):
                if any(eq(a, z) for z in q):
                    continue
                curr = b
                is_nilp = False
                for _ in range(len(elements) + 1):
                    if any(eq(curr, z) for z in q):
                        is_nilp = True
                        break
                    curr = mul_f(curr, b)
                if not is_nilp:
                    right_primary = False
                    break
        if not right_primary:
            break

    left_primary = True
    for a in elements:
        for b in elements:
            ab = mul_f(a, b)
            if any(eq(ab, z) for z in q):
                if any(eq(b, z) for z in q):
                    continue
                curr = a
                is_nilp = False
                for _ in range(len(elements) + 1):
                    if any(eq(curr, z) for z in q):
                        is_nilp = True
                        break
                    curr = mul_f(curr, a)
                if not is_nilp:
                    left_primary = False
                    break
        if not left_primary:
            break

    return right_primary or left_primary

def zero_divisors_are_nilpotent(elements, add_f, mul_f, eq, q):
    for x in elements:
        if any(eq(x, z) for z in q): continue
        is_zd = False
        for y in elements:
            if any(eq(y, z) for z in q): continue
            xy = mul_f(x, y)
            yx = mul_f(y, x)
            if any(eq(xy, z) for z in q) or any(eq(yx, z) for z in q):
                is_zd = True
                break
        if is_zd:
            curr = x
            is_nilp = False
            for _ in range(len(elements) + 1):
                if any(eq(curr, z) for z in q):
                    is_nilp = True
                    break
                curr = mul_f(curr, x)
            if not is_nilp:
                return False
    return True

def conditions(witness):
    try:
        elements, add_f, mul_f, eq, q = get_ring_ops(witness)
    except Exception:
        return [False, False]
        
    try:
        h1 = is_proper_ideal(elements, add_f, mul_f, eq, q)
    except Exception:
        h1 = False
        
    try:
        if not h1:
            neg_q = False
        else:
            prim = is_primary(elements, add_f, mul_f, eq, q)
            zd_nilp = zero_divisors_are_nilpotent(elements, add_f, mul_f, eq, q)
            neg_q = (prim != zd_nilp)
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: q is a proper ideal of R",
    "¬Q: q is a primary ideal iff every zero divisor in R/q is nilpotent fails"
]

N_HYP = 1
NEG_Q_INDEX = 1