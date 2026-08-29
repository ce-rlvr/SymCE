import itertools
from sympy import ImmutableMatrix

class FiniteRing:
    def __init__(self, elements, add, mul, zero, one):
        self.elements = elements
        self.add = add
        self.mul = mul
        self.zero = zero
        self.one = one
        self.elem_to_idx = {e: i for i, e in enumerate(elements)}
        self._ideals = None

    def get_ideals(self):
        if self._ideals is not None:
            return self._ideals
        
        n = len(self.elements)
        
        def ideal_generated_by(S):
            closure = set(S)
            closure.add(self.elem_to_idx[self.zero])
            changed = True
            while changed:
                old_len = len(closure)
                new_elements = set()
                for x_idx in closure:
                    for y_idx in closure:
                        s = self.add(self.elements[x_idx], self.elements[y_idx])
                        new_elements.add(self.elem_to_idx[s])
                    for r_idx in range(n):
                        p1 = self.mul(self.elements[r_idx], self.elements[x_idx])
                        p2 = self.mul(self.elements[x_idx], self.elements[r_idx])
                        new_elements.add(self.elem_to_idx[p1])
                        new_elements.add(self.elem_to_idx[p2])
                closure.update(new_elements)
                if len(closure) == old_len:
                    break
            return frozenset(closure)

        ideals = set()
        for i in range(n):
            ideals.add(ideal_generated_by([i]))
        
        changed = True
        while changed:
            old_len = len(ideals)
            new_ideals = set()
            for I1 in ideals:
                for I2 in ideals:
                    sum_ideal = set()
                    for x in I1:
                        for y in I2:
                            s = self.add(self.elements[x], self.elements[y])
                            sum_ideal.add(self.elem_to_idx[s])
                    new_ideals.add(frozenset(sum_ideal))
            ideals.update(new_ideals)
            if len(ideals) == old_len:
                break
                
        self._ideals = ideals
        return ideals

def _add_m2(A, B):
    return ImmutableMatrix((A + B).applyfunc(lambda x: x % 2))

def _mul_m2(A, B):
    return ImmutableMatrix((A * B).applyfunc(lambda x: x % 2))

_m2_elements = [ImmutableMatrix(2, 2, [a, b, c, d]) for a, b, c, d in itertools.product([0, 1], repeat=4)]
M2_Z2 = FiniteRing(
    elements=_m2_elements,
    add=_add_m2,
    mul=_mul_m2,
    zero=ImmutableMatrix(2, 2, [0, 0, 0, 0]),
    one=ImmutableMatrix(2, 2, [1, 0, 0, 1])
)

_z2_elements = [0, 1]
Z2 = FiniteRing(
    elements=_z2_elements,
    add=lambda x, y: (x + y) % 2,
    mul=lambda x, y: (x * y) % 2,
    zero=0,
    one=1
)

_z4_elements = [0, 1, 2, 3]
Z4 = FiniteRing(
    elements=_z4_elements,
    add=lambda x, y: (x + y) % 4,
    mul=lambda x, y: (x * y) % 4,
    zero=0,
    one=1
)

_z6_elements = [0, 1, 2, 3, 4, 5]
Z6 = FiniteRing(
    elements=_z6_elements,
    add=lambda x, y: (x + y) % 6,
    mul=lambda x, y: (x * y) % 6,
    zero=0,
    one=1
)

def conditions(witness):
    try:
        ideals = witness.get_ideals()
        
        def ideal_product(I, J):
            prod_elements = set()
            for x in I:
                for y in J:
                    p = witness.mul(witness.elements[x], witness.elements[y])
                    prod_elements.add(witness.elem_to_idx[p])
            
            containing_ideals = [ideal for ideal in ideals if prod_elements.issubset(ideal)]
            if not containing_ideals:
                return frozenset(range(len(witness.elements)))
            res = set(containing_ideals[0])
            for ideal in containing_ideals[1:]:
                res.intersection_update(ideal)
            return frozenset(res)
        
        prime_ideals = []
        full_ring = frozenset(range(len(witness.elements)))
        
        for P in ideals:
            if P == full_ring:
                continue
            is_prime = True
            for I in ideals:
                for J in ideals:
                    if ideal_product(I, J).issubset(P):
                        if not (I.issubset(P) or J.issubset(P)):
                            is_prime = False
                            break
                if not is_prime:
                    break
            if is_prime:
                prime_ideals.append(P)
                
        h1_ok = (len(prime_ideals) == 1)
    except Exception:
        h1_ok = False

    try:
        def is_unit(x_idx):
            x = witness.elements[x_idx]
            for y in witness.elements:
                if witness.mul(x, y) == witness.one and witness.mul(y, x) == witness.one:
                    return True
            return False
            
        def is_nilpotent(x_idx):
            x = witness.elements[x_idx]
            curr = x
            if curr == witness.zero:
                return True
            for _ in range(len(witness.elements)):
                curr = witness.mul(curr, x)
                if curr == witness.zero:
                    return True
            return False
            
        neg_q_ok = False
        for i in range(len(witness.elements)):
            if not is_unit(i) and not is_nilpotent(i):
                neg_q_ok = True
                break
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R has exactly one prime ideal",
    "¬Q: There exists an element in R that is neither a unit nor nilpotent"
]

N_HYP = 1
NEG_Q_INDEX = 1