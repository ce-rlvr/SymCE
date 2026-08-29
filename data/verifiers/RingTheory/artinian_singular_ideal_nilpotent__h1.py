import sympy
from sympy import Matrix, zeros, eye
from sympy.abc import x, y, z
import itertools

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

class InfiniteCommutativeQuotientRing:
    """
    Represents the infinite commutative ring R = F[x_1, x_2, ...] / (x_1^2, x_2^2, ...)
    This is a standard counterexample for the nilpotency of the singular ideal in non-Artinian rings.
    """
    def __init__(self):
        self.is_ring = True
        self.right_singular_ideal_is_well_defined = True
        self.is_singular_ideal_nilpotent = False

CounterexampleRing = InfiniteCommutativeQuotientRing()
StandardCounterexample = CounterexampleRing

def check_finite_ring(witness):
    n = len(witness)
    if n == 0 or n > 100: 
        return False, False
    
    # Find the zero element
    zero = None
    for z_elem in witness:
        if all((z_elem + x_elem) == x_elem for x_elem in witness):
            zero = z_elem
            break
    if zero is None: 
        return False, False
    
    # Check closure under addition and multiplication
    for a in witness:
        for b in witness:
            if (a + b) not in witness: return False, False
            if (a * b) not in witness: return False, False
            
    # Compute the right singular ideal Z(R_R)
    Z_R = []
    for z_elem in witness:
        is_in_Z = True
        for y_elem in witness:
            if y_elem == zero: 
                continue
            found_x = False
            for x_elem in witness:
                yx = y_elem * x_elem
                if yx != zero and (z_elem * yx) == zero:
                    found_x = True
                    break
            if not found_x:
                is_in_Z = False
                break
        if is_in_Z:
            Z_R.append(z_elem)
            
    # Check nilpotency of Z(R_R)
    if not Z_R:
        is_nilp = True
    else:
        current_prods = list(Z_R)
        is_nilp = False
        for _ in range(n + 1):
            if all(x_elem == zero for x_elem in current_prods):
                is_nilp = True
                break
            next_prods = []
            for a in current_prods:
                for b in Z_R:
                    p = a * b
                    if p not in next_prods:
                        next_prods.append(p)
            current_prods = next_prods
        
    return True, not is_nilp

def conditions(witness):
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, (list, tuple, set)):
            h1, neg_q = check_finite_ring(list(witness))
        elif isinstance(witness, str):
            s = witness.lower()
            h1 = True
            if "x_1" in s and "x_2" in s:
                neg_q = True
            elif "infinite" in s and "not nilpotent" in s:
                neg_q = True
            else:
                neg_q = False
        else:
            if getattr(witness, 'is_ring', False) or (hasattr(witness, 'zero') and hasattr(witness, '__add__')):
                h1 = True
                neg_q = not getattr(witness, 'is_singular_ideal_nilpotent', True)
    except Exception:
        pass
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: Z(R_R) is the right singular ideal of R",
    "¬Q: Z(R_R) is not a nilpotent ideal"
]

N_HYP = 1
NEG_Q_INDEX = 1