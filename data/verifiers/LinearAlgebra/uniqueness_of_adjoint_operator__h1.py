import sympy
from sympy import Matrix, eye, zeros
import itertools
import math

# Top-level setup: named object bindings that the witness expression may reference.
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    """
    Given a witness, checks whether it is a valid counterexample to the false conjecture.
    The witness can either be a custom object representing an infinite-dimensional space
    (which must provide specific methods) or a tuple of finite matrices:
    (B, T, T_star1, T_star2)
    """
    try:
        # If the witness is a custom object representing an abstract/infinite-dimensional space
        if hasattr(witness, 'is_non_degenerate'):
            h1 = bool(witness.is_non_degenerate())
            h2 = bool(witness.is_linear_operator())
            neg_q = bool(witness.has_multiple_adjoints())
            return [h1, h2, neg_q]
            
        # Otherwise, assume the witness is a tuple of sympy Matrices
        B, T, T_star1, T_star2 = witness
        
        # Convert to sympy Matrices if they aren't already
        B = Matrix(B)
        T = Matrix(T)
        T_star1 = Matrix(T_star1)
        T_star2 = Matrix(T_star2)
        
        # Hypothesis 1: B is a non-degenerate bilinear form on V
        # For finite matrices over a field, non-degenerate means determinant is non-zero.
        try:
            h1 = (B.det() != 0)
        except Exception:
            h1 = False
            
        # Hypothesis 2: T is a linear operator on V
        # Any valid square matrix represents a linear operator on V = F^n
        h2 = (T.shape[0] == T.shape[1] and T.shape == B.shape)
        
        # Negated Conclusion: There exists MORE THAN ONE linear operator T^* satisfying the adjoint condition.
        # Condition: B(T(u), v) = B(u, T^*(v))  =>  T^T * B = B * T^*
        eq1 = (T.transpose() * B == B * T_star1)
        eq2 = (T.transpose() * B == B * T_star2)
        distinct = (T_star1 != T_star2)
        
        neg_q = bool(eq1 and eq2 and distinct)
        
        return [h1, h2, neg_q]
        
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: B is a non-degenerate bilinear form on V",
    "H_2: T is a linear operator on V",
    "¬Q: There exist multiple distinct linear operators T^* satisfying B(T(u), v) = B(u, T^*(v))"
]

N_HYP = 2
NEG_Q_INDEX = 2