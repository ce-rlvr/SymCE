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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (R, I, J) where:
      - R is an integer n (representing the ring Z_n) or a list of elements.
      - I is a list of elements in the ideal I.
      - J is a list of elements in the ideal J.
    """
    try:
        if len(witness) != 3:
            return [False] * 5
        R, I, J = witness
        
        # Determine ring elements and operations
        if isinstance(R, int):
            n = R
            if n < 2: 
                return [False] * 5
            elements = list(range(n))
            zero = 0
            def add(x, y): return (x + y) % n
            def mul(x, y): return (x * y) % n
            h1 = True
        elif isinstance(R, (list, tuple, set)):
            elements = list(R)
            if len(elements) < 2: 
                return [False] * 5
            zero = None
            for e in elements:
                is_zero = True
                for x in elements:
                    if (e + x) != x:
                        is_zero = False
                        break
                if is_zero:
                    zero = e
                    break
            if zero is None: 
                return [False] * 5
            def add(x, y): return x + y
            def mul(x, y): return x * y
            
            h1 = True
            for x in elements:
                for y in elements:
                    if add(x, y) not in elements: h1 = False
                    if mul(x, y) not in elements: h1 = False
                    if mul(x, y) != mul(y, x): h1 = False
        else:
            return [False] * 5
            
        def is_ideal(K):
            if not isinstance(K, (list, set, tuple)): return False
            if not all(k in elements for k in K): return False
            if zero not in K: return False
            for x in K:
                for y in K:
                    if add(x, y) not in K: return False
                for r in elements:
                    if mul(r, x) not in K: return False
            return True
            
        # H_2: J is an ideal of R
        h2 = is_ideal(J)
        
        # H_3: The product ideal IJ is the zero ideal
        h3 = True
        if not isinstance(I, (list, set, tuple)):
            h3 = False
        elif not all(i in elements for i in I):
            h3 = False
        else:
            for i in I:
                for j in J:
                    if mul(i, j) != zero:
                        h3 = False
                        break
                if not h3: break
                
        # H_4: I is not the zero ideal
        h4 = is_ideal(I) and any(i != zero for i in I)
        
        # ¬Q: Not every element of the ideal J is a zero-divisor in R
        # A zero-divisor is a non-zero element x such that xy = 0 for some non-zero y.
        def is_zero_divisor(x):
            if x == zero: 
                return False
            for y in elements:
                if y != zero and mul(x, y) == zero:
                    return True
            return False
            
        every_j_is_zd = True
        if not isinstance(J, (list, set, tuple)):
            every_j_is_zd = False
        else:
            for j in J:
                if not is_zero_divisor(j):
                    every_j_is_zd = False
                    break
                
        neg_q = not every_j_is_zd
        
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False] * 5

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "H_3: The product ideal IJ is the zero ideal",
    "H_4: I is not the zero ideal",
    "¬Q: Not every element of the ideal J is a zero-divisor in R"
]

N_HYP = 4
NEG_Q_INDEX = 4