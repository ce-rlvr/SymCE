import itertools

class F2_MatrixRingElement:
    def __init__(self, a, b, c):
        self.a = a % 2
        self.b = b % 2
        self.c = c % 2
        
    def __add__(self, other):
        return F2_MatrixRingElement(self.a + other.a, self.b + other.b, self.c + other.c)
        
    def __mul__(self, other):
        return F2_MatrixRingElement(
            self.a * other.a,
            self.a * other.b + self.b * other.a,
            self.a * other.c + self.c * other.a
        )
        
    def __eq__(self, other):
        if not isinstance(other, F2_MatrixRingElement):
            return False
        return self.a == other.a and self.b == other.b and self.c == other.c
        
    def __hash__(self):
        return hash((self.a, self.b, self.c))
        
    def __repr__(self):
        return f"F2_MatrixRingElement({self.a}, {self.b}, {self.c})"

R_elements = [F2_MatrixRingElement(a, b, c) for a in (0, 1) for b in (0, 1) for c in (0, 1)]
a_elem = F2_MatrixRingElement(0, 1, 0)
b_elem = F2_MatrixRingElement(0, 0, 1)
d_elem = F2_MatrixRingElement(1, 0, 0)

def conditions(witness) -> list[bool]:
    try:
        R, a, b, d = witness
    except Exception:
        return [False, False, False]
        
    try:
        zero = next(x for x in R if all(x + y == y for y in R))
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (a in R) and (b in R) and (a != zero) and (b != zero)
    except Exception:
        h1 = False
        
    try:
        def divides(x, y):
            return any(x * k == y for k in R)
            
        d_div_a = divides(d, a)
        d_div_b = divides(d, b)
        
        is_gcd = d_div_a and d_div_b
        if is_gcd:
            for c in R:
                if divides(c, a) and divides(c, b):
                    if not divides(c, d):
                        is_gcd = False
                        break
        h2 = is_gcd
    except Exception:
        h2 = False
        
    try:
        ideal_b = []
        for x in R:
            bx = b * x
            if bx not in ideal_b:
                ideal_b.append(bx)
                
        ideal_d = []
        for x in R:
            dx = d * x
            if dx not in ideal_d:
                ideal_d.append(dx)
                
        cosets_b = []
        for x in R:
            coset = []
            for y in ideal_b:
                s = x + y
                if s not in coset:
                    coset.append(s)
            is_new = True
            for c in cosets_b:
                if len(c) == len(coset) and all(e in c for e in coset):
                    is_new = False
                    break
            if is_new:
                cosets_b.append(coset)
                
        M_elements = []
        for coset in cosets_b:
            m = coset[0]
            am = a * m
            if am in ideal_b:
                M_elements.append(coset)
                
        cosets_d = []
        for x in R:
            coset = []
            for y in ideal_d:
                s = x + y
                if s not in coset:
                    coset.append(s)
            is_new = True
            for c in cosets_d:
                if len(c) == len(coset) and all(e in c for e in coset):
                    is_new = False
                    break
            if is_new:
                cosets_d.append(coset)
        N_elements = cosets_d
        
        def get_coset(x, cosets):
            for c in cosets:
                if x in c:
                    return c
            return None
            
        is_iso = False
        if len(M_elements) == len(N_elements):
            for perm in itertools.permutations(range(len(N_elements))):
                mapping = {i: perm[i] for i in range(len(M_elements))}
                
                valid = True
                for i in range(len(M_elements)):
                    for j in range(len(M_elements)):
                        c1 = M_elements[i]
                        c2 = M_elements[j]
                        x = c1[0]
                        y = c2[0]
                        c3 = get_coset(x + y, M_elements)
                        if c3 is None:
                            valid = False
                            break
                        idx3 = M_elements.index(c3)
                        
                        mc1 = N_elements[mapping[i]]
                        mc2 = N_elements[mapping[j]]
                        mx = mc1[0]
                        my = mc2[0]
                        mc3 = get_coset(mx + my, N_elements)
                        if mc3 is None:
                            valid = False
                            break
                        midx3 = N_elements.index(mc3)
                        
                        if mapping[idx3] != midx3:
                            valid = False
                            break
                    if not valid:
                        break
                if not valid:
                    continue
                    
                for r in R:
                    for i in range(len(M_elements)):
                        c1 = M_elements[i]
                        x = c1[0]
                        c3 = get_coset(r * x, M_elements)
                        if c3 is None:
                            valid = False
                            break
                        idx3 = M_elements.index(c3)
                        
                        mc1 = N_elements[mapping[i]]
                        mx = mc1[0]
                        mc3 = get_coset(r * mx, N_elements)
                        if mc3 is None:
                            valid = False
                            break
                        midx3 = N_elements.index(mc3)
                        
                        if mapping[idx3] != midx3:
                            valid = False
                            break
                    if not valid:
                        break
                        
                if valid:
                    is_iso = True
                    break
                    
        neg_q = not is_iso
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: a and b are non-zero elements of R",
    "H_2: d is a greatest common divisor of a and b",
    "¬Q: Hom_R(R/<a>, R/<b>) is not isomorphic to R/<d>"
]

N_HYP = 2
NEG_Q_INDEX = 2