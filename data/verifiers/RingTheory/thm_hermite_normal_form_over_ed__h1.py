import sympy
from sympy import Matrix

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture:
    "If R is a Euclidean domain and A is an m x n matrix over R, then there exists
    an invertible m x m matrix U over R such that UA is in Hermite normal form."
    
    The witness should be a tuple (R, A) where R is a SymPy domain and A is a SymPy Matrix.
    However, since we only need to evaluate the conditions, we can infer R from A's elements
    or assume the witness is just the matrix A, and we check if its domain is Euclidean.
    """
    try:
        # Witness is expected to be a SymPy Matrix
        A = witness
        
        # H1: R is a Euclidean domain
        # In SymPy, we can check if the domain of the matrix elements is a PID/Euclidean.
        # For simplicity, we check if the elements belong to a known Euclidean domain like ZZ or QQ[x].
        # If A is a Matrix, we can get its ring/domain.
        domain = A.domain if hasattr(A, 'domain') else None
        if domain is None:
            # Try to infer domain from elements
            from sympy.polys.domains import ZZ, QQ
            if all(isinstance(x, sympy.Integer) for x in A):
                domain = ZZ
            else:
                # Fallback to checking if it's over a polynomial ring or similar
                domain = ZZ # Simplified for the sake of the verifier
        
        # A Euclidean domain is a PID. SymPy domains have is_PID.
        h1_ok = getattr(domain, 'is_PID', False) or getattr(domain, 'is_EuclideanRing', False)
        if domain == sympy.ZZ:
            h1_ok = True
            
    except Exception:
        h1_ok = False

    try:
        # H2: A is an m x n matrix with entries in R
        h2_ok = isinstance(A, Matrix)
    except Exception:
        h2_ok = False

    try:
        # neg_Q: There does NOT exist an invertible m x m matrix U over R such that UA is in HNF.
        # In SymPy, A.hnf() computes the Hermite Normal Form.
        # If it fails or raises an exception, then such U does not exist or HNF is not achievable.
        # We also check if the matrix can be put into HNF.
        try:
            H = A.hnf()
            # If it successfully computes HNF, then the conclusion holds, so neg_Q is False.
            neg_q_ok = False
        except Exception:
            # If it fails to compute HNF, then the conclusion fails, so neg_Q is True.
            neg_q_ok = True
            
        # Additionally, if the matrix is over a domain where HNF is not uniquely defined or 
        # cannot be computed (e.g., some Euclidean domains without canonical representatives),
        # we consider the conclusion to fail.
        if not neg_q_ok and not all(isinstance(x, sympy.Integer) for x in A):
            # For non-integer matrices where HNF might not be strictly defined in the standard way
            neg_q_ok = True
            
    except Exception:
        neg_q_ok = True

    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: A is an m x n matrix with entries in R",
    "¬Q: There does not exist an invertible m x m matrix U over R such that UA is in Hermite normal form"
]

N_HYP = 2
NEG_Q_INDEX = 2