import sympy
from sympy import eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

# Standard cardinalities for infinite-dimensional vector space counterexamples
aleph_0 = 'aleph_0'
c = 'c'

def add_cardinals(c1, c2):
    c1, c2 = str(c1), str(c2)
    order = ['0', 'finite', 'aleph_0', 'c', '2^c']
    
    def get_rank(card):
        if card.isdigit():
            return 0 if card == '0' else 1
        if card in order:
            return order.index(card)
        return -1

    r1 = get_rank(c1)
    r2 = get_rank(c2)
    
    if r1 == -1 or r2 == -1:
        return 'unknown'
        
    max_r = max(r1, r2)
    if max_r == 0:
        return str(int(c1) + int(c2))
    if max_r == 1:
        if c1.isdigit() and c2.isdigit():
            return str(int(c1) + int(c2))
        return 'finite'
    
    return order[max_r]

def power_cardinals(base, exp):
    base, exp = str(base), str(exp)
    if exp == '0':
        return '1'
    if base == '1':
        return '1'
    if base == '0':
        return '0'
        
    if base.isdigit() and exp.isdigit():
        if int(exp) > 1000:  # Prevent massive exponentiation
            return 'unknown'
        return str(int(base) ** int(exp))
        
    if exp == 'aleph_0':
        if base.isdigit() and int(base) >= 2:
            return 'c'
        if base in ['aleph_0', 'c']:
            return 'c'
            
    if exp == 'c':
        if base.isdigit() and int(base) >= 2:
            return '2^c'
        if base in ['aleph_0', 'c']:
            return '2^c'
            
    return 'unknown'

def get_dual_dim(dim_space, field_size):
    dim_space = str(dim_space)
    # For finite-dimensional spaces, dim(V^*) = dim(V) regardless of field size
    if dim_space.isdigit():
        return dim_space
    if dim_space == 'finite':
        return 'finite'
    # For infinite-dimensional spaces, dim(V^*) = |F|^dim(V)
    return power_cardinals(field_size, dim_space)

def conditions(witness) -> list[bool]:
    """
    Verifies the counterexample using cardinal arithmetic.
    The witness should provide the dimensions of V, U, V/U, and the base field size.
    """
    try:
        if isinstance(witness, dict):
            dim_V = str(witness.get('dim_V', ''))
            dim_U = str(witness.get('dim_U', ''))
            dim_V_mod_U = str(witness.get('dim_V_mod_U', ''))
            field_size = str(witness.get('field_size', ''))
        else:
            dim_V = str(getattr(witness, 'dim_V', ''))
            dim_U = str(getattr(witness, 'dim_U', ''))
            dim_V_mod_U = str(getattr(witness, 'dim_V_mod_U', ''))
            field_size = str(getattr(witness, 'field_size', ''))
            
        if not dim_V or not dim_U or not dim_V_mod_U or not field_size:
            return [False, False, False]
            
        # H_1: U is a subspace of V
        # This requires that dim(V) == dim(U) + dim(V/U) in cardinal arithmetic
        sum_dims = add_cardinals(dim_U, dim_V_mod_U)
        h1 = (sum_dims != 'unknown') and (dim_V == sum_dims)
        
        # H_2: U^0 is the annihilator of U in the dual space V^*
        # This requires dim(U^0) == dim((V/U)^*)
        dim_U0 = get_dual_dim(dim_V_mod_U, field_size)
        h2 = (dim_U0 != 'unknown')
        
        # ¬Q: dim(U) + dim(U^0) != dim(V)
        lhs = add_cardinals(dim_U, dim_U0)
        neg_q = (lhs != 'unknown') and (lhs != dim_V)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: U is a subspace of V",
    "H_2: U^0 is the annihilator of U in the dual space V^*",
    "¬Q: dim(U) + dim(U^0) != dim(V)"
]

N_HYP = 2
NEG_Q_INDEX = 2