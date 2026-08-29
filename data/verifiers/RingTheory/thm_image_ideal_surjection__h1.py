import sympy
from sympy import eye, zeros, Rational, Integer
from sympy.abc import x, y, z
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ring(ring, add, mul, zero):
    try:
        ring = list(ring)
        if not ring: return False
        if zero not in ring: return False
        
        add_table = {}
        mul_table = {}
        for a in ring:
            add_table[a] = {}
            mul_table[a] = {}
            for b in ring:
                ab_add = add(a, b)
                if ab_add not in ring: return False
                add_table[a][b] = ab_add
                
                ab_mul = mul(a, b)
                if ab_mul not in ring: return False
                mul_table[a][b] = ab_mul

        for a in ring:
            if add_table[a][zero] != a or add_table[zero][a] != a: return False
            has_inv = False
            for b in ring:
                if add_table[a][b] == zero and add_table[b][a] == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            for b in ring:
                if add_table[a][b] != add_table[b][a]: return False

        for a in ring:
            for b in ring:
                ab_add = add_table[a][b]
                ab_mul = mul_table[a][b]
                for c in ring:
                    if add_table[ab_add][c] != add_table[a][add_table[b][c]]: return False
                    if mul_table[ab_mul][c] != mul_table[a][mul_table[b][c]]: return False
                    if mul_table[a][add_table[b][c]] != add_table[mul_table[a][b]][mul_table[a][c]]: return False
                    if mul_table[ab_add][c] != add_table[mul_table[a][c]][mul_table[b][c]]: return False
        return True
    except Exception:
        return False

def is_ideal(subset, ring, add, mul, zero):
    try:
        subset = list(subset)
        ring = list(ring)
        if not subset: return False
        if zero not in subset: return False
        
        for x in subset:
            if x not in ring: return False
            
            has_inv = False
            for y in subset:
                if add(x, y) == zero and add(y, x) == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
            for y in subset:
                if add(x, y) not in subset: return False
                
            for r in ring:
                if mul(x, r) not in subset: return False
                if mul(r, x) not in subset: return False
                
        return True
    except Exception:
        return False

def check_surjective(R, S, f_func):
    try:
        R = list(R)
        S = list(S)
        image = []
        for x in R:
            fx = f_func(x)
            if fx not in image:
                image.append(fx)
                
        for y in S:
            if y not in image:
                return False
        return True
    except Exception:
        return False

def check_neg_Q(I, S, add_S, mul_S, zero_S, f_func):
    try:
        I = list(I)
        S = list(S)
        f_I = []
        for x in I:
            fx = f_func(x)
            if fx not in f_I:
                f_I.append(fx)
                
        return not is_ideal(f_I, S, add_S, mul_S, zero_S)
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            R = witness['R']
            S = witness['S']
            add_R = witness['add_R']
            mul_R = witness['mul_R']
            zero_R = witness['zero_R']
            add_S = witness['add_S']
            mul_S = witness['mul_S']
            zero_S = witness['zero_S']
            f = witness['f']
            I = witness['I']
        else:
            R = witness.R
            S = witness.S
            add_R = witness.add_R
            mul_R = witness.mul_R
            zero_R = witness.zero_R
            add_S = witness.add_S
            mul_S = witness.mul_S
            zero_S = witness.zero_S
            f = witness.f
            I = witness.I

        if isinstance(f, dict):
            f_func = lambda x: f[x]
        else:
            f_func = f
    except Exception:
        return [False, False, False, False]

    try:
        h1 = True
        if not is_ring(R, add_R, mul_R, zero_R): h1 = False
        if not is_ring(S, add_S, mul_S, zero_S): h1 = False
        if h1:
            for x in R:
                fx = f_func(x)
                if fx not in S: 
                    h1 = False
                    break
                for y in R:
                    fy = f_func(y)
                    if f_func(add_R(x, y)) != add_S(fx, fy): 
                        h1 = False
                        break
                    if f_func(mul_R(x, y)) != mul_S(fx, fy): 
                        h1 = False
                        break
                if not h1: break
    except Exception:
        h1 = False

    h2 = check_surjective(R, S, f_func)
    h3 = is_ideal(I, R, add_R, mul_R, zero_R)
    neg_q = check_neg_Q(I, S, add_S, mul_S, zero_S, f_func)

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: f is a ring homomorphism from R to S",
    "H_2: f is surjective",
    "H_3: I is an ideal of R",
    "¬Q: f(I) is not an ideal of S"
]

N_HYP = 3
NEG_Q_INDEX = 3