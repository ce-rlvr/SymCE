import sympy
import sympy.combinatorics
import sympy.combinatorics.named_groups
import sympy.combinatorics.permutations
import sympy.matrices
import sympy.ntheory
import sympy.abc
import sympy.polys
import z3
import math
import itertools
import functools

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        if not isinstance(witness, sympy.MatrixBase):
            try:
                witness = sympy.Matrix(witness)
            except Exception:
                return [False]
        
        if witness.rows != witness.cols:
            return [False]
            
        n = witness.rows
        if n == 0:
            return [False]
            
        # Construct the n x n Discrete Fourier Transform (DFT) matrix
        omega = sympy.exp(-2 * sympy.pi * sympy.I / n)
        F = sympy.Matrix(n, n, lambda j, k: omega**(j * k) / sympy.sqrt(n))
        
        # Check if the witness is diagonalized by the DFT matrix.
        # We check both F * C * F^H and F^H * C * F to accommodate different conventions
        # for the DFT matrix (e.g., whether the exponent is positive or negative).
        D1 = F * witness * F.H
        D2 = F.H * witness * F
        
        def is_diagonal(M):
            for i in range(n):
                for j in range(n):
                    if i != j:
                        val = sympy.expand(M[i, j])
                        if val != 0:
                            val = sympy.simplify(val)
                            if val != 0:
                                try:
                                    # Fallback to numerical evaluation if symbolic simplification leaves a non-zero expression
                                    c_val = complex(val.evalf())
                                    if abs(c_val) > 1e-9:
                                        return False
                                except Exception:
                                    # If it cannot be evaluated to a complex number, assume it's non-zero
                                    return False
            return True
            
        is_diag1 = is_diagonal(D1)
        is_diag2 = is_diagonal(D2)
        
        # The conclusion Q is that C is unitarily diagonalizable by the DFT matrix.
        # We want neg_Q to be True when this conclusion FAILS.
        neg_Q = not (is_diag1 or is_diag2)
        
        return [neg_Q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: C is not unitarily diagonalizable by the DFT matrix"
]

N_HYP = 0
NEG_Q_INDEX = 0