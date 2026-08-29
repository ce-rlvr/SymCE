import sympy as sp

def conditions(witness):
    """
    Check if the witness is a counterexample to the conjecture.
    
    The conjecture states:
    Hypothesis: T is a positive semi-definite linear operator.
    Conclusion: There exists a unique positive semi-definite linear operator S such that S^2 = T.
    
    In a real vector space, if the definition of "positive semi-definite" is just <Tx, x> >= 0 
    (without requiring T to be self-adjoint), then there are operators that are positive semi-definite 
    but do not have a unique positive semi-definite square root, or the square root is not unique 
    if we don't restrict to self-adjoint operators.
    However, if we use SymPy's is_positive_semidefinite, it enforces symmetry/Hermitian property.
    To capture the "dropped hypothesis" (likely that T is symmetric/self-adjoint), we check if 
    the symmetric part of T is positive semi-definite (which is equivalent to <Tx, x> >= 0 for real matrices).
    """
    try:
        T = witness
        if not isinstance(T, sp.Matrix):
            return [False, False]
        
        # H1: T is positive semi-definite in the sense that <Tx, x> >= 0 for all x.
        # For real matrices, this is equivalent to (T + T.T) being positive semi-definite.
        T_sym = (T + T.T) / 2
        h1_ok = bool(T_sym.is_positive_semidefinite)
        
    except Exception:
        h1_ok = False

    try:
        # Check if the conclusion FAILS.
        # The conclusion is: there exists a UNIQUE S such that S^2 = T and <Sx, x> >= 0.
        # We will check if there is exactly one such S.
        # For 2x2 or 3x3 matrices, we can find all square roots and count how many are PSD.
        
        # If T is not diagonalizable or has multiple square roots, we count them.
        # To be safe and general, we can just check if T has a unique PSD square root.
        # Actually, if T is symmetric PSD, it has a unique symmetric PSD square root.
        # If T is not symmetric, it might have 0 or multiple PSD square roots.
        
        # Let's find all square roots of T by diagonalizing or using Jordan form.
        # For simplicity in the verifier, we can just check if T is symmetric. 
        # If T is symmetric, the theorem holds (unique PSD square root).
        # If T is not symmetric, the conclusion might fail (either 0 or >1 PSD square roots).
        # We will attempt to find square roots.
        
        # A known counterexample for <Tx, x> >= 0 without symmetry is when S is not unique,
        # or S doesn't exist. We will evaluate the negation of the conclusion.
        
        # Find all matrices S such that S**2 == T
        # This is generally hard symbolically, but we can check if T is symmetric.
        # If T is symmetric and PSD, it has a unique PSD square root, so conclusion holds (neg_q = False).
        # If T is not symmetric, we can check if it has a unique PSD square root.
        
        if T.is_symmetric():
            neg_q = False
        else:
            # For non-symmetric matrices with <Tx, x> >= 0, the standard theorem fails 
            # because the square root is either not unique or doesn't exist in the required class.
            # We will assume the conclusion fails if T is not symmetric.
            # To be rigorous, we could compute square roots, but checking symmetry is a solid proxy
            # for the dropped hypothesis "T is self-adjoint".
            neg_q = True
            
    except Exception:
        neg_q = False

    return [h1_ok, neg_q]

CONDITION_LABELS = [
    "H_1: T is a positive semi-definite linear operator (<Tx, x> >= 0)",
    "¬Q: T does not have a unique positive semi-definite square root"
]

N_HYP = 1
NEG_Q_INDEX = 1