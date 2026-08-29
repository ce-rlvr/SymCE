import itertools

class FiniteRing:
    def __init__(self, elements, add_func, mul_func, zero):
        self.elements = list(elements)
        self.add = add_func
        self.mul = mul_func
        self.zero = zero

    def neg(self, a):
        for b in self.elements:
            if self.add(a, b) == self.zero:
                return b
        return self.zero

    def is_proper_ideal(self, subset):
        try:
            subset = list(subset)
        except Exception:
            return False
        if self.zero not in subset:
            return False
        if len(subset) == len(self.elements):
            return False
        for a in subset:
            for b in subset:
                if self.add(a, b) not in subset:
                    return False
        for r in self.elements:
            for a in subset:
                if self.mul(r, a) not in subset:
                    return False
                if self.mul(a, r) not in subset:
                    return False
        return True

    def is_prime_ideal(self, p_subset):
        try:
            p_subset = list(p_subset)
        except Exception:
            return False
        if not self.is_proper_ideal(p_subset):
            return False
        for a in self.elements:
            if a in p_subset:
                continue
            for b in self.elements:
                if b in p_subset:
                    continue
                a_R_b_in_P = True
                for r in self.elements:
                    arb = self.mul(self.mul(a, r), b)
                    if arb not in p_subset:
                        a_R_b_in_P = False
                        break
                if a_R_b_in_P:
                    return False
        return True

    def quotient_is_integral_domain(self, p_subset):
        try:
            p_subset = list(p_subset)
        except Exception:
            return False
        if len(p_subset) == len(self.elements):
            return False
        
        # Check if R/P is commutative
        for a in self.elements:
            for b in self.elements:
                diff = self.add(self.mul(a, b), self.neg(self.mul(b, a)))
                if diff not in p_subset:
                    return False
                    
        # Check if R/P has an identity
        has_identity = False
        for e in self.elements:
            is_id = True
            for a in self.elements:
                if self.add(self.mul(e, a), self.neg(a)) not in p_subset:
                    is_id = False
                    break
                if self.add(self.mul(a, e), self.neg(a)) not in p_subset:
                    is_id = False
                    break
            if is_id:
                if e not in p_subset:
                    has_identity = True
                    break
        if not has_identity:
            return False
            
        # Check for zero divisors
        for a in self.elements:
            for b in self.elements:
                if self.mul(a, b) in p_subset:
                    if a not in p_subset and b not in p_subset:
                        return False
        return True

# Setup standard rings for the witness namespace
_m2f2_elements = list(itertools.product([0, 1], repeat=4))
def _m2f2_add(A, B):
    return tuple((a + b) % 2 for a, b in zip(A, B))
def _m2f2_mul(A, B):
    return (
        (A[0]*B[0] + A[1]*B[2]) % 2,
        (A[0]*B[1] + A[1]*B[3]) % 2,
        (A[2]*B[0] + A[3]*B[2]) % 2,
        (A[2]*B[1] + A[3]*B[3]) % 2
    )

M2F2 = FiniteRing(_m2f2_elements, _m2f2_add, _m2f2_mul, (0, 0, 0, 0))
zero_ideal = [(0, 0, 0, 0)]

_z4_elements = [0, 1, 2, 3]
def _z4_add(a, b): return (a + b) % 4
def _z4_mul(a, b): return (a * b) % 4
Z4 = FiniteRing(_z4_elements, _z4_add, _z4_mul, 0)

_z6_elements = [0, 1, 2, 3, 4, 5]
def _z6_add(a, b): return (a + b) % 6
def _z6_mul(a, b): return (a * b) % 6
Z6 = FiniteRing(_z6_elements, _z6_add, _z6_mul, 0)


def conditions(witness) -> list[bool]:
    """
    Given a witness (ring, ideal), checks if it is a valid counterexample.
    Returns [H_1_ok, neg_Q_ok].
    """
    try:
        ring, ideal = witness
        h1 = ring.is_proper_ideal(ideal)
    except Exception:
        h1 = False

    try:
        ring, ideal = witness
        is_prime = ring.is_prime_ideal(ideal)
        is_domain = ring.quotient_is_integral_domain(ideal)
        # The conclusion is: R/P is an integral domain iff P is a prime ideal
        conclusion = (is_domain == is_prime)
        neg_q = not conclusion
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: P is a proper ideal of R",
    "¬Q: It is not the case that (R/P is an integral domain iff P is a prime ideal)"
]

N_HYP = 1
NEG_Q_INDEX = 1