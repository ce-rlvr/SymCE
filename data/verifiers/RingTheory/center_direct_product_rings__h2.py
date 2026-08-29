import itertools

# Top-level setup: named object bindings that the witness expression may reference.
def make_Zn(n):
    elements = list(range(n))
    add = {(a, b): (a + b) % n for a in elements for b in elements}
    mul = {(a, b): (a * b) % n for a in elements for b in elements}
    return (elements, add, mul)

def direct_product(R1, R2):
    e1, a1, m1 = R1
    e2, a2, m2 = R2
    elements = list(itertools.product(e1, e2))
    add = { (x, y): (a1[(x[0], y[0])], a2[(x[1], y[1])]) for x in elements for y in elements }
    mul = { (x, y): (m1[(x[0], y[0])], m2[(x[1], y[1])]) for x in elements for y in elements }
    return (elements, add, mul)

def make_M2_Z2():
    elements = list(itertools.product(range(2), repeat=4))
    def add_mat(A, B):
        return tuple((a + b) % 2 for a, b in zip(A, B))
    def mul_mat(A, B):
        return (
            (A[0]*B[0] + A[1]*B[2]) % 2,
            (A[0]*B[1] + A[1]*B[3]) % 2,
            (A[2]*B[0] + A[3]*B[2]) % 2,
            (A[2]*B[1] + A[3]*B[3]) % 2
        )
    add = {(A, B): add_mat(A, B) for A in elements for B in elements}
    mul = {(A, B): mul_mat(A, B) for A in elements for B in elements}
    return (elements, add, mul)

Z1 = make_Zn(1)
Z2 = make_Zn(2)
Z3 = make_Zn(3)
Z4 = make_Zn(4)
Z5 = make_Zn(5)
Z6 = make_Zn(6)
M2_Z2 = make_M2_Z2()

def is_ring(R):
    try:
        elements, add, mul = R
        elements = list(elements)
        if not elements: 
            return False
        
        # closure
        for a in elements:
            for b in elements:
                if (a, b) not in add or add[(a, b)] not in elements: return False
                if (a, b) not in mul or mul[(a, b)] not in elements: return False
                
        # add associativity
        for a in elements:
            for b in elements:
                for c in elements:
                    if add[(add[(a, b)], c)] != add[(a, add[(b, c)])]: return False
                    
        # add commutativity
        for a in elements:
            for b in elements:
                if add[(a, b)] != add[(b, a)]: return False
                
        # add identity
        zero = None
        for e in elements:
            if all(add[(e, a)] == a for a in elements):
                zero = e
                break
        if zero is None: return False
        
        # add inverse
        for a in elements:
            if not any(add[(a, b)] == zero for b in elements): return False
            
        # mul associativity
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul[(mul[(a, b)], c)] != mul[(a, mul[(b, c)])]: return False
                    
        # distributivity
        for a in elements:
            for b in elements:
                for c in elements:
                    if mul[(a, add[(b, c)])] != add[(mul[(a, b)], mul[(a, c)])]: return False
                    if mul[(add[(a, b)], c)] != add[(mul[(a, c)], mul[(b, c)])]: return False
                    
        # mul identity
        one = None
        for e in elements:
            if all(mul[(e, a)] == a and mul[(a, e)] == a for a in elements):
                one = e
                break
        if one is None: return False
        
        return True
    except Exception:
        return False

def center_set(R):
    elements, add, mul = R
    c = set()
    for x in elements:
        if all(mul[(x, a)] == mul[(a, x)] for a in elements):
            c.add(x)
    return c

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            R1 = witness.get('R1')
            R2 = witness.get('R2')
            R = witness.get('R')
        else:
            if len(witness) == 3:
                R1, R2, R = witness
            else:
                return [False, False]
    except Exception:
        return [False, False]

    try:
        h1 = is_ring(R1) and is_ring(R2)
    except Exception:
        h1 = False

    try:
        # R must also be a ring for Z(R) to be well-defined
        if not is_ring(R):
            neg_q = False
        else:
            c_R = center_set(R)
            c_R1 = center_set(R1)
            c_R2 = center_set(R2)
            prod = set(itertools.product(c_R1, c_R2))
            neg_q = (c_R != prod)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings",
    "¬Q: Z(R) is not equal to Z(R1) x Z(R2)"
]

N_HYP = 1
NEG_Q_INDEX = 1