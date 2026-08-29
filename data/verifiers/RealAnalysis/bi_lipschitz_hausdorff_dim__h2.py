import sympy
import math

# Top-level setup
# For abstract real analysis theorems where sets and functions cannot be easily 
# represented symbolically to compute Hausdorff dimensions, the witness is expected 
# to be a dictionary or object containing the boolean properties and dimensions.
# Example witness: 
# {'X_is_metric_space': True, 'Y_is_metric_space': True, 'A_is_subset_of_X': True, 'dim_A': 1, 'dim_fA': 2}

def conditions(witness) -> list[bool]:
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            h1 = bool(witness.get('X_is_metric_space', False) and witness.get('Y_is_metric_space', False))
            h2 = bool(witness.get('A_is_subset_of_X', False))
            dim_A = witness.get('dim_A', None)
            dim_fA = witness.get('dim_fA', None)
        elif isinstance(witness, tuple) and len(witness) == 2:
            # Fallback for simple tuple witness: (dim_A, dim_fA)
            h1 = True
            h2 = True
            dim_A, dim_fA = witness
        else:
            h1 = bool(getattr(witness, 'X_is_metric_space', False) and getattr(witness, 'Y_is_metric_space', False))
            h2 = bool(getattr(witness, 'A_is_subset_of_X', False))
            dim_A = getattr(witness, 'dim_A', None)
            dim_fA = getattr(witness, 'dim_fA', None)
            
        if dim_A is not None and dim_fA is not None:
            neg_q = float(dim_A) != float(dim_fA)
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: A is a subset of X",
    "¬Q: The Hausdorff dimension of A is not equal to the Hausdorff dimension of f(A)"
]

N_HYP = 2
NEG_Q_INDEX = 2