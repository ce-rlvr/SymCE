import sympy
import itertools

# Top-level setup: named object bindings that the witness expression may reference.
# We define integers to represent Z_n rings for convenience.
Z1 = 1
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def apply_op(op, a, b):
    if callable(op):
        return op(a, b)
    elif isinstance(op, dict):
        return op[(a, b)]
    elif isinstance(op, list):
        return op[a][b]
    else:
        raise ValueError("Unknown operator")

def check_ring_properties(R):
    """
    Returns a tuple (satisfies_x2_eq_x, has_identity, has_1_neq_0)
    """
    if isinstance(R, int):
        if R <= 0:
            return (False, False, False)
        if R == 1:
            return (True, True, False)  # Zero ring: x^2=x, has id (0), 1 == 0
        if R == 2:
            return (True, True, True)   # Z_2: x^2=x, has id, 1 != 0
        return (False, True, True)      # Z_n (n>2): x^2=x fails, has id, 1 != 0
        
    if isinstance(R, tuple) and len(R) == 3:
        elements, add, mul = R
        
        satisfies_x2 = True
        for x in elements:
            if apply_op(mul, x, x) != x:
                satisfies_x2 = False
                break
                
        has_id = False
        id_element = None
        for e in elements:
            is_id = True
            for x in elements:
                if apply_op(mul, e, x) != x or apply_op(mul, x, e) != x:
                    is_id = False
                    break
            if is_id:
                has_id = True
                id_element = e
                break
                
        has_zero = False
        zero_element = None
        for z in elements:
            is_zero = True
            for x in elements:
                if apply_op(add, z, x) != x or apply_op(add, x, z) != x:
                    is_zero = False
                    break
            if is_zero:
                has_zero = True
                zero_element = z
                break
                
        has_1_neq_0 = False
        if has_id and has_zero:
            if id_element != zero_element:
                has_1_neq_0 = True
                
        return (satisfies_x2, has_id, has_1_neq_0)
        
    return (False, False, False)

def check_boolean_ring(R):
    """
    A Boolean ring must satisfy x^2 = x, have an identity, and have 1 != 0.
    """
    props = check_ring_properties(R)
    return props[0] and props[1] and props[2]

def is_direct_product_boolean(family):
    """
    Checks if the direct product of a family of rings is a Boolean ring
    without explicitly constructing the Cartesian product.
    """
    if not family:
        # The empty product of rings is the zero ring, which has 1 == 0.
        return False
        
    all_x2 = True
    all_id = True
    any_1_neq_0 = False
    
    for R in family:
        props = check_ring_properties(R)
        if not props[0]:
            all_x2 = False
        if not props[1]:
            all_id = False
        if props[2]:
            any_1_neq_0 = True
            
    return all_x2 and all_id and any_1_neq_0

def conditions(witness) -> list[bool]:
    try:
        # Interpret the witness as a family of rings
        if isinstance(witness, int):
            if witness < 0:
                return [False, False, False]
            family = [2] * witness
        elif isinstance(witness, dict):
            family = list(witness.values())
        elif isinstance(witness, (list, tuple, set)):
            family = list(witness)
        elif hasattr(witness, '__iter__'):
            family = list(witness)
        else:
            return [False, False, False]
            
        # H_1: Let I be an index set
        h1 = True
        
        # H_2: Let {R_i} be a family of Boolean rings
        h2 = all(check_boolean_ring(R) for R in family)
        
        # ¬Q: The direct product R is NOT a Boolean ring
        is_dp_boolean = is_direct_product_boolean(family)
        neg_q = not is_dp_boolean
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: I is an index set",
    "H_2: {R_i} is a family of Boolean rings",
    "¬Q: The direct product R is not a Boolean ring"
]

N_HYP = 2
NEG_Q_INDEX = 2