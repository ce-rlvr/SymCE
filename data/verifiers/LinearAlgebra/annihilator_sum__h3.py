import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should provide the dimension `n` of the vector space V = R^n,
    a representation of the subspace W_1 (e.g., a list of basis vectors),
    and a representation of the subset W_2 (e.g., a list of its elements).
    """
    try:
        # Extract witness data
        if isinstance(witness, dict):
            n = int(witness.get('n', 0))
            W1_data = witness.get('W1', [])
            W2_data = witness.get('W2', [])
        elif isinstance(witness, (list, tuple)):
            n = int(witness[0])
            W1_data = witness[1]
            W2_data = witness[2]
        else:
            n = int(witness.n)
            W1_data = witness.W1
            W2_data = witness.W2
            
        if n <= 0:
            return [False, False, False]
            
        # Helper to safely convert input data to a SymPy Matrix
        def to_matrix(data, dim):
            if isinstance(data, Matrix):
                if data.rows == 0:
                    return Matrix(0, dim, [])
                return data
            if hasattr(data, '__len__') and len(data) == 0:
                return Matrix(0, dim, [])
            return Matrix(data)
            
        W1 = to_matrix(W1_data, n)
        W2 = to_matrix(W2_data, n)
        
        # Ensure the vectors belong to R^n
        if (W1.rows > 0 and W1.cols != n) or (W2.rows > 0 and W2.cols != n):
            return [False, False, False]
            
        # H_1: V is a vector space over a field F
        # Satisfied by our ambient space R^n
        H1 = True
        
        # H_2: W_1 is a subspace of V
        # Any matrix W1 defines a valid subspace via its row space
        H2 = True
        
        # Conclusion: (W_1 + W_2)^0 = W_1^0 \cap W_2^0
        # We compute the dimensions of both sides to check for equality.
        
        # W_1^0 \cap W_2^0 is the null space of the block matrix [W1; W2]
        M_int = Matrix([W1, W2])
        dim_int = n - M_int.rank()
        
        # (W_1 + W_2)^0 is the annihilator of the Minkowski sum.
        # If W_2 is empty, W_1 + W_2 is empty, and its annihilator is the whole dual space V^*.
        # If W_2 is non-empty, span(W_1 + W_2) = span(W_1 \cup W_2), so their annihilators match.
        if W2.rows == 0:
            dim_sum_ann = n
        else:
            dim_sum_ann = n - M_int.rank()
            
        # The conclusion fails if the dimensions of the two annihilator spaces are different
        neg_Q = (dim_int != dim_sum_ann)
        
        return [H1, H2, neg_Q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: W_1 is a subspace of V",
    "¬Q: (W_1 + W_2)^0 != W_1^0 \\cap W_2^0"
]

N_HYP = 2
NEG_Q_INDEX = 2