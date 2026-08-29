import itertools

# Top-level setup
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
O2 = zeros(2,2)
O3 = zeros(3,3)

CONDITION_LABELS = [
    "H_1: f is a graded ring homomorphism of degree zero",
    "¬Q: The kernel of f is not a homogeneous ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        R = witness.R
        S = witness.S
        R_add = witness.R_add
        R_mul = witness.R_mul
        S_add = witness.S_add
        S_mul = witness.S_mul
        R_zero = witness.R_zero
        S_zero = witness.S_zero
        R_one = witness.R_one
        S_one = witness.S_one
        f = witness.f
        
        G_add = getattr(witness, 'G_add', lambda a, b: a + b)
        H_add = getattr(witness, 'H_add', lambda a, b: a + b)
        phi = getattr(witness, 'phi', lambda d: d)
        
        R_hom = witness.R_hom
        S_hom = witness.S_hom
    except AttributeError:
        return [False, False]

    def check_ring(elems, add, mul, zero, one):
        if zero not in elems or one not in elems: return False
        
        add_t = {}
        mul_t = {}
        for a in elems:
            add_t[a] = {}
            mul_t[a] = {}
            for b in elems:
                try:
                    s = add(a, b)
                    p = mul(a, b)
                except Exception:
                    return False
                if s not in elems or p not in elems: return False
                add_t[a][b] = s
                mul_t[a][b] = p

        for a in elems:
            if add_t[a][zero] != a: return False
            if add_t[zero][a] != a: return False
            if mul_t[a][one] != a: return False
            if mul_t[one][a] != a: return False
            if mul_t[a][zero] != zero: return False
            if mul_t[zero][a] != zero: return False
            
            has_inv = False
            for b in elems:
                if add_t[a][b] == zero:
                    has_inv = True
                if add_t[a][b] != add_t[b][a]: return False
            if not has_inv: return False

            for b in elems:
                ab_add = add_t[a][b]
                ab_mul = mul_t[a][b]
                for c in elems:
                    if add_t[ab_add][c] != add_t[a][add_t[b][c]]: return False
                    if mul_t[ab_mul][c] != mul_t[a][mul_t[b][c]]: return False
                    if mul_t[a][add_t[b][c]] != add_t[mul_t[a][b]][mul_t[a][c]]: return False
                    if mul_t[add_t[a][b]][c] != add_t[mul_t[a][c]][mul_t[b][c]]: return False
        return True

    try:
        if not check_ring(R, R_add, R_mul, R_zero, R_one): return [False, False]
        if not check_ring(S, S_add, S_mul, S_zero, S_one): return [False, False]
    except Exception:
        return [False, False]

    try:
        for d, elems in R_hom.items():
            if R_zero not in elems: return [False, False]
            for a in elems:
                if a not in R: return [False, False]
                for b in elems:
                    if R_add(a, b) not in elems: return [False, False]
        
        for d, elems_d in R_hom.items():
            for e, elems_e in R_hom.items():
                target_deg = G_add(d, e)
                target_elems = R_hom.get(target_deg, [R_zero])
                for a in elems_d:
                    for b in elems_e:
                        if R_mul(a, b) not in target_elems: return [False, False]
        
        r_degrees = list(R_hom.keys())
        r_decomp = {}
        for combo in itertools.product(*(R_hom[d] for d in r_degrees)):
            s = R_zero
            for x in combo:
                s = R_add(s, x)
            if s in r_decomp:
                return [False, False]
            r_decomp[s] = dict(zip(r_degrees, combo))
        
        if len(r_decomp) != len(R): return [False, False]
        for x in R:
            if x not in r_decomp: return [False, False]
    except Exception:
        return [False, False]

    try:
        for d, elems in S_hom.items():
            if S_zero not in elems: return [False, False]
            for a in elems:
                if a not in S: return [False, False]
                for b in elems:
                    if S_add(a, b) not in elems: return [False, False]
        
        for d, elems_d in S_hom.items():
            for e, elems_e in S_hom.items():
                target_deg = H_add(d, e)
                target_elems = S_hom.get(target_deg, [S_zero])
                for a in elems_d:
                    for b in elems_e:
                        if S_mul(a, b) not in target_elems: return [False, False]
        
        s_degrees = list(S_hom.keys())
        s_decomp = set()
        for combo in itertools.product(*(S_hom[d] for d in s_degrees)):
            s = S_zero
            for y in combo:
                s = S_add(s, y)
            if s in s_decomp:
                return [False, False]
            s_decomp.add(s)
        
        if len(s_decomp) != len(S): return [False, False]
        for y in S:
            if y not in s_decomp: return [False, False]
    except Exception:
        return [False, False]

    try:
        if f(R_one) != S_one: return [False, False]
        if f(R_zero) != S_zero: return [False, False]
        for a in R:
            for b in R:
                if f(R_add(a, b)) != S_add(f(a), f(b)): return [False, False]
                if f(R_mul(a, b)) != S_mul(f(a), f(b)): return [False, False]
    except Exception:
        return [False, False]

    try:
        for d in r_degrees:
            for e in r_degrees:
                if phi(G_add(d, e)) != H_add(phi(d), phi(e)): return [False, False]
    except Exception:
        return [False, False]

    try:
        for d, elems in R_hom.items():
            target_deg = phi(d)
            target_elems = S_hom.get(target_deg, [S_zero])
            for x in elems:
                if f(x) not in target_elems: return [False, False]
    except Exception:
        return [False, False]

    h1_ok = True

    try:
        ker_f = set(x for x in R if f(x) == S_zero)
        
        is_homogeneous = True
        for x in ker_f:
            decomp = r_decomp[x]
            for d, x_d in decomp.items():
                if x_d not in ker_f:
                    is_homogeneous = False
                    break
            if not is_homogeneous:
                break
        
        neg_q_ok = not is_homogeneous
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]