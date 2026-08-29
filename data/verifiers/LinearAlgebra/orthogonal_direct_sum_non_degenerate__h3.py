import sympy
from sympy import Matrix, eye, zeros
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

N_HYP = 3
NEG_Q_INDEX = 3

CONDITION_LABELS = [
    "H_1: V is a vector space",
    "H_2: B is a symmetric bilinear form on V",
    "H_3: The restriction of B to W x W is non-degenerate",
    "¬Q: V is not the internal direct sum of W and its orthogonal complement W^\\perp"
]

def conditions(witness):
    expected_attrs = [
        'is_vector_space', 'is_symmetric_bilinear', 'is_non_degenerate', 'is_direct_sum',
        'V_is_vector_space', 'B_is_symmetric', 'B_W_non_degenerate', 'V_is_direct_sum'
    ]
    
    # Unwrap if witness is a tuple containing the actual witness object
    if isinstance(witness, tuple) and len(witness) > 0:
        first = witness[0]
        if isinstance(first, dict) or any(hasattr(first, attr) for attr in expected_attrs):
            witness = first

    # 1. Dictionary representation
    if isinstance(witness, dict):
        try:
            h1 = bool(witness.get('is_vector_space', witness.get('V_is_vector_space', False)))
            h2 = bool(witness.get('is_symmetric_bilinear', witness.get('B_is_symmetric', False)))
            h3 = bool(witness.get('is_non_degenerate', witness.get('B_W_non_degenerate', False)))
            neg_q = not bool(witness.get('is_direct_sum', witness.get('V_is_direct_sum', True)))
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 2. Custom object representation
    if any(hasattr(witness, attr) for attr in expected_attrs):
        try:
            def get_bool(obj, names, default):
                for name in names:
                    if hasattr(obj, name):
                        val = getattr(obj, name)
                        return bool(val() if callable(val) else val)
                return default

            h1 = get_bool(witness, ['is_vector_space', 'V_is_vector_space'], False)
            h2 = get_bool(witness, ['is_symmetric_bilinear', 'B_is_symmetric'], False)
            h3 = get_bool(witness, ['is_non_degenerate', 'B_W_non_degenerate'], False)
            neg_q = not get_bool(witness, ['is_direct_sum', 'V_is_direct_sum'], True)
            return [h1, h2, h3, neg_q]
        except Exception:
            pass

    # 3. Finite-dimensional matrix representation
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                B, W = witness
            elif len(witness) == 3:
                V, B, W = witness
            else:
                return [False, False, False, False]
            
            if isinstance(B, sympy.Matrix):
                h1 = True  # R^n is a vector space
                h2 = B.is_square and B.is_symmetric()
                
                if isinstance(W, list):
                    if len(W) == 0:
                        h3 = True
                    else:
                        M = sympy.Matrix([[ (w1.T * B * w2)[0] for w2 in W] for w1 in W])
                        h3 = M.det() != 0
                elif isinstance(W, sympy.Matrix):
                    M = W.T * B * W
                    h3 = M.det() != 0
                else:
                    h3 = False
                
                # For finite-dimensional spaces, if W is a subspace and B|_W is non-degenerate,
                # V is ALWAYS the internal direct sum of W and W^\perp.
                # Thus, a finite-dimensional witness cannot be a valid counterexample to this conjecture.
                neg_q = False
                return [h1, h2, h3, neg_q]
    except Exception:
        pass

    return [False, False, False, False]