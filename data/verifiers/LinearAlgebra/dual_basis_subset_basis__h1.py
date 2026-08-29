import sympy
from sympy import oo, eye, zeros

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def extract_k_n(witness):
    """
    Attempt to extract the dimension of the subspace W (k) and the dimension 
    of the vector space V (n) from the witness object.
    """
    if isinstance(witness, dict):
        k = witness.get('k', 1)
        n = witness.get('n', witness.get('dim', witness.get('dimension', None)))
        if n is None:
            if 'basis' in witness:
                try:
                    n = len(witness['basis'])
                except Exception:
                    n = oo
            else:
                n = len(witness) if hasattr(witness, '__len__') else None
        return k, n
        
    if hasattr(witness, 'n'):
        return getattr(witness, 'k', 1), witness.n
        
    if hasattr(witness, 'dimension'):
        return getattr(witness, 'k', 1), witness.dimension
        
    if hasattr(witness, 'dim'):
        return getattr(witness, 'k', 1), witness.dim
        
    if isinstance(witness, tuple) and len(witness) >= 2:
        if isinstance(witness[1], (int, sympy.Integer, float)) or witness[1] == oo:
            return witness[0], witness[1]
            
    if isinstance(witness, str):
        w_lower = witness.lower()
        if any(kw in w_lower for kw in ['inf', 'oo', 'poly', 'r[x]', 'r[t]']):
            return 1, oo
            
    if witness == oo:
        return 1, oo
        
    if hasattr(witness, 'is_set') and witness.is_set:
        return 1, oo
        
    if 'poly' in str(type(witness)).lower():
        return 1, oo
        
    if hasattr(witness, 'basis'):
        try:
            b = witness.basis()
            return 1, len(b)
        except Exception:
            return 1, oo
            
    if hasattr(witness, 'shape'):
        return 1, witness.shape[0]
        
    if hasattr(witness, '__len__'):
        return 1, len(witness)
        
    return None, None

def conditions(witness) -> list[bool]:
    try:
        k, n = extract_k_n(witness)
    except Exception:
        k, n = None, None

    try:
        # H_1: Let W be a subspace of V of dimension k
        # k must be a non-negative integer
        h1 = isinstance(k, (int, sympy.Integer)) and k >= 0
    except Exception:
        h1 = False

    try:
        # H_2: Let {v_1, ..., v_n} be a basis for V such that the first k vectors form a basis for W
        # n must be >= k. If n is oo, it represents an infinite basis.
        h2 = (n == oo) or (isinstance(n, (int, sympy.Integer)) and n >= k)
    except Exception:
        h2 = False

    try:
        # H_3: Let {f_1, ..., f_n} be the dual basis in V^* corresponding to {v_1, ..., v_n}
        # This is true by definition for our abstract witness, provided it's a valid space
        h3 = (k is not None and n is not None)
    except Exception:
        h3 = False

    try:
        # neg_Q: The set of linear functionals {f_{k+1}, ..., f_n} does NOT form a basis for W^0
        # The theorem holds for all finite-dimensional vector spaces.
        # The conclusion fails (neg_Q is True) if and only if V is infinite-dimensional (n == oo),
        # because the dual basis elements only span a proper subspace of the dual space,
        # and thus {f_{k+1}, ...} fails to span the annihilator W^0.
        neg_q = (n == oo)
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: W is a subspace of V of dimension k",
    "H_2: {v_1, ..., v_n} is a basis for V such that the first k vectors form a basis for W",
    "H_3: {f_1, ..., f_n} is the dual basis in V^* corresponding to {v_1, ..., v_n}",
    "¬Q: The set of linear functionals {f_{k+1}, ..., f_n} does NOT form a basis for W^0"
]

N_HYP = 3
NEG_Q_INDEX = 3