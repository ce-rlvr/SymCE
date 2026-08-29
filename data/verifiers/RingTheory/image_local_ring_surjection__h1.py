import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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

CONDITION_LABELS = [
    "H_1: R is a local ring",
    "H_2: S is a commutative ring with identity",
    "H_3: S is not the zero ring",
    "H_4: f is a surjective ring homomorphism from R to S",
    "¬Q: S is not a local ring"
]

N_HYP = 4
NEG_Q_INDEX = 4

def conditions(witness) -> list[bool]:
    # Check if witness is a mock object with pre-evaluated properties
    if hasattr(witness, 'H1') and hasattr(witness, 'neg_Q'):
        try:
            h1 = witness.H1() if callable(witness.H1) else witness.H1
            h2 = witness.H2() if callable(witness.H2) else witness.H2
            h3 = witness.H3() if callable(witness.H3) else witness.H3
            h4 = witness.H4() if callable(witness.H4) else witness.H4
            neg_q = witness.neg_Q() if callable(witness.neg_Q) else witness.neg_Q
            return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
        except Exception:
            pass

    # Extract R, S, f
    R, S, f = None, None, None
    if isinstance(witness, tuple) and len(witness) == 3:
        R, S, f = witness
    else:
        try:
            R = witness.R
            S = witness.S
            f = witness.f
        except Exception:
            pass

    def check_local(ring):
        if ring is None: return False
        if hasattr(ring, 'is_local'):
            val = ring.is_local
            return val() if callable(val) else val
        if hasattr(ring, 'is_local_ring'):
            val = ring.is_local_ring
            return val() if callable(val) else val
        if hasattr(ring, 'is_Field') and ring.is_Field:
            return True
            
        try:
            elements = list(ring.elements)
            zero = None
            for e in elements:
                if all(ring.add(e, x) == x for x in elements):
                    zero = e
                    break
            if zero is None: return False
            
            one = None
            for e in elements:
                if all(ring.mul(e, x) == x and ring.mul(x, e) == x for x in elements):
                    one = e
                    break
                    
            if one is not None:
                if zero == one:
                    return False
                non_units = []
                for x in elements:
                    is_unit = False
                    for y in elements:
                        if ring.mul(x, y) == one and ring.mul(y, x) == one:
                            is_unit = True
                            break
                    if not is_unit:
                        non_units.append(x)
                
                for a in non_units:
                    for b in non_units:
                        if ring.add(a, b) not in non_units:
                            return False
                for a in non_units:
                    for r in elements:
                        if ring.mul(a, r) not in non_units or ring.mul(r, a) not in non_units:
                            return False
                return True
            else:
                ideals = []
                n = len(elements)
                for i in range(1, 1 << n):
                    subset = [elements[j] for j in range(n) if (i & (1 << j))]
                    if len(subset) == n: continue
                    is_ideal = True
                    for a in subset:
                        for b in subset:
                            if ring.add(a, b) not in subset:
                                is_ideal = False
                                break
                        if not is_ideal: break
                    if not is_ideal: continue
                    for a in subset:
                        for r in elements:
                            if ring.mul(a, r) not in subset or ring.mul(r, a) not in subset:
                                is_ideal = False
                                break
                        if not is_ideal: break
                    if is_ideal:
                        ideals.append(subset)
                max_ideals = []
                for id1 in ideals:
                    is_max = True
                    for id2 in ideals:
                        if id1 != id2 and all(x in id2 for x in id1):
                            is_max = False
                            break
                    if is_max:
                        max_ideals.append(id1)
                return len(max_ideals) == 1
        except Exception:
            pass
        return False

    def check_commutative_with_identity(ring):
        if ring is None: return False
        if hasattr(ring, 'is_commutative') and hasattr(ring, 'has_identity'):
            c = ring.is_commutative
            c = c() if callable(c) else c
            i = ring.has_identity
            i = i() if callable(i) else i
            return bool(c and i)
            
        try:
            elements = list(ring.elements)
            for a in elements:
                for b in elements:
                    if ring.mul(a, b) != ring.mul(b, a):
                        return False
            for e in elements:
                if all(ring.mul(e, x) == x for x in elements):
                    return True
            return False
        except Exception:
            pass
        return False

    def check_not_zero_ring(ring):
        if ring is None: return False
        if hasattr(ring, 'is_zero_ring'):
            val = ring.is_zero_ring
            return not (val() if callable(val) else val)
        if hasattr(ring, 'is_Field') and ring.is_Field:
            return True
        try:
            elements = list(ring.elements)
            return len(elements) > 1
        except Exception:
            pass
        if ring.__class__.__name__ in ['IntegerRing', 'RationalField', 'RealField', 'ComplexField', 'PolynomialRing']:
            return True
        return False

    def check_surjective_homomorphism(R, S, f):
        if f is None: return False
        if hasattr(f, 'is_surjective_homomorphism'):
            val = f.is_surjective_homomorphism
            return val() if callable(val) else val
        if hasattr(witness, 'is_surjective_homomorphism'):
            val = witness.is_surjective_homomorphism
            return val() if callable(val) else val
            
        try:
            R_elems = list(R.elements)
            S_elems = list(S.elements)
            
            image = []
            for r in R_elems:
                s = f(r) if callable(f) else f[r]
                if s not in image:
                    image.append(s)
            if len(image) != len(S_elems):
                return False
                
            for a in R_elems:
                for b in R_elems:
                    fa = f(a) if callable(f) else f[a]
                    fb = f(b) if callable(f) else f[b]
                    
                    ab_add = R.add(a, b)
                    fab_add = f(ab_add) if callable(f) else f[ab_add]
                    if S.add(fa, fb) != fab_add:
                        return False
                        
                    ab_mul = R.mul(a, b)
                    fab_mul = f(ab_mul) if callable(f) else f[ab_mul]
                    if S.mul(fa, fb) != fab_mul:
                        return False
            return True
        except Exception:
            pass
        return False

    try:
        h1 = bool(check_local(R))
    except Exception:
        h1 = False

    try:
        h2 = bool(check_commutative_with_identity(S))
    except Exception:
        h2 = False

    try:
        h3 = bool(check_not_zero_ring(S))
    except Exception:
        h3 = False

    try:
        h4 = bool(check_surjective_homomorphism(R, S, f))
    except Exception:
        h4 = False

    try:
        neg_q = not bool(check_local(S))
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]