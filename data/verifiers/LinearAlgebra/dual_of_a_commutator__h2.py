import sympy as sp
import math
import itertools
import functools

# Top-level setup: named object bindings
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

# Note: Square brackets are intentionally avoided in the labels to prevent regex parsing errors in the validation script.
CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: comm(S, T) = ST - TS is the commutator of S and T",
    "not Q: The dual operator of the commutator does not satisfy comm(S, T)^* = -comm(S^*, T^*)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        S, T = witness
    except Exception:
        return [False, False, False]

    # H_1: Let V be a vector space over a field F
    try:
        if hasattr(S, 'shape') and hasattr(T, 'shape'):
            h1 = (S.shape == T.shape) and (S.shape[0] == S.shape[1])
        else:
            # Fallback for custom objects: check if they support addition and multiplication
            _ = S + T
            _ = S * T
            h1 = True
    except Exception:
        h1 = False

    # H_2: Let comm(S, T) = ST - TS be the commutator of S and T
    try:
        comm = S * T - T * S
        h2 = True
    except Exception:
        h2 = False

    # ¬Q: The dual operator of the commutator does NOT satisfy comm(S, T)^* = -comm(S^*, T^*)
    try:
        def get_dual(x):
            if hasattr(x, 'dual'):
                return x.dual() if callable(x.dual) else x.dual
            if hasattr(x, 'adjoint'):
                return x.adjoint() if callable(x.adjoint) else x.adjoint
            if hasattr(x, 'transpose'):
                return x.transpose() if callable(x.transpose) else x.transpose
            if hasattr(x, 'T'):
                return x.T() if callable(x.T) else x.T
            if hasattr(x, 'H'):
                return x.H() if callable(x.H) else x.H
            return x

        lhs = get_dual(comm)
        rhs = -(get_dual(S) * get_dual(T) - get_dual(T) * get_dual(S))
        
        is_eq = False
        if lhs == rhs:
            is_eq = True
        else:
            try:
                diff = lhs - rhs
                if hasattr(diff, 'is_zero_matrix') and diff.is_zero_matrix:
                    is_eq = True
                elif diff == 0:
                    is_eq = True
                else:
                    if hasattr(diff, 'applyfunc'):
                        diff_simp = diff.applyfunc(sp.simplify)
                        if hasattr(diff_simp, 'is_zero_matrix') and diff_simp.is_zero_matrix:
                            is_eq = True
                    else:
                        diff_simp = sp.simplify(diff)
                        if diff_simp == 0:
                            is_eq = True
            except Exception:
                pass
                
        neg_q = not is_eq
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]