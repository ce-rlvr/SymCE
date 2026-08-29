import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: B is the set of all idempotent elements of R",
    "H_3: Multiplication on B is the standard multiplication inherited from R",
    "¬Q: B does not form a Boolean ring under the operations (+) and standard multiplication"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    try:
        # Handle integer witness representing the ring Z/nZ
        if isinstance(witness, (int, float)) or type(witness).__name__ == 'Integer':
            n = int(witness)
            if n < 2:
                return [False, False, False, False]
            elements = list(range(n))
            add = lambda x, y: (x + y) % n
            mul = lambda x, y: (x * y) % n
            zero = 0
            one = 1
        # Handle tuple witness: (elements, add_func, mul_func, zero, one)
        elif isinstance(witness, tuple) and len(witness) == 5:
            elements, add, mul, zero, one = witness
            elements = list(elements)
        else:
            return [False, False, False, False]
            
        h1 = True
        if zero not in elements or one not in elements:
            h1 = False
            
        if h1:
            # Check ring axioms (commutativity and identity)
            for x in elements:
                if mul(x, one) != x or mul(one, x) != x:
                    h1 = False
                    break
                if add(x, zero) != x or add(zero, x) != x:
                    h1 = False
                    break
                
                # Check additive inverse exists
                has_inv = False
                for y in elements:
                    if add(x, y) == zero and add(y, x) == zero:
                        has_inv = True
                        break
                if not has_inv:
                    h1 = False
                    break
                    
                # Check commutativity
                for y in elements:
                    if mul(x, y) != mul(y, x):
                        h1 = False
                        break
                    if add(x, y) != add(y, x):
                        h1 = False
                        break
                if not h1:
                    break
                        
        # H2 and H3 are definitional in our context
        h2 = True
        h3 = True
        
        if not h1:
            return [False, False, False, False]
            
        # B is the set of all idempotent elements of R
        B = [x for x in elements if mul(x, x) == x]
        
        # Check if B forms a Boolean ring under (+) and (*)
        # It must be closed under addition, multiplication, and additive inverses.
        is_ring = True
        for x in B:
            # Find inverse of x in R
            inv_x = None
            for y in elements:
                if add(x, y) == zero:
                    inv_x = y
                    break
            
            # The inverse must be in B
            if inv_x not in B:
                is_ring = False
                
            # Check closure
            for y in B:
                if add(x, y) not in B:
                    is_ring = False
                if mul(x, y) not in B:
                    is_ring = False
                    
        neg_q = not is_ring
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]