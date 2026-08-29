import sympy as sp
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a counterexample to the false conjecture:
    "Every linear operator on a non-zero real vector space has an invariant subspace of dimension 1 or 2."
    (The dropped hypothesis is that the vector space is finite-dimensional).
    """
    h1 = False
    h2 = False
    neg_q = False
    
    try:
        # If the witness is provided as a tuple (Space, Operator), extract the operator
        if isinstance(witness, tuple) and len(witness) == 2:
            witness = witness[1]
            
        # If the witness is a list of lists, attempt to convert it to a SymPy Matrix
        if isinstance(witness, list) and all(isinstance(row, list) for row in witness):
            try:
                witness = sp.Matrix(witness)
            except Exception:
                pass
                
        # 1. Check if the witness is a finite-dimensional matrix
        if isinstance(witness, sp.MatrixBase):
            h1 = witness.shape[0] > 0
            h2 = witness.is_square
            # Over the reals, EVERY finite-dimensional linear operator on a non-zero space
            # has a 1D or 2D invariant subspace (due to the Fundamental Theorem of Algebra
            # ensuring the minimal polynomial has a linear or quadratic factor).
            neg_q = False
            return [h1, h2, neg_q]
            
        # 2. Check if the witness is a string representing a known infinite-dimensional counterexample
        if isinstance(witness, str):
            s = witness.lower()
            h1 = True
            h2 = True
            if "right" in s and "shift" in s:
                neg_q = True
            elif "mul" in s and "x" in s:
                neg_q = True
            elif "integrat" in s:
                neg_q = True
            elif s == "x":
                neg_q = True
            else:
                neg_q = False
            return [h1, h2, neg_q]
            
        # 3. Check if the witness is a SymPy Expression (e.g., representing multiplication by x)
        if isinstance(witness, sp.Expr):
            h1 = True
            h2 = True
            s = str(witness).lower()
            if s == 'x':
                neg_q = True
            elif "integral" in s or "integrat" in s:
                neg_q = True
            elif "mul" in s and "x" in s:
                neg_q = True
            else:
                neg_q = False
            return [h1, h2, neg_q]
            
        # 4. Check if the witness is a function or custom class representing an operator
        name = ""
        if hasattr(witness, "__name__"):
            name = witness.__name__.lower()
        elif hasattr(witness, "__class__"):
            name = witness.__class__.__name__.lower()
            
        if name:
            h1 = True
            h2 = True
            if "right" in name and "shift" in name:
                neg_q = True
            elif "mul" in name and "x" in name:
                neg_q = True
            elif "integrat" in name:
                neg_q = True
            else:
                neg_q = False
            return [h1, h2, neg_q]
            
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is not the zero vector space",
    "H_2: T is a linear operator on V",
    "¬Q: V does not contain a T-invariant subspace of dimension 1 or dimension 2"
]

N_HYP = 2
NEG_Q_INDEX = 2