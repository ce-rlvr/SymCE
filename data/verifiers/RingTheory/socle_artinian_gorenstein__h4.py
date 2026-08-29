import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

# Expected witness format:
# A list of sympy.Matrix objects of the same square shape, representing a basis
# for a finite-dimensional commutative algebra over Q.

def conditions(witness):
    """
    Checks if the witness satisfies the hypotheses and falsifies the conclusion.
    Returns a list of booleans: [H_1, H_2, H_3, neg_Q].
    """
    res = [False, False, False, False]
    
    try:
        if not isinstance(witness, list) or len(witness) == 0:
            return res
        n = len(witness)
        if not all(isinstance(M, sp.Matrix) for M in witness):
            return res
        if not all(M.is_square for M in witness):
            return res
        d = witness[0].shape[0]
        if d == 0:
            return res
        if not all(M.shape == (d, d) for M in witness):
            return res
            
        # Check linear independence of the basis
        vecs = [M.vec() for M in witness]
        basis_mat = sp.Matrix.hstack(*vecs)
        if basis_mat.rank() != n:
            return res
            
        # Check commutativity
        is_comm = True
        for i in range(n):
            for j in range(i + 1, n):
                if witness[i] * witness[j] != witness[j] * witness[i]:
                    is_comm = False
                    break
            if not is_comm:
                break
        if not is_comm:
            return res
            
        # Check if the span contains the identity matrix
        I_vec = sp.eye(d).vec()
        if basis_mat.row_join(I_vec).rank() != n:
            return res
            
        # Check closure under multiplication
        is_closed = True
        for i in range(n):
            for j in range(i, n):
                prod_vec = (witness[i] * witness[j]).vec()
                if basis_mat.row_join(prod_vec).rank() != n:
                    is_closed = False
                    break
            if not is_closed:
                break
        if not is_closed:
            return res
            
        res[0] = True
    except Exception:
        return res

    try:
        # Compute the trace form matrix T
        T = sp.zeros(n, n)
        for i in range(n):
            for j in range(n):
                T[i, j] = sp.trace(witness[i] * witness[j])
        
        # For a finite-dimensional commutative algebra over Q,
        # it is a local ring with residue field Q iff the trace form has rank 1.
        # We restrict to residue field Q as it is sufficient for the standard counterexample.
        if T.rank() == 1:
            res[1] = True
    except Exception:
        pass

    try:
        # Any finite-dimensional algebra over a field is Artinian.
        if res[0]:
            res[2] = True
    except Exception:
        pass

    try:
        if res[0] and res[1]:
            # Compute the Jacobson radical J (maximal ideal)
            J_coeffs = T.nullspace()
            N_list = []
            for vec in J_coeffs:
                N = sp.zeros(d, d)
                for i in range(n):
                    N += vec[i] * witness[i]
                N_list.append(N)
                
            # The socle is the annihilator of J.
            # We find all elements x = sum(c_i * witness[i]) such that x * N = 0 for all N in J.
            eq_cols = []
            for i in range(n):
                col_blocks = []
                for N in N_list:
                    col_blocks.append((witness[i] * N).vec())
                if col_blocks:
                    eq_cols.append(sp.Matrix.vstack(*col_blocks))
                    
            if not eq_cols:
                # If J is trivial, the annihilator is the whole ring
                dim_socle = n
            else:
                eq_mat = sp.Matrix.hstack(*eq_cols)
                dim_socle = n - eq_mat.rank()
                
            # Since the residue field is Q, dim_k(Socle) is just dim_socle
            if dim_socle != 1:
                res[3] = True
    except Exception:
        pass

    return res

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m and residue field k = R/m",
    "H_3: R is an Artinian ring",
    "¬Q: The socle of R is not a one-dimensional vector space over k"
]

N_HYP = 3
NEG_Q_INDEX = 3