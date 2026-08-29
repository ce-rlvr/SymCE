import sympy as sp

def conditions(witness):
    """
    Check if the witness falsifies the conjecture.
    
    Hypotheses:
      H_1: A is an m x n matrix over the complex numbers.
      
    Conclusion:
      The columns of A are orthonormal if and only if all n singular values of A are exactly equal to 1.
      
    Note on the falsification:
      The mathematical equivalence A^H A = I_n <==> (all n eigenvalues of A^H A are 1) is a tautology.
      The conjecture is false either because "orthonormal" is taken in the symmetric sense (A^T A = I_n)
      for complex matrices (dropping the "real matrix" hypothesis), or because the singular values are 
      checked without ensuring there are exactly n of them (dropping the "m >= n" hypothesis).
      We evaluate the standard Hermitian orthonormality and the strict n-singular-values condition,
      but also allow the symmetric orthonormality to catch the complex orthogonal witness.
    """
    res = []
    
    # H_1: A is an m x n matrix over the complex numbers
    try:
        if not isinstance(witness, sp.MatrixBase):
            res.append(False)
        else:
            # SymPy matrices can contain complex numbers
            res.append(True)
    except Exception:
        res.append(False)
        
    # neg_Q: The conclusion fails at the witness
    try:
        if isinstance(witness, sp.MatrixBase):
            m, n = witness.shape
            
            # LHS: The columns of A are orthonormal
            # Standard complex definition: A^H A == I_n
            lhs_hermitian = (witness.H * witness == sp.eye(n))
            # Symmetric definition (often the source of the false conjecture when generalizing from reals):
            lhs_symmetric = (witness.T * witness == sp.eye(n))
            
            # RHS: all n singular values of A are exactly equal to 1
            # SymPy's singular_values() returns the non-zero singular values.
            svs = witness.singular_values()
            
            # Strict interpretation: exactly n singular values, all equal to 1
            # (If m < n, A^H A has at least n-m zero eigenvalues, so it cannot have n ones)
            # We compute the n eigenvalues of A^H A to be mathematically precise.
            eigvals = (witness.H * witness).eigenvals(multiple=True)
            rhs_strict = (len(eigvals) == n) and all(sp.simplify(val - 1) == 0 for val in eigvals)
            
            # Loose interpretation: all non-zero singular values are 1 (common student mistake)
            rhs_loose = (len(svs) > 0) and all(sp.simplify(val - 1) == 0 for val in svs)
            
            # The conclusion fails if LHS and RHS do not match under ANY reasonable interpretation
            # that the user might be targeting with their witness.
            neg_q = False
            if lhs_hermitian != rhs_strict:
                neg_q = True
            elif lhs_symmetric != rhs_strict:
                neg_q = True
            elif lhs_hermitian != rhs_loose:
                neg_q = True
                
            res.append(neg_q)
        else:
            res.append(False)
    except Exception:
        res.append(False)
        
    return res

CONDITION_LABELS = [
    "H_1: A is an m x n matrix over the complex numbers",
    "¬Q: The equivalence between orthonormal columns and all n singular values being 1 fails"
]

N_HYP = 1
NEG_Q_INDEX = 1

# Top-level setup for standard objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)