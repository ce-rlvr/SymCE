import itertools
from sympy import Matrix

class Zn:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1 % n
    def add(self, a, b):
        return (a + b) % self.n
    def mul(self, a, b):
        return (a * b) % self.n
    def sub(self, a, b):
        return (a - b) % self.n
    def eq(self, a, b):
        return (a - b) % self.n == 0

class MatrixRing:
    def __init__(self, n, modulus):
        self.n = n
        self.modulus = modulus
        self.elements = []
        for entries in itertools.product(range(modulus), repeat=n*n):
            self.elements.append(Matrix(n, n, entries))
        self.zero = Matrix.zeros(n, n)
        self.one = Matrix.eye(n).applyfunc(lambda x: x % modulus)
    def add(self, a, b):
        return (a + b).applyfunc(lambda x: x % self.modulus)
    def mul(self, a, b):
        return (a * b).applyfunc(lambda x: x % self.modulus)
    def sub(self, a, b):
        return (a - b).applyfunc(lambda x: x % self.modulus)
    def eq(self, a, b):
        return self.sub(a, b) == self.zero

Z2 = Zn(2)
Z3 = Zn(3)
Z4 = Zn(4)
Z6 = Zn(6)
M2_Z2 = MatrixRing(2, 2)

def conditions(witness) -> list[bool]:
    try:
        R, e = witness
    except Exception:
        return [False, False]
        
    # H1: R is a ring with identity
    try:
        h1 = True
        if not hasattr(R, 'elements') or not hasattr(R, 'add') or not hasattr(R, 'mul'):
            h1 = False
        elif not hasattr(R, 'zero') or not hasattr(R, 'one') or not hasattr(R, 'eq') or not hasattr(R, 'sub'):
            h1 = False
        else:
            # Check if e is in R
            if not any(R.eq(e, x) for x in R.elements):
                h1 = False
                
            if h1:
                # Check if one is identity
                for x in R.elements:
                    if not R.eq(R.mul(R.one, x), x) or not R.eq(R.mul(x, R.one), x):
                        h1 = False
                        break
            if h1:
                # Check if zero is additive identity
                for x in R.elements:
                    if not R.eq(R.add(R.zero, x), x) or not R.eq(R.add(x, R.zero), x):
                        h1 = False
                        break
            if h1:
                # Check ring axioms on a subset to ensure it's a valid ring
                subset = R.elements[:10]
                for a in subset:
                    for b in subset:
                        if not R.eq(R.add(a, b), R.add(b, a)):
                            h1 = False
                            break
                        for c in subset:
                            if not R.eq(R.add(R.add(a, b), c), R.add(a, R.add(b, c))):
                                h1 = False
                                break
                            if not R.eq(R.mul(R.mul(a, b), c), R.mul(a, R.mul(b, c))):
                                h1 = False
                                break
                            if not R.eq(R.mul(a, R.add(b, c)), R.add(R.mul(a, b), R.mul(a, c))):
                                h1 = False
                                break
                            if not R.eq(R.mul(R.add(a, b), c), R.add(R.mul(a, c), R.mul(b, c))):
                                h1 = False
                                break
                        if not h1:
                            break
                    if not h1:
                        break
    except Exception:
        h1 = False

    # neg_Q: R is NOT isomorphic to eR x (1-e)R
    try:
        # Generate eR
        eR_elements = []
        for x in R.elements:
            ex = R.mul(e, x)
            if not any(R.eq(ex, y) for y in eR_elements):
                eR_elements.append(ex)
                
        # Generate (1-e)R
        one_minus_e = R.sub(R.one, e)
        omeR_elements = []
        for x in R.elements:
            omex = R.mul(one_minus_e, x)
            if not any(R.eq(omex, y) for y in omeR_elements):
                omeR_elements.append(omex)
                
        # Direct product elements
        prod_elements = list(itertools.product(eR_elements, omeR_elements))
        
        if len(prod_elements) != len(R.elements):
            neg_q = True
        else:
            def prod_add(a, b):
                return (R.add(a[0], b[0]), R.add(a[1], b[1]))
            def prod_mul(a, b):
                return (R.mul(a[0], b[0]), R.mul(a[1], b[1]))
            def prod_eq(a, b):
                return R.eq(a[0], b[0]) and R.eq(a[1], b[1])
                
            # Check if prod has an identity
            has_id = False
            for u in prod_elements:
                is_id = True
                for x in prod_elements:
                    ux = prod_mul(u, x)
                    xu = prod_mul(x, u)
                    if not prod_eq(ux, x) or not prod_eq(xu, x):
                        is_id = False
                        break
                if is_id:
                    has_id = True
                    break
            
            if not has_id:
                neg_q = True
            else:
                n_el = len(R.elements)
                if n_el > 8:
                    neg_q = False
                else:
                    # Full isomorphism check
                    R_add_table = [[0]*n_el for _ in range(n_el)]
                    R_mul_table = [[0]*n_el for _ in range(n_el)]
                    for i in range(n_el):
                        for j in range(n_el):
                            s = R.add(R.elements[i], R.elements[j])
                            m = R.mul(R.elements[i], R.elements[j])
                            R_add_table[i][j] = next(k for k in range(n_el) if R.eq(R.elements[k], s))
                            R_mul_table[i][j] = next(k for k in range(n_el) if R.eq(R.elements[k], m))
                            
                    P_add_table = [[0]*n_el for _ in range(n_el)]
                    P_mul_table = [[0]*n_el for _ in range(n_el)]
                    for i in range(n_el):
                        for j in range(n_el):
                            s = prod_add(prod_elements[i], prod_elements[j])
                            m = prod_mul(prod_elements[i], prod_elements[j])
                            P_add_table[i][j] = next(k for k in range(n_el) if prod_eq(prod_elements[k], s))
                            P_mul_table[i][j] = next(k for k in range(n_el) if prod_eq(prod_elements[k], m))
                            
                    R_zero_idx = next(i for i in range(n_el) if R.eq(R.elements[i], R.zero))
                    R_one_idx = next(i for i in range(n_el) if R.eq(R.elements[i], R.one))
                    
                    P_zero_idx = None
                    for i in range(n_el):
                        if all(P_add_table[i][j] == j and P_add_table[j][i] == j for j in range(n_el)):
                            P_zero_idx = i
                            break
                            
                    P_one_idx = None
                    for i in range(n_el):
                        if all(P_mul_table[i][j] == j and P_mul_table[j][i] == j for j in range(n_el)):
                            P_one_idx = i
                            break
                            
                    if P_zero_idx is None or P_one_idx is None:
                        neg_q = True
                    else:
                        R_rem = [i for i in range(n_el) if i != R_zero_idx and i != R_one_idx]
                        P_rem = [i for i in range(n_el) if i != P_zero_idx and i != P_one_idx]
                        
                        if len(R_rem) != len(P_rem):
                            neg_q = True
                        else:
                            isomorphic = False
                            for p in itertools.permutations(P_rem):
                                mapping = {R_zero_idx: P_zero_idx}
                                if R_one_idx != R_zero_idx:
                                    mapping[R_one_idx] = P_one_idx
                                for i, x in enumerate(R_rem):
                                    mapping[x] = p[i]
                                    
                                add_ok = True
                                for i in range(n_el):
                                    for j in range(n_el):
                                        if mapping[R_add_table[i][j]] != P_add_table[mapping[i]][mapping[j]]:
                                            add_ok = False
                                            break
                                    if not add_ok:
                                        break
                                if not add_ok:
                                    continue
                                    
                                mul_ok = True
                                for i in range(n_el):
                                    for j in range(n_el):
                                        if mapping[R_mul_table[i][j]] != P_mul_table[mapping[i]][mapping[j]]:
                                            mul_ok = False
                                            break
                                    if not mul_ok:
                                        break
                                if mul_ok:
                                    isomorphic = True
                                    break
                            neg_q = not isomorphic
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a ring with identity",
    "¬Q: R is not isomorphic to eR x (1-e)R"
]

N_HYP = 1
NEG_Q_INDEX = 1