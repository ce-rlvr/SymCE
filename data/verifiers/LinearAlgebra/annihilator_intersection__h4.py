import sympy
from sympy import Matrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture:
    "If V is a finite-dimensional vector space and W_1 is a subspace, 
    then (W_1 \cap W_2)^0 = W_1^0 + W_2^0."
    (The dropped hypothesis is that W_2 is a subspace).
    
    The witness should provide W_1 (a basis or spanning set for the subspace)
    and W_2 (a finite subset of V).
    """
    try:
        # Parse witness
        if isinstance(witness, dict):
            W1 = witness.get('W1', [])
            W2 = witness.get('W2', [])
        elif isinstance(witness, tuple) and len(witness) == 2:
            W1, W2 = witness
        elif isinstance(witness, tuple) and len(witness) == 3:
            _, W1, W2 = witness
        else:
            W1, W2 = witness

        # Convert sympy Matrices to lists of lists if necessary
        if hasattr(W1, 'tolist') and not isinstance(W1, list):
            W1 = W1.tolist()
        if hasattr(W2, 'tolist') and not isinstance(W2, list):
            W2 = W2.tolist()
            
        def to_list(v):
            if hasattr(v, 'tolist'):
                flat = v.tolist()
                if len(flat) == 1: 
                    return flat[0]
                if all(isinstance(x, list) and len(x) == 1 for x in flat): 
                    return [x[0] for x in flat]
                return flat
            return list(v)
            
        W1 = [to_list(v) for v in W1]
        W2 = [to_list(v) for v in W2]
        
        # Infer dimension of the vector space V
        if W1:
            n = len(W1[0])
        elif W2:
            n = len(W2[0])
        else:
            n = 1
            
        # H1: V is a vector space over a field F (always true for F^n)
        h1 = True
        
        # H2: V is finite-dimensional (always true for F^n)
        h2 = True
        
        # H3: W_1 is a subspace of V
        # We interpret W1 as a set of generators for the subspace W_1.
        # It is valid if all vectors have length n.
        h3 = all(len(v) == n for v in W1)
        if not h3:
            return [h1, h2, False, False]
            
        # Ensure W2 vectors also have length n
        if not all(len(v) == n for v in W2):
            return [h1, h2, h3, False]
            
        # Matrix whose rows span W_1
        W1_mat = Matrix(W1) if W1 else Matrix(0, n, [])
        W1_rank = W1_mat.rank()
        
        # Compute the intersection W_1 \cap W_2
        # Since W_2 is a finite set, we just find which elements of W_2 lie in W_1
        W1_cap_W2 = []
        for v in W2:
            test_mat = Matrix([v]).col_join(W1_mat)
            if test_mat.rank() == W1_rank:
                W1_cap_W2.append(v)
                
        # LHS: (W_1 \cap W_2)^0
        # The annihilator of a set S is the nullspace of the matrix with rows S.
        # Its dimension is n - rank(S).
        M_cap = Matrix(W1_cap_W2) if W1_cap_W2 else Matrix(0, n, [])
        dim_LHS = n - M_cap.rank()
        
        # RHS: W_1^0 + W_2^0
        # The annihilator of W_2 is the annihilator of span(W_2).
        # W_1^0 + W_2^0 = (W_1 \cap span(W_2))^0.
        # Its dimension is n - dim(W_1 \cap span(W_2)).
        W2_mat = Matrix(W2) if W2 else Matrix(0, n, [])
        dim_W1 = W1_mat.rank()
        dim_W2_span = W2_mat.rank()
        
        W1_plus_W2_mat = W1_mat.col_join(W2_mat)
        dim_W1_plus_W2 = W1_plus_W2_mat.rank()
        
        # dim(A \cap B) = dim(A) + dim(B) - dim(A + B)
        dim_span_cap = dim_W1 + dim_W2_span - dim_W1_plus_W2
        dim_RHS = n - dim_span_cap
        
        # The conclusion fails if the dimensions of the annihilators are different
        neg_q = (dim_LHS != dim_RHS)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: V is finite-dimensional",
    "H_3: W_1 is a subspace of V",
    "¬Q: (W_1 \\cap W_2)^0 \\neq W_1^0 + W_2^0"
]

N_HYP = 3
NEG_Q_INDEX = 3