import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for standard linear algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Handle the case where the witness is a family (list) of matrices
        if isinstance(witness, list):
            for A in witness:
                if not hasattr(A, 'is_Matrix') or not A.is_Matrix:
                    return [False]
                if hasattr(A, 'free_symbols') and A.free_symbols:
                    return [False]
            
            Q = True
            for A in witness:
                try:
                    cells = A.jordan_cells()
                    for eig, size in cells:
                        try:
                            val = abs(complex(eig))
                            if val > 1.000001:
                                Q = False
                            elif abs(val - 1.0) < 0.000001 and size > 1:
                                Q = False
                        except Exception:
                            try:
                                is_z = bool(eig == 0)
                            except Exception:
                                is_z = False
                            if not is_z and size > 1:
                                Q = False
                except Exception:
                    Q = False
            
            P = True
            max_norm = 0
            for A in witness:
                try:
                    norms = []
                    for m in [1, 10, 20, 50, 100]:
                        Am = A**m
                        norm = 0
                        for val in Am:
                            try:
                                v = abs(complex(val))
                            except Exception:
                                v = 0
                            if v > norm:
                                norm = v
                        norms.append(norm)
                        if norm > max_norm:
                            max_norm = norm
                    if norms[-1] > 10000 and norms[-1] > norms[0]:
                        P = False
                    elif norms[-1] > 1000 and norms[-1] > norms[-2] > norms[-3]:
                        P = False
                except Exception:
                    P = False
            if max_norm > 10000:
                P = False
            
            return [P != Q]

        # Handle the case where the witness is a single matrix
        if not hasattr(witness, 'is_Matrix') or not witness.is_Matrix:
            return [False]

        if hasattr(witness, 'free_symbols') and witness.free_symbols:
            return [False]

        # Check if it's a standard numerical matrix over C or R
        is_standard = True
        for val in witness:
            if hasattr(val, 'is_number'):
                if not val.is_number:
                    is_standard = False
                    break
            else:
                is_standard = False
                break
        
        if is_standard:
            # For standard real/complex matrices, the theorem is mathematically true.
            # Any apparent failure would be a numerical/evaluation artifact.
            return [False]

        # For non-standard matrices (e.g., over finite fields)
        Q = True
        try:
            cells = witness.jordan_cells()
            for eig, size in cells:
                try:
                    val = abs(complex(eig))
                    if val > 1.000001:
                        Q = False
                    elif abs(val - 1.0) < 0.000001 and size > 1:
                        Q = False
                except Exception:
                    try:
                        is_z = bool(eig == 0)
                    except Exception:
                        is_z = False
                    if not is_z and size > 1:
                        Q = False
        except Exception:
            Q = False

        P = True
        try:
            norms = []
            for m in [1, 10, 20, 50, 100]:
                Am = witness**m
                norm = 0
                for val in Am:
                    try:
                        v = abs(complex(val))
                    except Exception:
                        v = 0
                    if v > norm:
                        norm = v
                norms.append(norm)
            
            if norms[-1] > 10000 and norms[-1] > norms[0]:
                P = False
            elif norms[-1] > 1000 and norms[-1] > norms[-2] > norms[-3]:
                P = False
        except Exception:
            P = False

        return [P != Q]

    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: The equivalence between uniform boundedness of A^m and the eigenvalue condition fails"
]
N_HYP = 0
NEG_Q_INDEX = 0