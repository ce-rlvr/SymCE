import sympy
import math

# Top-level setup for potential witness expressions
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def parse_module(obj):
    """
    Parses a module representation into a list of invariant factors (integers).
    The module is assumed to be a finitely generated Z-module.
    - An integer `n` represents Z/nZ.
    - A list of integers represents the direct sum of Z/n_i Z.
    - A matrix represents the presentation matrix A, where M = Z^r / Im(A).
    """
    if isinstance(obj, (int, sympy.Integer)):
        return [int(obj)]
    if isinstance(obj, (list, tuple)):
        if len(obj) > 0 and isinstance(obj[0], (list, tuple)):
            obj = sympy.Matrix(obj)
        else:
            return [int(x) for x in obj]
    if hasattr(obj, 'smith_normal_form'):
        S = obj.smith_normal_form()
        invs = [S[i, i] for i in range(min(S.rows, S.cols))]
        if S.rows > S.cols:
            invs.extend([0] * (S.rows - S.cols))
        return [int(x) for x in invs]
    raise ValueError("Unknown module representation")

def is_zero_module(invs):
    """
    A Z-module is zero iff all its invariant factors are units (1 or -1).
    (Note: invariant factor 0 represents a free component Z, which is non-zero).
    """
    return all(abs(x) == 1 for x in invs)

def tensor_is_zero(inv_M, inv_N):
    """
    The tensor product of Z/aZ and Z/bZ is Z/gcd(a,b)Z.
    The tensor product of two modules is zero iff all pairwise tensor products
    of their cyclic components are zero.
    """
    for a in inv_M:
        for b in inv_N:
            if math.gcd(a, b) != 1:
                return False
    return True

def conditions(witness):
    try:
        # Witness can be (M, N) or (R, M, N)
        if isinstance(witness, (tuple, list)) and len(witness) == 3:
            _, M_obj, N_obj = witness
        elif isinstance(witness, (tuple, list)) and len(witness) == 2:
            M_obj, N_obj = witness
        else:
            return [False, False, False, False]
            
        inv_M = parse_module(M_obj)
        inv_N = parse_module(N_obj)
    except Exception:
        return [False, False, False, False]
        
    # H1: M and N are finitely generated R-modules
    # By definition of our parsing (finite list of invariant factors), they are finitely generated.
    h1 = True
    
    # H2: M is not the zero module
    try:
        h2 = not is_zero_module(inv_M)
    except Exception:
        h2 = False
        
    # H3: N is not the zero module
    try:
        h3 = not is_zero_module(inv_N)
    except Exception:
        h3 = False
        
    # neg_Q: The tensor product M \otimes_R N is the zero module
    try:
        neg_q = tensor_is_zero(inv_M, inv_N)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: M and N are finitely generated R-modules",
    "H_2: M is not the zero module",
    "H_3: N is not the zero module",
    "¬Q: The tensor product M \\otimes_R N is the zero module"
]

N_HYP = 3
NEG_Q_INDEX = 3