import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

def make_callable(op):
    if isinstance(op, dict):
        return lambda a, b: op.get((a, b), op.get(str((a, b))))
    return op

def make_callable_f(f):
    if isinstance(f, dict):
        return lambda x: f.get(x, f.get(str(x)))
    return f

def check_ring(elements, add, mul):
    if not elements: return False
    elements = list(elements)
    for a in elements:
        for b in elements:
            s = add(a, b)
            if s not in elements: return False
            if s != add(b, a): return False
            for c in elements:
                if add(s, c) != add(a, add(b, c)): return False
    zero = None
    for z in elements:
        if all(add(z, a) == a for a in elements):
            zero = z
            break
    if zero is None: return False
    for a in elements:
        if not any(add(a, b) == zero for b in elements): return False
    for a in elements:
        for b in elements:
            p = mul(a, b)
            if p not in elements: return False
            if p != mul(b, a): return False
            for c in elements:
                if mul(p, c) != mul(a, mul(b, c)): return False
    for a in elements:
        for b in elements:
            for c in elements:
                if mul(a, add(b, c)) != add(mul(a, b), mul(a, c)): return False
    return True

def check_homomorphism(R, S, add_R, mul_R, add_S, mul_S, f):
    if not R or not S or not f: return False
    for a in R:
        fa = f(a)
        if fa not in S: return False
        for b in R:
            if f(add_R(a, b)) != add_S(fa, f(b)): return False
            if f(mul_R(a, b)) != mul_S(fa, f(b)): return False
    one_R = None
    for e in R:
        if all(mul_R(e, a) == a for a in R):
            one_R = e
            break
    one_S = None
    for e in S:
        if all(mul_S(e, a) == a for a in S):
            one_S = e
            break
    if one_R is not None and one_S is not None:
        if f(one_R) != one_S: return False
    return True

def check_ideal(R, add_R, mul_R, I):
    if not I or not R: return False
    for x in I:
        if x not in R: return False
    zero = None
    for z in R:
        if all(add_R(z, a) == a for a in R):
            zero = z
            break
    if zero not in I: return False
    for a in I:
        for b in I:
            if add_R(a, b) not in I: return False
        inv = None
        for x in R:
            if add_R(a, x) == zero:
                inv = x
                break
        if inv not in I: return False
    for r in R:
        for a in I:
            if mul_R(r, a) not in I: return False
    return True

def ideal_generated_by(S, add_S, mul_S, subset):
    closure = []
    for x in subset:
        if x in S and x not in closure:
            closure.append(x)
    zero = None
    for z in S:
        if all(add_S(z, a) == a for a in S):
            zero = z
            break
    if zero is not None and zero not in closure:
        closure.append(zero)
    
    changed = True
    while changed:
        changed = False
        new_elements = []
        for a in closure:
            for b in closure:
                s = add_S(a, b)
                if s in S and s not in closure and s not in new_elements:
                    new_elements.append(s)
            for r in S:
                p = mul_S(r, a)
                if p in S and p not in closure and p not in new_elements:
                    new_elements.append(p)
            for x in S:
                if add_S(a, x) == zero:
                    if x not in closure and x not in new_elements:
                        new_elements.append(x)
                    break
        if new_elements:
            closure.extend(new_elements)
            changed = True
    return closure

def product_ideal(R, add_R, mul_R, I, J):
    generators = []
    for i in I:
        for j in J:
            p = mul_R(i, j)
            if p not in generators:
                generators.append(p)
    return ideal_generated_by(R, add_R, mul_R, generators)

def extension(S, add_S, mul_S, f, I):
    f_I = [f(i) for i in I]
    return ideal_generated_by(S, add_S, mul_S, f_I)

def sets_equal(A, B):
    if len(A) != len(B): return False
    for a in A:
        if a not in B: return False
    return True

def conditions(witness):
    try:
        R = witness["R"]
        S = witness["S"]
        add_R = make_callable(witness["add_R"])
        mul_R = make_callable(witness["mul_R"])
        add_S = make_callable(witness["add_S"])
        mul_S = make_callable(witness["mul_S"])
        f = make_callable_f(witness["f"])
        I = witness["I"]
        J = witness["J"]
    except Exception:
        return [False, False, False, False, False]
    
    try:
        h1 = check_ring(R, add_R, mul_R)
    except Exception:
        h1 = False

    try:
        h2 = check_ring(S, add_S, mul_S)
    except Exception:
        h2 = False

    try:
        h3 = check_homomorphism(R, S, add_R, mul_R, add_S, mul_S, f)
    except Exception:
        h3 = False

    try:
        h4 = check_ideal(R, add_R, mul_R, I)
    except Exception:
        h4 = False

    try:
        IJ = product_ideal(R, add_R, mul_R, I, J)
        IJ_e = extension(S, add_S, mul_S, f, IJ)
        
        I_e = extension(S, add_S, mul_S, f, I)
        J_e = extension(S, add_S, mul_S, f, J)
        I_e_J_e = product_ideal(S, add_S, mul_S, I_e, J_e)
        
        neg_Q = not sets_equal(IJ_e, I_e_J_e)
    except Exception:
        neg_Q = False

    return [h1, h2, h3, h4, neg_Q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S is a commutative ring",
    "H_3: f is a ring homomorphism from R to S",
    "H_4: I is an ideal of R",
    "¬Q: (IJ)^e != I^e J^e"
]

N_HYP = 4
NEG_Q_INDEX = 4