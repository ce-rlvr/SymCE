import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import factorint

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
    "H_1: R is a commutative ring",
    "H_2: R is a reduced ring",
    "¬Q: The localized ring S^{-1}R is not a reduced ring"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        # The witness can be a tuple (R, S) or just R (with S implicitly the set of non-zero elements)
        if isinstance(witness, tuple) and len(witness) == 2:
            R_obj, S_obj = witness
        else:
            R_obj = witness
            S_obj = None

        # Case 1: R is represented as an integer n (for the ring Z/nZ)
        if isinstance(R_obj, int):
            n = R_obj
            # H1: Z/nZ is a commutative ring (valid for n > 1)
            h1 = (n > 1)
            
            # H2: Z/nZ is a reduced ring iff n is square-free
            factors = factorint(n)
            h2 = all(v == 1 for v in factors.values())
            
            if S_obj is None:
                # Implicitly, S is the set of all non-zero elements
                S = set(range(1, n))
            else:
                S = set(s % n for s in S_obj)
                
            # Check if S is a valid multiplicative set
            is_mult_closed = True
            if 1 not in S:
                is_mult_closed = False
            else:
                for a in S:
                    for b in S:
                        if (a * b) % n not in S:
                            is_mult_closed = False
                            break
                    if not is_mult_closed:
                        break
                        
            # ¬Q: S^{-1}R is NOT a reduced ring.
            # This happens if S is not multiplicatively closed (so S^{-1}R is not a valid ring construction),
            # or if 0 is in S (making S^{-1}R the zero ring, which under some strict definitions is not reduced).
            neg_q = (not is_mult_closed) or (0 in S)
            
            return [bool(h1), bool(h2), bool(neg_q)]
            
        # Case 2: Fallback for Sympy objects or custom ring representations
        h1 = getattr(R_obj, 'is_commutative', False)
        if callable(h1): 
            h1 = h1()
        
        h2 = getattr(R_obj, 'is_reduced', None)
        if h2 is None:
            # Domains are always reduced
            h2 = getattr(R_obj, 'is_domain', False)
        if callable(h2): 
            h2 = h2()
        
        neg_q = False
        if S_obj is not None and hasattr(S_obj, '__iter__'):
            is_mult_closed = True
            S_list = list(S_obj)
            has_one = any(getattr(x, 'is_one', x == 1) for x in S_list)
            has_zero = any(getattr(x, 'is_zero', x == 0) for x in S_list)
            
            if not has_one:
                is_mult_closed = False
            else:
                for a in S_list:
                    for b in S_list:
                        if (a * b) not in S_list:
                            is_mult_closed = False
                            break
                    if not is_mult_closed:
                        break
            neg_q = (not is_mult_closed) or has_zero
        else:
            # If S is not provided, assume S is the set of non-zero elements.
            # It is multiplicatively closed iff R is an integral domain.
            is_domain = getattr(R_obj, 'is_domain', True)
            if callable(is_domain): 
                is_domain = is_domain()
            neg_q = not is_domain
            
        return [bool(h1), bool(h2), bool(neg_q)]
        
    except Exception:
        return [False, False, False]