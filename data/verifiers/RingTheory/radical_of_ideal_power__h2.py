import sympy
import itertools
import math

class Z_n:
    def __init__(self, n):
        self.n = n
        self.elements = list(range(n))
        self.zero = 0
        self.one = 1
        
    def add(self, a, b): 
        return (a + b) % self.n
        
    def mul(self, a, b): 
        return (a * b) % self.n
        
    def is_commutative(self): 
        return True
        
    def __str__(self): 
        return f"Z_{self.n}"
        
    def __repr__(self): 
        return f"Z_{self.n}"

# Standard rings for potential counterexamples
Z2 = Z_n(2)
Z3 = Z_n(3)
Z4 = Z_n(4)
Z6 = Z_n(6)
Z8 = Z_n(8)
Z12 = Z_n(12)
Z16 = Z_n(16)
ZZ = sympy.ZZ

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple: (R, I, n)
    where R is a ring (e.g., ZZ or Z8), I is a subset of R (list/set), and n is an integer.
    """
    try:
        R, I, n = witness
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative ring
    is_comm_ring = False
    try:
        if R == sympy.ZZ:
            is_comm_ring = True
        elif hasattr(R, 'elements') and hasattr(R, 'add') and hasattr(R, 'mul'):
            is_comm_ring = True
            # Check commutativity of addition
            for a in R.elements:
                for b in R.elements:
                    if R.add(a, b) != R.add(b, a):
                        is_comm_ring = False
            # Check associativity of addition
            if is_comm_ring:
                for a in R.elements:
                    for b in R.elements:
                        for c in R.elements:
                            if R.add(R.add(a, b), c) != R.add(a, R.add(b, c)):
                                is_comm_ring = False
            # Check commutativity of multiplication
            if is_comm_ring:
                for a in R.elements:
                    for b in R.elements:
                        if R.mul(a, b) != R.mul(b, a):
                            is_comm_ring = False
            # Check associativity of multiplication
            if is_comm_ring:
                for a in R.elements:
                    for b in R.elements:
                        for c in R.elements:
                            if R.mul(R.mul(a, b), c) != R.mul(a, R.mul(b, c)):
                                is_comm_ring = False
            # Check distributivity
            if is_comm_ring:
                for a in R.elements:
                    for b in R.elements:
                        for c in R.elements:
                            if R.mul(a, R.add(b, c)) != R.add(R.mul(a, b), R.mul(a, c)):
                                is_comm_ring = False
            # Check zero exists and additive inverses
            if is_comm_ring:
                has_zero = False
                z_elem = None
                for z in R.elements:
                    if all(R.add(a, z) == a for a in R.elements):
                        has_zero = True
                        z_elem = z
                        break
                if not has_zero:
                    is_comm_ring = False
                else:
                    for a in R.elements:
                        has_inv = False
                        for b in R.elements:
                            if R.add(a, b) == z_elem:
                                has_inv = True
                                break
                        if not has_inv:
                            is_comm_ring = False
    except Exception:
        is_comm_ring = False
        
    # H_2: n is an integer strictly greater than 0
    try:
        n_gt_0 = isinstance(n, int) and n > 0
    except Exception:
        n_gt_0 = False
        
    # ¬Q: The radical of the ideal I^n is NOT equal to the radical of I
    neg_q = False
    try:
        if R == sympy.ZZ:
            if n <= 0:
                I_n_set = set()
            elif not I:
                I_n_set = set()
            else:
                I_n_set = set(I)
                for _ in range(n - 1):
                    next_set = set()
                    for a in I_n_set:
                        for b in I:
                            next_set.add(a * b)
                    I_n_set = next_set
                    
            g = 0
            for x in I_n_set:
                g = math.gcd(g, x)
            
            rad_I = set()
            for x in I:
                if x == 0:
                    rad_I.add(0)
                elif x == 1:
                    rad_I.add(1)
                    rad_I.add(-1)
                elif x == -1:
                    rad_I.add(-1)
                else:
                    for y in range(-abs(x), abs(x) + 1):
                        if y in (0, 1, -1):
                            continue
                        curr = y
                        while abs(curr) <= abs(x):
                            if curr == x:
                                rad_I.add(y)
                                break
                            curr *= y
            
            # The radical of a non-zero ideal in ZZ is infinite, while rad_I is finite.
            if g != 0:
                neg_q = True
            else:
                neg_q = False
                
        elif hasattr(R, 'elements'):
            if n <= 0:
                I_n_set = set()
            elif not I:
                I_n_set = set()
            else:
                I_n_set = set(I)
                for _ in range(n - 1):
                    next_set = set()
                    for a in I_n_set:
                        for b in I:
                            next_set.add(R.mul(a, b))
                    I_n_set = next_set
                
            ideal_In = set(I_n_set)
            z_elem = None
            for z in R.elements:
                if all(R.add(a, z) == a for a in R.elements):
                    z_elem = z
                    break
            if z_elem is not None:
                ideal_In.add(z_elem)
                
            changed = True
            while changed:
                changed = False
                new_ideal = set(ideal_In)
                for x in ideal_In:
                    for y in ideal_In:
                        new_ideal.add(R.add(x, y))
                    for r in R.elements:
                        new_ideal.add(R.mul(r, x))
                if len(new_ideal) > len(ideal_In):
                    ideal_In = new_ideal
                    changed = True
                    
            rad_ideal_In = set()
            for x in R.elements:
                curr = x
                for _ in range(len(R.elements)):
                    if curr in ideal_In:
                        rad_ideal_In.add(x)
                        break
                    curr = R.mul(curr, x)
                    
            rad_I = set()
            for x in R.elements:
                curr = x
                for _ in range(len(R.elements)):
                    if curr in I:
                        rad_I.add(x)
                        break
                    curr = R.mul(curr, x)
                    
            neg_q = (rad_ideal_In != rad_I)
    except Exception:
        neg_q = False
        
    return [is_comm_ring, n_gt_0, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: n is an integer strictly greater than 0",
    "¬Q: The radical of the ideal I^n is not equal to the radical of I"
]

N_HYP = 2
NEG_Q_INDEX = 2