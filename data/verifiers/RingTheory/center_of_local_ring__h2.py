import sympy
from sympy import eye, zeros

class ZMod:
    def __init__(self, val, mod):
        self.val = val % mod
        self.mod = mod
        
    def __add__(self, other):
        if isinstance(other, ZMod) and self.mod == other.mod:
            return ZMod(self.val + other.val, self.mod)
        return NotImplemented
        
    def __mul__(self, other):
        if isinstance(other, ZMod) and self.mod == other.mod:
            return ZMod(self.val * other.val, self.mod)
        return NotImplemented
        
    def __neg__(self):
        return ZMod(-self.val, self.mod)
        
    def __sub__(self, other):
        if isinstance(other, ZMod) and self.mod == other.mod:
            return ZMod(self.val - other.val, self.mod)
        return NotImplemented
        
    def __eq__(self, other):
        if isinstance(other, ZMod):
            return self.val == other.val and self.mod == other.mod
        return False
        
    def __hash__(self):
        return hash((self.val, self.mod))
        
    def __repr__(self):
        return f"{self.val} mod {self.mod}"

# Standard finite rings for testing
Z2 = [ZMod(i, 2) for i in range(2)]
Z3 = [ZMod(i, 3) for i in range(3)]
Z4 = [ZMod(i, 4) for i in range(4)]
Z6 = [ZMod(i, 6) for i in range(6)]

# Standard matrices
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a ring",
    "H_2: Z(R) is the center of the ring R",
    "¬Q: Z(R) is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # The witness can be either a collection of elements representing R,
        # or a tuple (R, Z_R) where Z_R is the explicitly provided center.
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (list, tuple, set)):
            R, Z_R_given = witness
            R = list(R)
            Z_R_given = list(Z_R_given)
            given_tuple = True
        elif isinstance(witness, (list, tuple, set)):
            R = list(witness)
            given_tuple = False
        else:
            return [False, False, False]
            
        # Limit size to prevent performance issues with infinite or overly large rings
        if len(R) > 100 or len(R) == 0:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H1: R is a ring
    try:
        h1_ok = False
        zero = None
        for e in R:
            if all(e + x == x for x in R):
                zero = e
                break
        
        one = None
        for e in R:
            if all(e * x == x and x * e == x for x in R):
                one = e
                break
        
        if zero is not None and one is not None:
            try:
                R_set = set(R)
                def in_R(x): return x in R_set
            except TypeError:
                def in_R(x): return x in R

            is_ring_flag = True
            for a in R:
                # Check existence of additive inverse
                if not any(a + x == zero for x in R):
                    is_ring_flag = False
                    break
                for b in R:
                    ab_plus = a + b
                    ab_mul = a * b
                    
                    # Closure
                    if not in_R(ab_plus) or not in_R(ab_mul):
                        is_ring_flag = False
                        break
                        
                    # Commutativity of addition
                    if ab_plus != b + a:
                        is_ring_flag = False
                        break
                        
                    # Associativity and Distributivity
                    for c in R:
                        if ab_plus + c != a + (b + c):
                            is_ring_flag = False
                            break
                        if ab_mul * c != a * (b * c):
                            is_ring_flag = False
                            break
                        if a * (b + c) != ab_mul + a * c:
                            is_ring_flag = False
                            break
                        if ab_plus * c != a * c + b * c:
                            is_ring_flag = False
                            break
                    if not is_ring_flag: break
                if not is_ring_flag: break
            h1_ok = is_ring_flag
    except Exception:
        h1_ok = False

    # H2: Z(R) is the center of R
    try:
        Z_R = []
        for a in R:
            if all(a * x == x * a for x in R):
                Z_R.append(a)
        
        if given_tuple:
            h2_ok = True
            for x in Z_R_given:
                if x not in Z_R:
                    h2_ok = False
                    break
            for x in Z_R:
                if x not in Z_R_given:
                    h2_ok = False
                    break
        else:
            h2_ok = True
    except Exception:
        h2_ok = False

    # ¬Q: Z(R) is not a local ring
    try:
        if not h1_ok or not h2_ok:
            neg_q = False
        else:
            # A commutative ring is local iff the set of its non-units forms an ideal.
            # Since Z(R) is the center, it is always commutative.
            units = []
            for a in Z_R:
                if any(a * b == one for b in Z_R):
                    units.append(a)
            
            non_units = [a for a in Z_R if a not in units]
            
            try:
                non_units_set = set(non_units)
                def in_non_units(x): return x in non_units_set
            except TypeError:
                def in_non_units(x): return x in non_units

            is_local = True
            
            # Check if non-units are closed under addition
            for a in non_units:
                for b in non_units:
                    if not in_non_units(a + b):
                        is_local = False
                        break
                if not is_local: break
                
            # Check if non-units absorb multiplication from Z_R
            if is_local:
                for a in non_units:
                    for r in Z_R:
                        if not in_non_units(a * r):
                            is_local = False
                            break
                    if not is_local: break
            
            # The trivial ring is not considered local
            if one == zero:
                is_local = False
                
            neg_q = not is_local
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]