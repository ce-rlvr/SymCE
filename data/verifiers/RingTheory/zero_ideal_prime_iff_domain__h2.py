import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import sympy.abc

# Top-level setup for standard algebra objects
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

def check_ring(witness):
    if isinstance(witness, type):
        try:
            witness = witness()
        except Exception:
            pass

    # 1. String representations of common rings
    if isinstance(witness, str):
        w = witness.replace(" ", "").lower()
        # Commutative rings without identity and without zero divisors
        if w in ["2z", "3z", "4z", "5z", "6z", "2*z", "3*z", "4*z", "2*zz", "3*zz", "2z[x]", "3z[x]", "evenintegers"]:
            return True, False, True
        # Integral domains
        if w in ["z", "q", "r", "c", "z[x]", "zz", "qq", "rr", "cc"]:
            return True, True, True
        # Zero ring
        if w in ["{0}", "0"]:
            return True, False, False

    # 2. SymPy expressions that might represent ideals like 2*Z
    if isinstance(witness, sympy.Expr) or (hasattr(witness, '__class__') and witness.__class__.__name__ in ['Mul', 'Symbol']):
        w = str(witness).replace(" ", "").lower()
        if w in ["2*z", "3*z", "4*z", "2*zz", "3*zz"]:
            return True, False, True

    # 3. Custom object with explicit properties
    if hasattr(witness, 'is_commutative_ring') and hasattr(witness, 'is_integral_domain') and hasattr(witness, 'is_zero_ideal_prime'):
        return bool(witness.is_commutative_ring), bool(witness.is_integral_domain), bool(witness.is_zero_ideal_prime)

    # 4. Finite ring provided via elements, add, mul, zero
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
        elements = list(witness.elements)
        zero = witness.zero
        
        is_comm = True
        for a in elements:
            for b in elements:
                if witness.mul(a, b) != witness.mul(b, a):
                    is_comm = False
                    break
            if not is_comm:
                break
                
        has_zero_div = False
        for a in elements:
            if a == zero: continue
            for b in elements:
                if b == zero: continue
                if witness.mul(a, b) == zero:
                    has_zero_div = True
                    break
            if has_zero_div: break
            
        has_id = False
        for e in elements:
            if e == zero: continue
            is_id = True
            for a in elements:
                if witness.mul(a, e) != a or witness.mul(e, a) != a:
                    is_id = False
                    break
            if is_id:
                has_id = True
                break
                
        is_zero_ring = (len(elements) <= 1)
        
        # An integral domain is a commutative ring with identity (1 != 0) and no zero divisors.
        is_idom = is_comm and has_id and not has_zero_div and not is_zero_ring
        
        # The ideal {0} is prime iff the ring is not the zero ring and has no zero divisors.
        is_zip = not has_zero_div and not is_zero_ring
        
        return is_comm, is_idom, is_zip

    raise ValueError("Unknown witness format")

def conditions(witness) -> list[bool]:
    try:
        is_comm, is_idom, is_zip = check_ring(witness)
        h1 = is_comm
        # The conclusion is: R is an integral domain iff {0} is a prime ideal.
        # The negated conclusion is that this equivalence fails.
        neg_q = (is_idom != is_zip)
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "¬Q: R is an integral domain is not equivalent to {0} being a prime ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1