import itertools
from sympy import Matrix

class FiniteRing:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = elements
        self.add = add_func
        self.mul = mul_func
        self.zero = zero

def _make_M2_Z2():
    elements = [Matrix(2, 2, entries) for entries in itertools.product(range(2), repeat=4)]
    def add(A, B):
        return (A + B).applyfunc(lambda x: x % 2)
    def mul(A, B):
        return (A * B).applyfunc(lambda x: x % 2)
    zero = Matrix(2, 2, [0, 0, 0, 0])
    return FiniteRing(elements, add, mul, zero)

M2_Z2 = _make_M2_Z2()

def _make_UT2_Z2():
    elements = [Matrix(2, 2, [a, b, 0, c]) for a, b, c in itertools.product(range(2), repeat=3)]
    def add(A, B):
        return (A + B).applyfunc(lambda x: x % 2)
    def mul(A, B):
        return (A * B).applyfunc(lambda x: x % 2)
    zero = Matrix(2, 2, [0, 0, 0, 0])
    return FiniteRing(elements, add, mul, zero)

UT2_Z2 = _make_UT2_Z2()

def _make_Z2():
    return FiniteRing([0, 1], lambda a, b: (a + b) % 2, lambda a, b: (a * b) % 2, 0)
Z2 = _make_Z2()

def _make_Z4():
    return FiniteRing([0, 1, 2, 3], lambda a, b: (a + b) % 4, lambda a, b: (a * b) % 4, 0)
Z4 = _make_Z4()

def _make_Z6():
    return FiniteRing(list(range(6)), lambda a, b: (a + b) % 6, lambda a, b: (a * b) % 6, 0)
Z6 = _make_Z6()

def conditions(witness):
    try:
        if isinstance(witness, FiniteRing):
            ring = witness
            I_elements = [ring.zero]
        else:
            ring, I_elements = witness
            I_elements = list(I_elements)
            
        # H_1: I is an ideal of R
        h1 = True
        if not I_elements:
            h1 = False
        elif ring.zero not in I_elements:
            h1 = False
        else:
            for e in I_elements:
                if e not in ring.elements:
                    h1 = False
            if h1:
                for a in I_elements:
                    for b in I_elements:
                        if ring.add(a, b) not in I_elements:
                            h1 = False
                for i in I_elements:
                    for r in ring.elements:
                        if ring.mul(r, i) not in I_elements:
                            h1 = False
                        if ring.mul(i, r) not in I_elements:
                            h1 = False
                            
        # Compute the radical of I: {x in R | x^n in I for some n >= 1}
        radical_I = []
        for x in ring.elements:
            curr = x
            in_I = False
            for _ in range(len(ring.elements)):
                if curr in I_elements:
                    in_I = True
                    break
                curr = ring.mul(curr, x)
            if in_I:
                radical_I.append(x)
                
        # Find all ideals of R
        principal_ideals = []
        for x in ring.elements:
            ideal = [x]
            for r in ring.elements:
                ideal.append(ring.mul(r, x))
                ideal.append(ring.mul(x, r))
                for r2 in ring.elements:
                    ideal.append(ring.mul(r, ring.mul(x, r2)))
            
            closure = set(ring.elements.index(e) for e in ideal)
            added = True
            while added:
                added = False
                for i1 in list(closure):
                    for i2 in list(closure):
                        e1 = ring.elements[i1]
                        e2 = ring.elements[i2]
                        s = ring.add(e1, e2)
                        idx = ring.elements.index(s)
                        if idx not in closure:
                            closure.add(idx)
                            added = True
            principal_ideals.append(closure)
            
        all_ideals = set()
        for pid in principal_ideals:
            all_ideals.add(tuple(sorted(list(pid))))
            
        added = True
        while added:
            added = False
            current_ideals = list(all_ideals)
            for idl1 in current_ideals:
                for idl2 in current_ideals:
                    sum_ideal = set()
                    for i1 in idl1:
                        for i2 in idl2:
                            e1 = ring.elements[i1]
                            e2 = ring.elements[i2]
                            s = ring.add(e1, e2)
                            sum_ideal.add(ring.elements.index(s))
                    sum_tuple = tuple(sorted(list(sum_ideal)))
                    if sum_tuple not in all_ideals:
                        all_ideals.add(sum_tuple)
                        added = True
                        
        def product_ideal(idl1_indices, idl2_indices):
            prod_set = set()
            for i1 in idl1_indices:
                for i2 in idl2_indices:
                    e1 = ring.elements[i1]
                    e2 = ring.elements[i2]
                    p = ring.mul(e1, e2)
                    prod_set.add(ring.elements.index(p))
            added = True
            while added:
                added = False
                for i1 in list(prod_set):
                    for i2 in list(prod_set):
                        e1 = ring.elements[i1]
                        e2 = ring.elements[i2]
                        s = ring.add(e1, e2)
                        idx = ring.elements.index(s)
                        if idx not in prod_set:
                            prod_set.add(idx)
                            added = True
            return tuple(sorted(list(prod_set)))
            
        def is_prime_ideal(P_indices):
            P_set = set(P_indices)
            for A in all_ideals:
                for B in all_ideals:
                    AB = product_ideal(A, B)
                    if set(AB).issubset(P_set):
                        if not (set(A).issubset(P_set) or set(B).issubset(P_set)):
                            return False
            return True
            
        # Find all prime ideals
        prime_ideals = []
        for idl in all_ideals:
            if len(idl) == len(ring.elements):
                continue  # Prime ideals must be proper
            if is_prime_ideal(idl):
                prime_ideals.append(idl)
                
        # Intersection of all prime ideals containing I
        I_indices = set(ring.elements.index(e) for e in I_elements)
        primes_containing_I = [P for P in prime_ideals if I_indices.issubset(set(P))]
        
        if not primes_containing_I:
            intersection_indices = set(range(len(ring.elements)))
        else:
            intersection_indices = set(primes_containing_I[0])
            for P in primes_containing_I[1:]:
                intersection_indices = intersection_indices.intersection(set(P))
                
        radical_indices = set(ring.elements.index(e) for e in radical_I)
        
        # Conclusion: The radical of I is equal to the intersection of all prime ideals of R that contain I
        q = (radical_indices == intersection_indices)
        neg_q = not q
        
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is an ideal of R",
    "¬Q: The radical of I is NOT equal to the intersection of all prime ideals of R that contain I"
]

N_HYP = 1
NEG_Q_INDEX = 1