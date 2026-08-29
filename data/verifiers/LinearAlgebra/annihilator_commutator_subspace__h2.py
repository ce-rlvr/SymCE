import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    The conjecture claims that the set of linear functionals f such that f(xy) = f(yx)
    is equal to the annihilator of [A, A]. For an associative algebra, if [A, A] denotes
    the commutator ideal, this is false (they are only equal if [A, A] is the commutator subspace).
    """
    try:
        if not isinstance(witness, (list, tuple)):
            return [False, False]
        if len(witness) == 0:
            return [False, False]
            
        # Convert elements to SymPy Matrices
        try:
            witness = [Matrix(m) for m in witness]
        except Exception:
            return [False, False]
            
        shape = witness[0].shape
        if shape[0] != shape[1]:
            return [False, False]
        for M in witness:
            if M.shape != shape:
                return [False, False]
                
        def get_basis_and_rank(mats):
            if not mats:
                return [], 0
            # Flatten each matrix into a vector
            flat = [list(m) for m in mats]
            # Transpose so that each matrix corresponds to a column
            M = Matrix(flat).T
            _, pivots = M.rref()
            return [mats[i] for i in pivots], len(pivots)
            
        basis, d = get_basis_and_rank(witness)
        if d == 0:
            return [False, False]
            
        # Check H1: A is an associative algebra over a field F
        # (i.e., the span of the basis matrices is closed under multiplication)
        is_algebra = True
        for i in range(d):
            for j in range(d):
                prod = basis[i] * basis[j]
                _, rank = get_basis_and_rank(basis + [prod])
                if rank > d:
                    is_algebra = False
                    break
            if not is_algebra:
                break
                
        h1 = is_algebra
        if not h1:
            return [False, False]
            
        # Compute the commutator subspace
        commutators = []
        for i in range(d):
            for j in range(i + 1, d):
                commutators.append(basis[i] * basis[j] - basis[j] * basis[i])
                
        ideal_basis, dim_comm_subspace = get_basis_and_rank(commutators)
        
        # Compute the commutator ideal
        # Iteratively multiply by basis elements until the rank stabilizes
        current_rank = dim_comm_subspace
        while True:
            new_elements = []
            for B in basis:
                for C in ideal_basis:
                    new_elements.append(B * C)
                    new_elements.append(C * B)
            
            next_ideal_basis, next_rank = get_basis_and_rank(ideal_basis + new_elements)
            
            if next_rank == current_rank:
                break
            ideal_basis = next_ideal_basis
            current_rank = next_rank
            
        dim_ideal = current_rank
        
        # The conclusion fails if the set of trace functions (annihilator of the commutator subspace)
        # is NOT equal to the annihilator of the commutator ideal [A, A].
        # This happens exactly when the commutator subspace is strictly smaller than the commutator ideal.
        neg_q = (dim_ideal != dim_comm_subspace)
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]

CONDITION_LABELS = ["H_1: A is an associative algebra over a field F", "¬Q: The set of linear functionals f such that f(xy) = f(yx) is NOT equal to the annihilator of the commutator ideal"]
N_HYP = 1
NEG_Q_INDEX = 1