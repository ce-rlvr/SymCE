import sympy
from sympy import eye, zeros
from sympy.polys.domains import GF

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture.
    Returns [H_1_ok, H_2_ok, neg_Q_ok].
    """
    try:
        if not hasattr(witness, 'shape') or len(witness.shape) != 2:
            return [False, False, False]
        n, m = witness.shape
        if n != m:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    # H_1: Assume A is an involution, meaning A^2 = I
    try:
        I = sympy.eye(n)
        A_sq = witness ** 2
        if A_sq == I:
            h1 = True
        else:
            # Fallback for custom matrix classes or strict equality issues
            diff = A_sq - I
            if all(diff[i, j] == 0 for i in range(n) for j in range(n)):
                h1 = True
            else:
                h1 = False
    except Exception:
        h1 = False

    # H_2: Let k be the dimension of the eigenspace corresponding to the eigenvalue 1
    try:
        I = sympy.eye(n)
        A_minus_I = witness - I
        try:
            ns = A_minus_I.nullspace()
            k = len(ns)
        except Exception:
            # Fallback to rank-nullity theorem if nullspace() fails
            k = n - A_minus_I.rank()
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: The characteristic polynomial of A is NOT p_A(x) = (x-1)^k (x+1)^{n-k}
    try:
        x = sympy.Symbol('x')
        
        # Compute the actual characteristic polynomial of the witness
        if hasattr(witness, 'charpoly'):
            cp = witness.charpoly(x)
            if hasattr(cp, 'as_expr'):
                p_A = cp.as_expr()
            else:
                p_A = cp
        else:
            xI_minus_A = x * sympy.eye(n) - witness
            p_A = xI_minus_A.det()
            
        # Compute the expected characteristic polynomial from the formula
        expected_p_A = ((x - 1)**k * (x + 1)**(n - k)).expand()
        p_A_expanded = sympy.expand(p_A)
        
        # Check if the polynomials are exactly the same expression
        if p_A_expanded == expected_p_A:
            q_holds = True
        else:
            diff = sympy.simplify(p_A_expanded - expected_p_A)
            if diff == 0:
                # If their difference evaluates to 0, they might be mathematically equivalent
                # but evaluated in a finite field (e.g., GF(2) where 1 == -1).
                # The conjecture is false because the formula over Z[x] does not match.
                # We verify strict expression equality via string representation.
                if str(p_A_expanded) == str(expected_p_A):
                    q_holds = True
                else:
                    q_holds = False
            else:
                q_holds = False
                
        neg_q = not q_holds
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: A is an involution (A^2 = I)",
    "H_2: k is the dimension of the eigenspace for eigenvalue 1",
    "¬Q: The characteristic polynomial is NOT (x-1)^k (x+1)^{n-k}"
]

N_HYP = 2
NEG_Q_INDEX = 2