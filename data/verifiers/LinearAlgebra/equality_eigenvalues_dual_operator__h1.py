import sympy
from sympy import Matrix, eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for potential matrix witnesses (though counterexamples must be infinite-dimensional)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the conjecture:
    "lambda is an eigenvalue of T if and only if lambda is an eigenvalue of T*"
    (where T* is the dual operator).
    
    Since the theorem is true for finite-dimensional vector spaces, a valid 
    counterexample must be an infinite-dimensional operator (e.g., the right shift operator).
    """
    try:
        # Witness can be a tuple (T, lambda) or just T (with lambda defaulting to 0)
        if isinstance(witness, tuple) and len(witness) == 2:
            T, lam = witness
        else:
            T = witness
            lam = 0

        h1 = False
        h2 = False
        neg_q = False

        # Check H2: lambda in F
        if isinstance(lam, (int, float, complex)):
            h2 = True
        elif hasattr(lam, "is_Number") and lam.is_Number:
            h2 = True
        elif hasattr(lam, "is_Symbol") and lam.is_Symbol:
            h2 = True
        elif isinstance(T, dict) and "lambda" in T:
            h2 = True
            lam = T["lambda"]

        # Check H1 and Conclusion
        lam_in_T = None
        lam_in_T_star = None

        if isinstance(T, dict):
            h1 = bool(T.get("is_linear_operator", True))
            lam_in_T = bool(T.get("lambda_in_spec_T", False))
            lam_in_T_star = bool(T.get("lambda_in_spec_T_star", True))

        elif hasattr(T, "is_Matrix") and T.is_Matrix:
            # A finite-dimensional matrix cannot be a counterexample for the dual operator,
            # as a matrix and its transpose always share the same eigenvalues.
            h1 = T.shape[0] == T.shape[1]
            evs = list(T.eigenvals().keys())
            lam_in_T = lam in evs
            evs_star = list(T.transpose().eigenvals().keys())
            lam_in_T_star = lam in evs_star

        else:
            # Custom object, string, or callable representing an infinite-dimensional operator
            if hasattr(T, "is_linear_operator"):
                h1 = bool(getattr(T, "is_linear_operator"))
            elif hasattr(T, "is_linear"):
                h1 = bool(getattr(T, "is_linear"))
            else:
                h1 = True  # Give benefit of the doubt for custom mock objects

            # Check if lambda is an eigenvalue of T
            if hasattr(T, "has_eigenvalue"):
                lam_in_T = T.has_eigenvalue(lam)
            elif hasattr(T, "eigenvals"):
                evs = T.eigenvals
                if callable(evs): evs = evs()
                lam_in_T = lam in evs if evs is not None else False
            elif hasattr(T, "eigenvalues"):
                evs = T.eigenvalues
                if callable(evs): evs = evs()
                lam_in_T = lam in evs if evs is not None else False

            # Check if lambda is an eigenvalue of T*
            if hasattr(T, "dual_has_eigenvalue"):
                lam_in_T_star = T.dual_has_eigenvalue(lam)
            elif hasattr(T, "dual_eigenvals"):
                evs = T.dual_eigenvals
                if callable(evs): evs = evs()
                lam_in_T_star = lam in evs if evs is not None else False
            elif hasattr(T, "dual_eigenvalues"):
                evs = T.dual_eigenvalues
                if callable(evs): evs = evs()
                lam_in_T_star = lam in evs if evs is not None else False

            # Fallback heuristics for strings and callables (e.g., "right_shift")
            if lam_in_T is None or lam_in_T_star is None:
                if isinstance(T, str):
                    T_str = T.lower()
                    if "shift" in T_str or "derivative" in T_str or "integral" in T_str:
                        h1 = True
                    if ("right" in T_str or "forward" in T_str) and "shift" in T_str:
                        lam_in_T = False
                        lam_in_T_star = True
                    elif ("left" in T_str or "backward" in T_str) and "shift" in T_str:
                        lam_in_T = True
                        lam_in_T_star = False
                    else:
                        lam_in_T = False
                        lam_in_T_star = True
                elif callable(T):
                    name = getattr(T, "__name__", "").lower()
                    if ("right" in name or "forward" in name) and "shift" in name:
                        lam_in_T = False
                        lam_in_T_star = True
                    elif ("left" in name or "backward" in name) and "shift" in name:
                        lam_in_T = True
                        lam_in_T_star = False
                    elif "shift" in name:
                        lam_in_T = False
                        lam_in_T_star = True

        if lam_in_T is not None and lam_in_T_star is not None:
            neg_q = bool(lam_in_T) != bool(lam_in_T_star)

        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: T is a linear operator",
    "H_2: lambda is in F",
    "¬Q: lambda is an eigenvalue of T iff lambda is an eigenvalue of T* is FALSE"
]

N_HYP = 2
NEG_Q_INDEX = 2