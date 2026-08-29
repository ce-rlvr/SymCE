import sympy
from sympy import eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness elements
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_ring_tables(n, add, mul):
    if not isinstance(n, int) or n <= 0: return False
    if not isinstance(add, (list, tuple)) or not isinstance(mul, (list, tuple)): return False
    if len(add) != n or len(mul) != n: return False
    for i in range(n):
        if not isinstance(add[i], (list, tuple)) or not isinstance(mul[i], (list, tuple)): return False
        if len(add[i]) != n or len(mul[i]) != n: return False
        for j in range(n):
            if not isinstance(add[i][j], int) or not (0 <= add[i][j] < n): return False
            if not isinstance(mul[i][j], int) or not (0 <= mul[i][j] < n): return False
            
    # Check add commutativity
    for i in range(n):
        for j in range(n):
            if add[i][j] != add[j][i]: return False

    # Check add associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if add[add[i][j]][k] != add[i][add[j][k]]: return False

    # Check mul associativity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[mul[i][j]][k] != mul[i][mul[j][k]]: return False

    # Check distributivity
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: return False
                if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]: return False

    # Find zero
    zero = -1
    for i in range(n):
        if all(add[i][j] == j for j in range(n)):
            zero = i
            break
    if zero == -1: return False

    # Check add inverse
    for i in range(n):
        if not any(add[i][j] == zero for j in range(n)): return False

    return True

def is_ring_objects(R):
    try:
        if not isinstance(R, (list, tuple)) or not R: return False
        
        # Check closure and commutativity
        for a in R:
            for b in R:
                sum_ab = a + b
                prod_ab = a * b
                
                found_sum = False
                found_prod = False
                for x in R:
                    if sum_ab == x: found_sum = True
                    if prod_ab == x: found_prod = True
                if not found_sum or not found_prod: return False
                
                if a + b != b + a: return False
                
        # Find zero
        zero = None
        for e in R:
            is_z = True
            for x in R:
                if x + e != x or e + x != x:
                    is_z = False
                    break
            if is_z:
                zero = e
                break
        if zero is None: return False
        
        # Check inverse
        for a in R:
            has_inv = False
            for b in R:
                if a + b == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Check associativity and distributivity
        for a in R:
            for b in R:
                for c in R:
                    if (a + b) + c != a + (b + c): return False
                    if (a * b) * c != a * (b * c): return False
                    if a * (b + c) != (a * b) + (a * c): return False
                    if (a + b) * c != (a * c) + (b * c): return False
        return True
    except Exception:
        return False

def is_ring(R):
    if isinstance(R, tuple) and len(R) == 3 and isinstance(R[0], int):
        return is_ring_tables(R[0], R[1], R[2])
    else:
        return is_ring_objects(R)

def get_elements(R):
    if isinstance(R, tuple) and len(R) == 3 and isinstance(R[0], int):
        return list(range(R[0]))
    else:
        return list(R)

def add_R(R, a, b):
    if isinstance(R, tuple) and len(R) == 3 and isinstance(R[0], int):
        return R[1][a][b]
    else:
        return a + b

def mul_R(R, a, b):
    if isinstance(R, tuple) and len(R) == 3 and isinstance(R[0], int):
        return R[2][a][b]
    else:
        return a * b

def is_ideal(R1, R2, I):
    elems1 = get_elements(R1)
    elems2 = get_elements(R2)
    
    if not isinstance(I, (list, tuple)): return False
    for item in I:
        if not isinstance(item, (list, tuple)) or len(item) != 2: return False
        x, y = item
        
        def in_elems(val, elems):
            for e in elems:
                if val == e: return True
            return False
            
        if not in_elems(x, elems1) or not in_elems(y, elems2): return False
        
    if not I: return False
    
    def find_zero(R, elems):
        for e in elems:
            is_z = True
            for x in elems:
                if add_R(R, x, e) != x or add_R(R, e, x) != x:
                    is_z = False
                    break
            if is_z:
                return e
        return None
        
    z1 = find_zero(R1, elems1)
    z2 = find_zero(R2, elems2)
    if z1 is None or z2 is None: return False
    
    def in_I(pair, I_list):
        px, py = pair
        for (ix, iy) in I_list:
            if px == ix and py == iy:
                return True
        return False

    if not in_I((z1, z2), I): return False
    
    # Check closure under addition
    for (x1, y1) in I:
        for (x2, y2) in I:
            sum_x = add_R(R1, x1, x2)
            sum_y = add_R(R2, y1, y2)
            if not in_I((sum_x, sum_y), I): return False
            
    # Check closure under additive inverse
    for (x, y) in I:
        has_inv = False
        for (ix, iy) in I:
            if add_R(R1, x, ix) == z1 and add_R(R2, y, iy) == z2:
                has_inv = True
                break
        if not has_inv: return False

    # Check ideal property (absorption)
    for (x, y) in I:
        for r1 in elems1:
            for r2 in elems2:
                lx = mul_R(R1, r1, x)
                ly = mul_R(R2, r2, y)
                if not in_I((lx, ly), I): return False
                
                rx = mul_R(R1, x, r1)
                ry = mul_R(R2, y, r2)
                if not in_I((rx, ry), I): return False
                
    return True

def check_neg_Q(R1, R2, I):
    unique_I = []
    for pair in I:
        px, py = pair
        found = False
        for ux, uy in unique_I:
            if px == ux and py == uy:
                found = True
                break
        if not found:
            unique_I.append(pair)
            
    I1 = []
    for px, py in unique_I:
        found = False
        for ux in I1:
            if px == ux:
                found = True
                break
        if not found:
            I1.append(px)
            
    I2 = []
    for px, py in unique_I:
        found = False
        for uy in I2:
            if py == uy:
                found = True
                break
        if not found:
            I2.append(py)
            
    return len(unique_I) != len(I1) * len(I2)

def parse_witness(witness):
    if isinstance(witness, dict):
        return witness.get("R1"), witness.get("R2"), witness.get("I")
    elif isinstance(witness, tuple) and len(witness) == 3:
        return witness[0], witness[1], witness[2]
    elif hasattr(witness, "R1") and hasattr(witness, "R2") and hasattr(witness, "I"):
        return witness.R1, witness.R2, witness.I
    return None, None, None

def conditions(witness) -> list[bool]:
    """
    Evaluates the hypotheses and the negated conclusion for the given witness.
    The witness should provide two rings R1, R2 and a subset I of R1 x R2.
    """
    try:
        R1, R2, I = parse_witness(witness)
        if R1 is None or R2 is None or I is None:
            return [False, False, False]
            
        # H1: R1 and R2 are rings
        # Note: The theorem is true for rings with identity. The dropped hypothesis was "with identity".
        # To allow a valid counterexample, we verify they are rings but do not enforce the identity check.
        h1 = is_ring(R1) and is_ring(R2)
        
        # H2: I is a two-sided ideal of R1 x R2
        h2 = False
        if h1:
            h2 = is_ideal(R1, R2, I)
            
        # neg_Q: I is not of the form I1 x I2
        neg_q = False
        if h1 and h2:
            neg_q = check_neg_Q(R1, R2, I)
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R1 and R2 are rings",
    "H_2: I is a two-sided ideal of R1 x R2",
    "¬Q: I is not of the form I1 x I2"
]
N_HYP = 2
NEG_Q_INDEX = 2