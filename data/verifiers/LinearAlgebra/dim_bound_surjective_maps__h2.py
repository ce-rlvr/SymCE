import sympy
from sympy.ntheory import factorint
from sympy import oo

# Top-level setup for standard objects
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The dropped hypothesis is "T is a linear map". 
    Without it, T is just a surjective function. A surjective function from F^dim_V 
    to F^dim_W with dim(V) < dim(W) can only exist if F is an infinite field.
    
    Expected witness format: a tuple (dim_V, dim_W, field_size)
    or a dictionary/object with these attributes.
    """
    try:
        if isinstance(witness, dict):
            dim_V = witness.get('dim_V')
            dim_W = witness.get('dim_W')
            field_size = witness.get('field_size')
        elif hasattr(witness, 'dim_V') and hasattr(witness, 'dim_W') and hasattr(witness, 'field_size'):
            dim_V = witness.dim_V
            dim_W = witness.dim_W
            field_size = witness.field_size
        else:
            dim_V, dim_W, field_size = witness
            
        h1 = False
        try:
            dim_V_int = int(dim_V)
            dim_W_int = int(dim_W)
            if dim_V_int == dim_V and dim_W_int == dim_W:
                if dim_V_int >= 0 and dim_W_int >= 0:
                    h1 = True
                    dim_V, dim_W = dim_V_int, dim_W_int
        except (ValueError, TypeError):
            pass
            
        if h1 and field_size != oo:
            try:
                fs_int = int(field_size)
                if fs_int == field_size and fs_int >= 2:
                    # A finite field must have a prime power size
                    factors = factorint(fs_int)
                    if len(factors) != 1:
                        h1 = False
                    else:
                        field_size = fs_int
                else:
                    h1 = False
            except (ValueError, TypeError):
                h1 = False
                
        # H2: T is surjective
        # We verify if a surjective function T can mathematically exist from F^dim_V to F^dim_W.
        if field_size == oo:
            if dim_W == 0:
                h2 = True
            else:
                h2 = (dim_V > 0)
        elif h1:
            # For finite fields, |V| >= |W| is required for surjectivity
            h2 = (field_size ** dim_V) >= (field_size ** dim_W)
        else:
            h2 = False
            
        # ¬Q: dim(V) < dim(W)
        try:
            neg_q = bool(dim_V < dim_W)
        except Exception:
            neg_q = False
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: Let V and W be finite-dimensional vector spaces over a field F",
    "H_2: T is surjective",
    "¬Q: dim(V) < dim(W)"
]

N_HYP = 2
NEG_Q_INDEX = 2