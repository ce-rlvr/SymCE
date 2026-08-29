import math

class ZnRing:
    def __init__(self, n):
        self.n = n
    def __call__(self, x):
        return (self.n, x % self.n)
    def __eq__(self, other):
        return isinstance(other, ZnRing) and self.n == other.n

# Provide common finite rings as named objects for the witness
Z2 = ZnRing(2)
Z3 = ZnRing(3)
Z4 = ZnRing(4)
Z5 = ZnRing(5)
Z6 = ZnRing(6)
Z8 = ZnRing(8)
Z10 = ZnRing(10)
Z12 = ZnRing(12)

def extract_n_x(witness):
    try:
        if hasattr(witness, "n") and hasattr(witness, "x"):
            return int(witness.n), int(witness.x)
        if isinstance(witness, (tuple, list)) and len(witness) == 2:
            n_val, x_val = witness
            if hasattr(n_val, "n"):
                n_val = n_val.n
            return int(n_val), int(x_val)
    except Exception:
        pass
    return None, None

def conditions(witness):
    n, x = extract_n_x(witness)
    if n is None or x is None:
        return [False, False, False]
        
    try:
        # Restrict n to a reasonable size to ensure fast execution
        if n < 2 or n > 2000:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: R is a commutative Noetherian ring
    # Z/nZ is a finite commutative ring, hence it is always Noetherian.
    try:
        h1 = True
    except Exception:
        h1 = False
        
    # H_2: x is a non-zero, non-unit element of R
    try:
        x_mod = x % n
        h2 = (x_mod != 0) and (math.gcd(x_mod, n) > 1)
    except Exception:
        h2 = False
        
    # ¬Q: x CANNOT be expressed as a finite product of irreducible elements of R
    try:
        x_mod = x % n
        
        # Find all non-units in Z/nZ
        non_units = [i for i in range(n) if math.gcd(i, n) != 1]
        
        # An element is irreducible if it is a non-zero non-unit and CANNOT be 
        # written as a product of two non-units.
        products_of_non_units = set()
        for b in non_units:
            for c in non_units:
                products_of_non_units.add((b * c) % n)
                
        irreducibles = [a for a in non_units if a != 0 and a not in products_of_non_units]
        
        if not irreducibles:
            # If there are no irreducibles, x cannot be factored into them
            # (the empty product is 1, but x is a non-unit, so x != 1)
            neg_q = True
        else:
            # Compute the multiplicative closure of the set of irreducibles
            closure = set(irreducibles)
            queue = list(irreducibles)
            
            while queue:
                curr = queue.pop(0)
                for irr in irreducibles:
                    nxt = (curr * irr) % n
                    if nxt not in closure:
                        closure.add(nxt)
                        queue.append(nxt)
                        
            neg_q = (x_mod not in closure)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative Noetherian ring",
    "H_2: x is a non-zero, non-unit element of R",
    "¬Q: x cannot be expressed as a finite product of irreducible elements of R"
]

N_HYP = 2
NEG_Q_INDEX = 2