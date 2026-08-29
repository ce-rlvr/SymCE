import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

# Top-level setup
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

def contains(lst, item, eq):
    for x in lst:
        if eq(x, item):
            return True
    return False

def parse_witness(witness):
    if isinstance(witness, dict):
        R = witness['R']
        S = witness['S']
        I = witness['I']
        add = witness.get('add', lambda x, y: x + y)
        mul = witness.get('mul', lambda x, y: x * y)
        eq = witness.get('eq', lambda x, y: x == y)
    elif hasattr(witness, 'R') and hasattr(witness, 'S') and hasattr(witness, 'I'):
        R = witness.R
        S = witness.S
        I = witness.I
        add = getattr(witness, 'add', lambda x, y: x + y)
        mul = getattr(witness, 'mul', lambda x, y: x * y)
        eq = getattr(witness, 'eq', lambda x, y: x == y)
    elif isinstance(witness, tuple) and len(witness) == 3:
        R, S, I = witness
        add = lambda x, y: x + y
        mul = lambda x, y: x * y
        eq = lambda x, y: x == y
    else:
        raise ValueError("Unknown witness format")
        
    zero = None
    for z in R:
        if all(eq(add(z, x), x) and eq(add(x, z), x) for x in R):
            zero = z
            break
            
    if zero is None:
        raise ValueError("Ring R has no zero element")
        
    neg_map = {}
    for x in R:
        for y in R:
            if eq(add(x, y), zero) and eq(add(y, x), zero):
                neg_map[x] = y
                break
    
    def neg(x):
        if x in neg_map:
            return neg_map[x]
        return -x
        
    return R, S, I, add, mul, neg, zero, eq

def is_subring(R, S, add, mul, neg, zero, eq):
    if not S: return False
    for s in S:
        if not contains(R, s, eq): return False
    if zero is not None and not contains(S, zero, eq): return False
    for a in S:
        if not contains(S, neg(a), eq): return False
        for b in S:
            if not contains(S, add(a, b), eq): return False
            if not contains(S, mul(a, b), eq): return False
    return True

def is_ideal(R, I, add, mul, neg, zero, eq):
    if not is_subring(R, I, add, mul, neg, zero, eq): return False
    for r in R:
        for i in I:
            if not contains(I, mul(r, i), eq): return False
            if not contains(I, mul(i, r), eq): return False
    return True

def get_cosets(ring, ideal, add, eq):
    cosets = []
    for r in ring:
        coset = []
        for i in ideal:
            val = add(r, i)
            if not contains(coset, val, eq):
                coset.append(val)
        is_new = True
        for c in cosets:
            if len(c) == len(coset) and all(contains(c, x, eq) for x in coset):
                is_new = False
                break
        if is_new:
            cosets.append(coset)
    return cosets

def find_coset(cosets, element, eq):
    for c in cosets:
        if contains(c, element, eq):
            return c
    return None

def check_canonical_isomorphism(cosets_S_cap_I, cosets_I, add, mul, eq):
    mapping = {}
    for idx, c in enumerate(cosets_S_cap_I):
        rep = c[0]
        target_c = find_coset(cosets_I, rep, eq)
        if target_c is None: return False
        
        target_idx = -1
        for i, tc in enumerate(cosets_I):
            if tc is target_c:
                target_idx = i
                break
        if target_idx == -1: return False
        mapping[idx] = target_idx
        
    if len(set(mapping.values())) != len(cosets_I):
        return False
        
    for i1, c1 in enumerate(cosets_S_cap_I):
        for i2, c2 in enumerate(cosets_S_cap_I):
            sum_rep = add(c1[0], c2[0])
            sum_c1 = find_coset(cosets_S_cap_I, sum_rep, eq)
            if sum_c1 is None: return False
            
            sum_c1_idx = -1
            for i, tc in enumerate(cosets_S_cap_I):
                if tc is sum_c1: sum_c1_idx = i; break
            target_sum_idx = mapping[sum_c1_idx]
            
            sum_target_rep = add(cosets_I[mapping[i1]][0], cosets_I[mapping[i2]][0])
            expected_target_sum = find_coset(cosets_I, sum_target_rep, eq)
            if expected_target_sum is None: return False
            
            expected_target_sum_idx = -1
            for i, tc in enumerate(cosets_I):
                if tc is expected_target_sum: expected_target_sum_idx = i; break
                
            if target_sum_idx != expected_target_sum_idx:
                return False
                
            mul_rep = mul(c1[0], c2[0])
            mul_c1 = find_coset(cosets_S_cap_I, mul_rep, eq)
            if mul_c1 is None: return False
            
            mul_c1_idx = -1
            for i, tc in enumerate(cosets_S_cap_I):
                if tc is mul_c1: mul_c1_idx = i; break
            target_mul_idx = mapping[mul_c1_idx]
            
            mul_target_rep = mul(cosets_I[mapping[i1]][0], cosets_I[mapping[i2]][0])
            expected_target_mul = find_coset(cosets_I, mul_target_rep, eq)
            if expected_target_mul is None: return False
            
            expected_target_mul_idx = -1
            for i, tc in enumerate(cosets_I):
                if tc is expected_target_mul: expected_target_mul_idx = i; break
                
            if target_mul_idx != expected_target_mul_idx:
                return False
    return True

def check_isomorphism(ring1, ideal1, cosets1, ring2, ideal2, cosets2, add, mul, eq):
    n = len(cosets1)
    if n != len(cosets2): return False
    if n > 8: return False
    
    for p in itertools.permutations(range(n)):
        mapping = {i: p[i] for i in range(n)}
        is_iso = True
        for i1 in range(n):
            for i2 in range(n):
                sum_rep = add(cosets1[i1][0], cosets1[i2][0])
                sum_c1 = find_coset(cosets1, sum_rep, eq)
                if sum_c1 is None: is_iso = False; break
                
                sum_c1_idx = -1
                for i, tc in enumerate(cosets1):
                    if tc is sum_c1: sum_c1_idx = i; break
                target_sum_idx = mapping[sum_c1_idx]
                
                sum_target_rep = add(cosets2[mapping[i1]][0], cosets2[mapping[i2]][0])
                expected_target_sum = find_coset(cosets2, sum_target_rep, eq)
                if expected_target_sum is None: is_iso = False; break
                
                expected_target_sum_idx = -1
                for i, tc in enumerate(cosets2):
                    if tc is expected_target_sum: expected_target_sum_idx = i; break
                    
                if target_sum_idx != expected_target_sum_idx:
                    is_iso = False; break
                    
                mul_rep = mul(cosets1[i1][0], cosets1[i2][0])
                mul_c1 = find_coset(cosets1, mul_rep, eq)
                if mul_c1 is None: is_iso = False; break
                
                mul_c1_idx = -1
                for i, tc in enumerate(cosets1):
                    if tc is mul_c1: mul_c1_idx = i; break
                target_mul_idx = mapping[mul_c1_idx]
                
                mul_target_rep = mul(cosets2[mapping[i1]][0], cosets2[mapping[i2]][0])
                expected_target_mul = find_coset(cosets2, mul_target_rep, eq)
                if expected_target_mul is None: is_iso = False; break
                
                expected_target_mul_idx = -1
                for i, tc in enumerate(cosets2):
                    if tc is expected_target_mul: expected_target_mul_idx = i; break
                    
                if target_mul_idx != expected_target_mul_idx:
                    is_iso = False; break
            if not is_iso:
                break
        if is_iso:
            return True
    return False

def conditions(witness):
    try:
        R, S, I, add, mul, neg, zero, eq = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    try:
        h1 = is_subring(R, S, add, mul, neg, zero, eq)
    except Exception:
        h1 = False
        
    try:
        h2 = is_ideal(R, I, add, mul, neg, zero, eq)
    except Exception:
        h2 = False
        
    try:
        S_cap_I = [x for x in S if contains(I, x, eq)]
        cond1 = is_ideal(S, S_cap_I, add, mul, neg, zero, eq)
        
        S_plus_I = []
        for s in S:
            for i in I:
                val = add(s, i)
                if not contains(S_plus_I, val, eq):
                    S_plus_I.append(val)
        cond2 = is_subring(R, S_plus_I, add, mul, neg, zero, eq)
        
        if not cond1 or not cond2:
            q = False
        else:
            quotient1 = get_cosets(S_plus_I, I, add, eq)
            quotient2 = get_cosets(S, S_cap_I, add, eq)
            
            if len(quotient1) != len(quotient2):
                q = False
            else:
                if check_canonical_isomorphism(quotient2, quotient1, add, mul, eq):
                    q = True
                else:
                    q = check_isomorphism(S_plus_I, I, quotient1, S, S_cap_I, quotient2, add, mul, eq)
    except Exception:
        q = True
        
    return [h1, h2, not q]

CONDITION_LABELS = [
    "H_1: S is a subring of R",
    "H_2: I is an ideal of R",
    "¬Q: S \\cap I is not an ideal of S, or S+I is not a subring of R, or (S+I)/I is not isomorphic to S/(S \\cap I)"
]

N_HYP = 2
NEG_Q_INDEX = 2