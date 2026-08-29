import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        A = sympy.Matrix(witness)
        if not A.is_square:
            return [False]
        
        n = A.shape[0]
        if n == 0:
            return [False]
        
        # Calculate the center and radius of the Gershgorin disk for each row
        centers = []
        radii = []
        for i in range(n):
            c = complex(sympy.N(A[i, i]))
            centers.append(c)
            r = sum(abs(complex(sympy.N(A[i, j]))) for j in range(n) if j != i)
            radii.append(r)
            
        # Find the eigenvalues of the matrix
        roots = []
        try:
            evals = A.eigenvals(multiple=True)
            if evals:
                roots = evals
        except Exception:
            pass
            
        if not roots:
            roots = A.charpoly().all_roots()
            
        if not roots:
            return [False]
        
        # Check if there is any eigenvalue strictly outside ALL Gershgorin disks
        neg_q = False
        for lam_sym in roots:
            lam = complex(sympy.N(lam_sym))
            
            in_any_disk = False
            for i in range(n):
                # Using a small tolerance for floating-point arithmetic
                if abs(lam - centers[i]) <= radii[i] + 1e-7:
                    in_any_disk = True
                    break
            
            if not in_any_disk:
                neg_q = True
                break
                
        return [neg_q]
    except Exception:
        return [False]

CONDITION_LABELS = [
    "¬Q: There exists an eigenvalue of A strictly outside the union of its Gershgorin disks"
]

N_HYP = 0
NEG_Q_INDEX = 0