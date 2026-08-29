import itertools

class FiniteRing:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func
        self.zero = zero

    def is_ideal(self, subset):
        subset = list(subset)
        if self.zero not in subset:
            return False
        # Check closure under negation
        for a in subset:
            has_neg = False
            for b in subset:
                if self.add(a, b) == self.zero:
                    has_neg = True
                    break
            if not has_neg:
                return False
        # Check closure under addition
        for a in subset:
            for b in subset:
                if self.add(a, b) not in subset:
                    return False
        # Check absorption
        for r in self.elements:
            for x in subset:
                if self.mul(r, x) not in subset:
                    return False
                if self.mul(x, r) not in subset:
                    return False
        return True

    def is_prime_ideal(self, subset):
        if not self.is_ideal(subset):
            return False
        subset = set(subset)
        
        cache = {}
        def principal_ideal(x):
            if x in cache:
                return cache[x]
            ideal = {x, self.zero}
            while True:
                new_ideal = set(ideal)
                for u in ideal:
                    for v in ideal:
                        new_ideal.add(self.add(u, v))
                for u in ideal:
                    for r in self.elements:
                        if self.add(u, r) == self.zero:
                            new_ideal.add(r)
                for u in ideal:
                    for r in self.elements:
                        new_ideal.add(self.mul(r, u))
                        new_ideal.add(self.mul(u, r))
                if len(new_ideal) == len(ideal):
                    cache[x] = ideal
                    return ideal
                ideal = new_ideal

        for a in self.elements:
            if a in subset: 
                continue
            I_a = principal_ideal(a)
            for b in self.elements:
                if b in subset: 
                    continue
                I_b = principal_ideal(b)
                
                contained = True
                for x in I_a:
                    for y in I_b:
                        if self.mul(x, y) not in subset:
                            contained = False
                            break
                    if not contained:
                        break
                
                if contained:
                    return False
                    
        return True

    def quotient_embeds_in_field(self, subset):
        subset = set(subset)
        classes = []
        for a in self.elements:
            cls = frozenset(self.add(a, p) for p in subset)
            if cls not in classes:
                classes.append(cls)
        
        if len(classes) <= 1:
            return False
            
        # Check if addition is commutative (required for standard rings)
        for a in self.elements:
            for b in self.elements:
                if self.add(a, b) != self.add(b, a):
                    return False
                    
        # Check commutativity of R/P
        for c1 in classes:
            for c2 in classes:
                a = next(iter(c1))
                b = next(iter(c2))
                ab = self.mul(a, b)
                ba = self.mul(b, a)
                if frozenset(self.add(ab, p) for p in subset) != frozenset(self.add(ba, p) for p in subset):
                    return False
                    
        # Find identity in R/P
        identity = None
        for c_e in classes:
            e = next(iter(c_e))
            is_id = True
            for c_a in classes:
                a = next(iter(c_a))
                ea = self.mul(e, a)
                if frozenset(self.add(ea, p) for p in subset) != c_a:
                    is_id = False
                    break
            if is_id:
                identity = c_e
                break
                
        if identity is None:
            return False
            
        zero_class = frozenset(subset)
        if identity == zero_class:
            return False
            
        # Check if every non-zero element has an inverse in R/P
        for c_a in classes:
            if c_a == zero_class:
                continue
            a = next(iter(c_a))
            has_inv = False
            for c_b in classes:
                b = next(iter(c_b))
                ab = self.mul(a, b)
                if frozenset(self.add(ab, p) for p in subset) == identity:
                    has_inv = True
                    break
            if not has_inv:
                return False
                
        return True

# Setup standard counterexample ring: M_2(F_2)
_m2_elements = list(itertools.product([0, 1], repeat=4))
def _m2_add(a, b):
    return tuple((x + y) % 2 for x, y in zip(a, b))
def _m2_mul(a, b):
    return (
        (a[0]*b[0] + a[1]*b[2]) % 2,
        (a[0]*b[1] + a[1]*b[3]) % 2,
        (a[2]*b[0] + a[3]*b[2]) % 2,
        (a[2]*b[1] + a[3]*b[3]) % 2
    )
_m2_zero = (0, 0, 0, 0)

M2_F2 = FiniteRing(_m2_elements, _m2_add, _m2_mul, _m2_zero)
zero_ideal = [_m2_zero]

# Setup some commutative rings for convenience
_z4_elements = [0, 1, 2, 3]
def _z4_add(a, b): return (a + b) % 4
def _z4_mul(a, b): return (a * b) % 4
Z4 = FiniteRing(_z4_elements, _z4_add, _z4_mul, 0)

_z6_elements = [0, 1, 2, 3, 4, 5]
def _z6_add(a, b): return (a + b) % 6
def _z6_mul(a, b): return (a * b) % 6
Z6 = FiniteRing(_z6_elements, _z6_add, _z6_mul, 0)


def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should be a tuple (R, P) where R is a FiniteRing and P is a list of elements.
    """
    try:
        R, P = witness
    except Exception:
        return [False, False]
        
    try:
        h1 = R.is_ideal(P) and len(P) < len(R.elements)
    except Exception:
        h1 = False
        
    try:
        is_prime = R.is_prime_ideal(P)
        embeds = R.quotient_embeds_in_field(P)
        # The conclusion is: P is prime iff it embeds in a field.
        # The negated conclusion is True when this equivalence fails.
        neg_q = is_prime != embeds
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a proper ideal of R",
    "¬Q: The equivalence (P is prime iff there exists a field F and hom phi with ker(phi) = P) fails"
]

N_HYP = 1
NEG_Q_INDEX = 1