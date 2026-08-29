import sympy
from sympy import MatrixBase, simplify, expand, eye, zeros
from sympy.abc import x, y, z

# Standard linear algebra objects for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Check if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (A, p) where A is a square sympy Matrix 
    and p is a callable representing the function applied to the matrix.
    """
    try:
        A, p = witness
        h1 = isinstance(A, MatrixBase) and A.is_square
    except Exception:
        return [False, False]
        
    if not h1:
        return [False, False]
        
    try:
        # Compute eigenvalues of A with algebraic multiplicities
        eig_dict = A.eigenvals()
        eig_A = []
        for val, mult in eig_dict.items():
            eig_A.extend([val] * mult)
            
        # Compute p(lambda_i) for each eigenvalue
        p_eigs = []
        for val in eig_A:
            pval = p(val)
            # If p(val) returns a 1x1 matrix, extract the scalar
            if isinstance(pval, MatrixBase):
                if pval.shape == (1, 1):
                    pval = pval[0, 0]
                else:
                    return [h1, False]
            p_eigs.append(pval)
            
        # Compute p(A)
        pA = p(A)
        if not isinstance(pA, MatrixBase):
            return [h1, False]
            
        # Compute eigenvalues of p(A) with algebraic multiplicities
        eig_pA_dict = pA.eigenvals()
        eig_pA = []
        for val, mult in eig_pA_dict.items():
            eig_pA.extend([val] * mult)
            
        # Helper to compare two multisets of sympy expressions
        def compare_multisets(list1, list2):
            if len(list1) != len(list2):
                return False
            l2 = list(list2)
            for e1 in list1:
                found = False
                for i, e2 in enumerate(l2):
                    try:
                        diff = e1 - e2
                        if diff == 0 or simplify(diff) == 0 or expand(diff) == 0:
                            l2.pop(i)
                            found = True
                            break
                    except Exception:
                        pass
                if not found:
                    return False
            return True
            
        # The conclusion holds if the multisets of eigenvalues match
        q = compare_multisets(p_eigs, eig_pA)
        neg_q = not q
        
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is an n x n complex matrix",
    "¬Q: The eigenvalues of p(A) are not precisely p(lambda_1), ..., p(lambda_n)"
]

N_HYP = 1
NEG_Q_INDEX = 1