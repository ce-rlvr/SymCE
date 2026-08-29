import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Check if the witness is a valid counterexample to the conjecture.
    The witness should be a square matrix over QQ representing the operator T.
    """
    # H_1: V is a finite-dimensional vector space over a field F
    # We require the witness to be a square matrix over QQ.
    try:
        if not (hasattr(witness, 'is_square') and witness.is_square):
            h1 = False
        else:
            h1 = all(isinstance(sympy.sympify(e), sympy.Rational) for e in witness)
    except Exception:
        h1 = False

    # ¬Q: The conclusion fails at the witness.
    # Conclusion: T is diagonalizable iff every T-invariant subspace has a T-invariant complement.
    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            cp = witness.charpoly(x).as_expr()
            
            # Factor the characteristic polynomial over QQ
            content, factors = sympy.factor_list(cp, x, domain='QQ')
            
            rad_expr = sympy.Integer(1)
            all_linear = True
            for p, exp in factors:
                rad_expr *= p
                if sympy.Poly(p, x).degree() > 1:
                    all_linear = False
                    
            # Evaluate the radical polynomial at the matrix
            coeffs = sympy.Poly(rad_expr, x).all_coeffs()
            n = witness.shape[0]
            rad_M = sympy.zeros(n, n)
            for i, c in enumerate(coeffs):
                rad_M += c * (witness ** (len(coeffs) - 1 - i))
                
            # Q_holds: every T-invariant subspace has a T-invariant complement.
            # This is true iff the minimal polynomial is square-free,
            # which is equivalent to the radical of the charpoly annihilating the matrix.
            Q_holds = rad_M.is_zero_matrix
            
            # P_holds: T is diagonalizable over QQ.
            # This is true iff the minimal polynomial is square-free AND splits into linear factors.
            P_holds = Q_holds and all_linear
            
            # The conclusion is P <-> Q. We want the negation (P != Q).
            neg_q = bool(P_holds != Q_holds)
            
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "¬Q: T is diagonalizable iff every T-invariant subspace has a T-invariant complement fails"
]

N_HYP = 1
NEG_Q_INDEX = 1