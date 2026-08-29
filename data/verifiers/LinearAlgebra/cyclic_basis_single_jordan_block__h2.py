import sympy

def conditions(witness):
    """
    Checks the hypotheses and the negated conclusion for the conjecture:
    "If V is a finite-dimensional vector space and the Jordan canonical form of T 
    consists of exactly one Jordan block of size dim(V), then there exists a vector v 
    such that {v, Tv, ..., T^{dim(V)-1}v} forms a basis for V."
    """
    try:
        # The witness is expected to be a square matrix T representing the linear operator.
        if not isinstance(witness, sympy.MatrixBase):
            return [False, False, False]
        if not witness.is_square:
            return [False, False, False]
            
        n = witness.shape[0]
        
        # H_1: V is a finite-dimensional vector space over a field F.
        # Any square matrix of size n implicitly acts on the finite-dimensional space F^n.
        H1 = True
        
        if n == 0:
            H2 = False
            neg_Q = False
        else:
            # Compute the Jordan canonical form
            P, J = witness.jordan_form()
            
            # Extract Jordan blocks from the block-diagonal matrix J
            blocks = []
            i = 0
            while i < n:
                lam = J[i, i]
                size = 1
                # A Jordan block has the eigenvalue on the diagonal and 1s on the superdiagonal
                while i + size < n and J[i + size, i + size] == lam and J[i + size - 1, i + size] == 1:
                    size += 1
                blocks.append((lam, size))
                i += size
                
            # H_2: The Jordan canonical form of T consists of exactly one Jordan block of size dim(V)
            H2 = (len(blocks) == 1)
            
            # neg_Q: There does NOT exist a vector v such that {v, Tv, ..., T^{dim(V)-1}v} forms a basis.
            # A matrix has such a cyclic vector if and only if its minimal polynomial equals its 
            # characteristic polynomial. This is equivalent to saying that for every eigenvalue, 
            # there is exactly one Jordan block (i.e., geometric multiplicity is 1).
            block_eigenvalues = [b[0] for b in blocks]
            has_cyclic_vector = (len(block_eigenvalues) == len(set(block_eigenvalues)))
            neg_Q = not has_cyclic_vector
            
        return [H1, H2, neg_Q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: The Jordan canonical form of T consists of exactly one Jordan block of size dim(V)",
    "¬Q: There does not exist a vector v in V such that {v, Tv, ..., T^{dim(V)-1}v} forms a basis for V"
]

N_HYP = 2
NEG_Q_INDEX = 2

# Standard algebra objects for the namespace
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)