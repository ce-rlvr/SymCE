import sympy
from sympy import S, eye, zeros
from sympy.abc import x, y, z
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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

def extract(witness):
    if hasattr(witness, 'R1') and hasattr(witness, 'R2'):
        R1 = witness.R1
        R2 = witness.R2
        pi_1 = getattr(witness, 'pi_1', lambda a, b: a)
        return R1, R2, pi_1
    elif isinstance(witness, tuple):
        if len(witness) == 3:
            return witness[0], witness[1], witness[2]
        elif len(witness) == 2:
            return witness[0], witness[1], lambda a, b: a
    return None, None, None

def is_ring(R):
    try:
        if hasattr(R, 'is_Ring') and R.is_Ring:
            return True
    except Exception:
        pass
    try:
        if R in [S.Integers, S.Rationals, S.Reals, S.Complexes]:
            return True
    except Exception:
        pass
    try:
        from sympy.polys.domains import Ring
        if isinstance(R, Ring):
            return True
    except Exception:
        pass
    
    try:
        R_list = list(R)
        if len(R_list) == 0:
            return False
        zero = None
        for z_elem in R_list:
            if all(a + z_elem == a and z_elem + a == a for a in R_list):
                zero = z_elem
                break
        if zero is None:
            return False
        for a in R_list:
            has_inv = False
            for b in R_list:
                if a + b == zero and b + a == zero:
                    has_inv = True
                if (a + b) not in R_list:
                    return False
                if (a * b) not in R_list:
                    return False
            if not has_inv:
                return False
        return True
    except Exception:
        return False

def get_zero(R):
    try:
        if R in [S.Integers, S.Rationals, S.Reals, S.Complexes]:
            return S.Zero
    except Exception:
        pass
    try:
        if hasattr(R, 'zero'):
            return R.zero
    except Exception:
        pass
    try:
        R_list = list(R)
        for z_elem in R_list:
            if all(a + z_elem == a and z_elem + a == a for a in R_list):
                return z_elem
    except Exception:
        pass
    return 0

def conditions(witness) -> list[bool]:
    R1, R2, pi_1 = extract(witness)
    if R1 is None or R2 is None:
        return [False, False, False]
    
    # H1: R_1 and R_2 are rings
    try:
        h1 = is_ring(R1) and is_ring(R2)
    except Exception:
        h1 = False
        
    # H2: pi_1 is the canonical projection homomorphism defined by pi_1(x, y) = x
    try:
        z1 = get_zero(R1)
        z2 = get_zero(R2)
        h2 = (pi_1(z1, z2) == z1)
        try:
            for x_elem in R1:
                for y_elem in R2:
                    if pi_1(x_elem, y_elem) != x_elem:
                        h2 = False
        except Exception:
            pass
    except Exception:
        h2 = False
        
    # neg_Q: The kernel of pi_1 is NOT the ideal {(0, y) | y in R_2}
    # (This fails if the zero element of R_1 is not the integer 0)
    try:
        if hasattr(witness, 'kernel_is_0_y'):
            neg_q = not witness.kernel_is_0_y
        else:
            z1 = get_zero(R1)
            try:
                is_zero_int = (z1 == 0)
            except Exception:
                is_zero_int = False
            
            if is_zero_int:
                neg_q = False
            else:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R_1 and R_2 are rings",
    "H_2: pi_1 is the canonical projection homomorphism defined by pi_1(x, y) = x",
    "¬Q: The kernel of pi_1 is not the ideal {(0, y) | y in R_2}"
]

N_HYP = 2
NEG_Q_INDEX = 2