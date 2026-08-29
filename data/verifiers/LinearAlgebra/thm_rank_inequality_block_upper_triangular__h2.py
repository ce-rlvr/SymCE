import sympy as sp

def conditions(witness):
    """
    Verifies that the witness satisfies the remaining hypotheses and falsifies the conclusion.
    
    The conjecture is about the rank of a block upper triangular matrix.
    Remaining hypotheses:
      H1: F is a field.
      H2: C is a p x q matrix over F.
      H3: B is an m x q matrix over F.
      H4: M is the (m+p) x (n+q) block upper triangular matrix composed of A as the top-left block, 
          B as the top-right block, a zero matrix as the bottom-left block, and C as the bottom-right block.
          
    Conclusion to falsify:
      rank(M) >= rank(A) + rank(C)
    """
    try:
        # Extract components from the witness
        F = witness.get('F')
        A = witness.get('A')
        B = witness.get('B')
        C = witness.get('C')
        M = witness.get('M')
        m = witness.get('m')
        n = witness.get('n')
        p = witness.get('p')
        q = witness.get('q')
        
        # H1: F is a field
        try:
            h1 = F.is_Field
        except Exception:
            h1 = False
            
        # H2: C is a p x q matrix over F
        try:
            h2 = isinstance(C, sp.MatrixBase) and C.rows == p and C.cols == q
        except Exception:
            h2 = False
            
        # H3: B is an m x q matrix over F
        try:
            h3 = isinstance(B, sp.MatrixBase) and B.rows == m and B.cols == q
        except Exception:
            h3 = False
            
        # H4: M is the (m+p) x (n+q) block upper triangular matrix
        try:
            h4 = False
            if isinstance(M, sp.MatrixBase) and isinstance(A, sp.MatrixBase):
                if M.rows == m + p and M.cols == n + q:
                    top_left = M[:m, :n]
                    top_right = M[:m, n:]
                    bottom_left = M[m:, :n]
                    bottom_right = M[m:, n:]
                    
                    if top_left == A and top_right == B and bottom_left.is_zero_matrix and bottom_right == C:
                        h4 = True
        except Exception:
            h4 = False
            
        # Negated Conclusion: rank(M) < rank(A) + rank(C)
        # Note: Mathematically, rank(M) >= rank(A) + rank(C) is always true for matrices over a field.
        # If the conjecture is false, it must be due to a dropped hypothesis allowing A to be over a ring 
        # with zero divisors, or some other structural anomaly where the standard rank inequality fails.
        try:
            neg_q = M.rank() < A.rank() + C.rank()
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
        
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: C is a p x q matrix over F",
    "H_3: B is an m x q matrix over F",
    "H_4: M is the (m+p) x (n+q) block upper triangular matrix composed of A, B, 0, and C",
    "¬Q: rank(M) < rank(A) + rank(C)"
]

N_HYP = 4
NEG_Q_INDEX = 4

# Top-level setup for standard objects
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)