import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.matrices
import itertools

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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: S and T are multiplicative subsets of R",
    "¬Q: The localized ring T_bar^-1(S^-1 R) is not isomorphic to (ST)^-1 R"
]
N_HYP = 2
NEG_Q_INDEX = 2

def call_op(op, x, y):
    if callable(op):
        return op(x, y)
    return op[x][y]

def is_commutative_ring(elements, add, mul):
    if not elements: return False
    # check closure
    for x in elements:
        for y in elements:
            if call_op(add, x, y) not in elements: return False
            if call_op(mul, x, y) not in elements: return False
    # check commutativity
    for x in elements:
        for y in elements:
            if call_op(add, x, y) != call_op(add, y, x): return False
            if call_op(mul, x, y) != call_op(mul, y, x): return False
    # check associativity
    for x in elements:
        for y in elements:
            for z in elements:
                xy_add = call_op(add, x, y)
                yz_add = call_op(add, y, z)
                if call_op(add, xy_add, z) != call_op(add, x, yz_add): return False
                
                xy_mul = call_op(mul, x, y)
                yz_mul = call_op(mul, y, z)
                if call_op(mul, xy_mul, z) != call_op(mul, x, yz_mul): return False
    # check distributivity
    for x in elements:
        for y in elements:
            for z in elements:
                yz_add = call_op(add, y, z)
                xy_mul = call_op(mul, x, y)
                xz_mul = call_op(mul, x, z)
                if call_op(mul, x, yz_add) != call_op(add, xy_mul, xz_mul): return False
    # check zero
    zero = None
    for x in elements:
        if all(call_op(add, x, y) == y for y in elements):
            zero = x
            break
    if zero is None: return False
    # check additive inverses
    for x in elements:
        if not any(call_op(add, x, y) == zero for y in elements): return False
    return True

def is_multiplicative_subset(elements, mul, S):
    if not S: return False
    for x in S:
        if x not in elements: return False
        for y in S:
            if y not in elements: return False
            if call_op(mul, x, y) not in S: return False
    return True

def localize(elements, add, mul, S):
    if not S:
        return None, None, None, None
    
    pairs = [(r, s) for r in elements for s in S]
    classes = []
    pair_to_class = {}
    
    for p in pairs:
        if p in pair_to_class:
            continue
        eq_class = []
        r1, s1 = p
        for q in pairs:
            r2, s2 = q
            term1 = call_op(mul, r1, s2)
            term2 = call_op(mul, r2, s1)
            equivalent = False
            for s3 in S:
                if call_op(mul, s3, term1) == call_op(mul, s3, term2):
                    equivalent = True
                    break
            if equivalent:
                eq_class.append(q)
        
        cls_tuple = tuple(sorted(eq_class, key=lambda x: str(x)))
        classes.append(cls_tuple)
        for q in eq_class:
            pair_to_class[q] = cls_tuple
            
    new_add = {}
    new_mul = {}
    for c1 in classes:
        new_add[c1] = {}
        new_mul[c1] = {}
        for c2 in classes:
            r1, s1 = c1[0]
            r2, s2 = c2[0]
            num_add = call_op(add, call_op(mul, r1, s2), call_op(mul, r2, s1))
            den_add = call_op(mul, s1, s2)
            new_add[c1][c2] = pair_to_class[(num_add, den_add)]
            
            num_mul = call_op(mul, r1, r2)
            den_mul = call_op(mul, s1, s2)
            new_mul[c1][c2] = pair_to_class[(num_mul, den_mul)]
            
    return classes, new_add, new_mul, pair_to_class

def are_isomorphic(elems1, add1, mul1, elems2, add2, mul2):
    if len(elems1) != len(elems2): return False
    if len(elems1) == 0: return True
    
    # Find zeros
    zero1 = None
    for x in elems1:
        if all(add1[x][y] == y for y in elems1):
            zero1 = x
            break
    zero2 = None
    for x in elems2:
        if all(add2[x][y] == y for y in elems2):
            zero2 = x
            break
            
    if zero1 is None or zero2 is None: return False
    
    # Find ones
    ones1 = [x for x in elems1 if all(mul1[x][y] == y for y in elems1)]
    ones2 = [x for x in elems2 if all(mul2[x][y] == y for y in elems2)]
    
    if not ones1 and not ones2:
        pass
    elif len(ones1) != len(ones2):
        return False
        
    for mapping in itertools.permutations(elems2):
        f = dict(zip(elems1, mapping))
        if f[zero1] != zero2: continue
        if ones1 and ones2 and f[ones1[0]] != ones2[0]: continue
        
        is_hom = True
        for x in elems1:
            for y in elems1:
                if f[add1[x][y]] != add2[f[x]][f[y]]:
                    is_hom = False
                    break
                if f[mul1[x][y]] != mul2[f[x]][f[y]]:
                    is_hom = False
                    break
            if not is_hom:
                break
        if is_hom:
            return True
    return False

def conditions(witness):
    try:
        elements, add, mul, S, T = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_commutative_ring(elements, add, mul)
    except Exception:
        h1 = False
        
    try:
        h2 = is_multiplicative_subset(elements, mul, S) and is_multiplicative_subset(elements, mul, T)
    except Exception:
        h2 = False
        
    try:
        if not (h1 and h2):
            neg_q = False
        else:
            # ST
            ST = list(set([call_op(mul, s, t) for s in S for t in T]))
            
            # (ST)^-1 R
            elems_ST, add_ST, mul_ST, _ = localize(elements, add, mul, ST)
            
            # S^-1 R
            elems_S, add_S, mul_S, pair_to_class_S = localize(elements, add, mul, S)
            
            # T_bar
            s0 = S[0]
            T_bar = []
            for t in T:
                num = call_op(mul, t, s0)
                den = s0
                T_bar.append(pair_to_class_S[(num, den)])
            T_bar = list(set(T_bar))
            
            # T_bar^-1 (S^-1 R)
            elems_Tbar, add_Tbar, mul_Tbar, _ = localize(elems_S, add_S, mul_S, T_bar)
            
            if elems_ST is None or elems_Tbar is None:
                neg_q = False
            else:
                iso = are_isomorphic(elems_Tbar, add_Tbar, mul_Tbar, elems_ST, add_ST, mul_ST)
                neg_q = not iso
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]