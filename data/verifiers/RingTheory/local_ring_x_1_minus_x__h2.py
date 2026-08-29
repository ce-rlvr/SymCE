import math
import sympy
from sympy.ntheory import primefactors

# Top-level setup
x, y, z = sympy.symbols('x y z')

def check_tuple_ring(witness):
    elements, add_table, mul_table = witness
    n = len(elements)
    if n == 0:
        return [False, False, False]
    
    # Find zero
    zero_idx = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)) and all(add_table[j][i] == j for j in range(n)):
            zero_idx = i
            break
    if zero_idx is None:
        return [False, False, False]
        
    # Find one
    one_idx = None
    for i in range(n):
        if all(mul_table[i][j] == j and mul_table[j][i] == j for j in range(n)):
            one_idx = i
            break
    if one_idx is None:
        return [False, False, False]
        
    # Check commutative
    is_comm = True
    for i in range(n):
        for j in range(n):
            if mul_table[i][j] != mul_table[j][i]:
                is_comm = False
                break
    
    h1 = is_comm
    
    # Find units
    units = set()
    for i in range(n):
        for j in range(n):
            if mul_table[i][j] == one_idx and mul_table[j][i] == one_idx:
                units.add(i)
                break
                
    # H2: For all x, x or 1-x is a unit
    h2 = True
    for x in range(n):
        # find -x
        neg_x = None
        for j in range(n):
            if add_table[x][j] == zero_idx and add_table[j][x] == zero_idx:
                neg_x = j
                break
        if neg_x is None:
            h2 = False
            break
        one_minus_x = add_table[one_idx][neg_x]
        if x not in units and one_minus_x not in units:
            h2 = False
            break
            
    # Negated conclusion: NOT a local ring
    # A finite commutative ring is local iff the set of non-units forms an ideal.
    non_units = set(range(n)) - units
    is_local = False
    if n > 1:
        is_ideal = True
        for a in non_units:
            for b in non_units:
                if add_table[a][b] not in non_units:
                    is_ideal = False
                    break
            if not is_ideal:
                break
        is_local = is_ideal
    else:
        # The zero ring (n=1) is not a local ring
        is_local = False
        
    neg_q = not is_local
    
    return [h1, h2, neg_q]

def conditions(witness) -> list[bool]:
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The witness can be an integer `n` representing the ring Z/nZ,
    or a tuple `(elements, add_table, mul_table)` representing a finite ring.
    """
    # Try integer Z/nZ
    try:
        if hasattr(witness, '__index__') or isinstance(witness, (int, sympy.Integer)):
            n = int(witness)
            if n >= 1:
                h1 = True
                h2 = True
                for x in range(n):
                    is_unit_x = (math.gcd(x, n) == 1)
                    is_unit_1_minus_x = (math.gcd((1 - x) % n, n) == 1)
                    if not (is_unit_x or is_unit_1_minus_x):
                        h2 = False
                        break
                is_local = (n > 1) and (len(primefactors(n)) == 1)
                neg_q = not is_local
                return [h1, h2, neg_q]
    except Exception:
        pass
        
    # Try tuple (elements, add_table, mul_table)
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            return check_tuple_ring(witness)
    except Exception:
        pass
        
    return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: For every element x in R, either x or 1-x is a unit in R",
    "¬Q: R is not a local ring"
]

N_HYP = 2
NEG_Q_INDEX = 2