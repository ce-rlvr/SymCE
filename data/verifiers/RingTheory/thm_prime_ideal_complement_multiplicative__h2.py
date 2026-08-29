import itertools

class Zn:
    """Representation of the ring of integers modulo n."""
    def __init__(self, n):
        self.n = n
        
    def __repr__(self):
        return f"Zn({self.n})"

# Top-level setup: named object bindings that the witness expression may reference.
Z2 = Zn(2)
Z3 = Zn(3)
Z4 = Zn(4)
Z5 = Zn(5)
Z6 = Zn(6)

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: P is a prime ideal iff R \\setminus P is a multiplicatively closed subset of R (fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        # Witness should be a tuple (R, P) where R is a ring (e.g., Zn(6)) and P is a subset of R.
        if not isinstance(witness, (list, tuple)) or len(witness) != 2:
            return [False, False]
            
        R, P = witness
        
        if hasattr(R, 'n'):
            n = R.n
        elif isinstance(R, int):
            n = R
        else:
            return [False, False]
            
        n = int(n)
        if n < 1:
            return [False, False]
            
        try:
            P = set(P)
        except TypeError:
            return [False, False]
            
        if not P.issubset(set(range(n))):
            return [False, False]
            
        # H1: R is a commutative ring.
        # Z/nZ is always a commutative ring for n >= 1.
        h1 = True
        
        # Check if P is an ideal in Z/nZ
        is_ideal = True
        if not P:
            is_ideal = False
        else:
            # Closed under subtraction
            for a in P:
                for b in P:
                    if (a - b) % n not in P:
                        is_ideal = False
            # Absorbs multiplication from R
            for r in range(n):
                for p in P:
                    if (r * p) % n not in P:
                        is_ideal = False
                        
        # Check if P is a prime ideal
        is_prime = False
        if is_ideal and len(P) < n:  # Must be a proper ideal
            is_prime = True
            for a in range(n):
                for b in range(n):
                    if (a * b) % n in P:
                        if a not in P and b not in P:
                            is_prime = False
                            break
                if not is_prime:
                    break
                    
        # Check if R \setminus P is a multiplicatively closed subset
        complement = set(range(n)) - P
        is_mult_closed = True
        for a in complement:
            for b in complement:
                if (a * b) % n not in complement:
                    is_mult_closed = False
                    break
            if not is_mult_closed:
                break
                
        # The conclusion Q is the equivalence of the two properties
        q = (is_prime == is_mult_closed)
        
        # We want the conclusion to FAIL
        neg_q = not q
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]