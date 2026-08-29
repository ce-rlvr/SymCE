import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    # H_1: A is a square matrix
    try:
        if not hasattr(witness, 'jordan_form'):
            return [False, False]
        if not hasattr(witness, 'shape') or len(witness.shape) != 2:
            return [False, False]
        if witness.shape[0] != witness.shape[1]:
            return [False, False]
        h1 = True
    except Exception:
        return [False, False]
        
    # ¬Q: The Jordan canonical form of adj(A) does NOT have the exact same block structure 
    # as J with eigenvalues replaced by det(A)/lambda.
    try:
        A = witness
        det_A = A.det()
        P, J = A.jordan_form()
        
        def extract_blocks(mat):
            n = mat.shape[0]
            blocks = []
            i = 0
            while i < n:
                lam = mat[i, i]
                size = 1
                # In SymPy's Jordan form, 1s are placed on the superdiagonal for each block
                while i + size < n and mat[i + size, i + size] == lam and mat[i + size - 1, i + size] == 1:
                    size += 1
                blocks.append((lam, size))
                i += size
            return blocks
            
        blocks_A = extract_blocks(J)
        
        # If any eigenvalue is 0, the replacement det(A)/lambda is undefined (division by zero).
        # Thus, the conclusion's required block structure cannot even be formed, so the conclusion fails.
        has_zero_eigenvalue = False
        for lam, size in blocks_A:
            if sympy.simplify(lam) == 0:
                has_zero_eigenvalue = True
                break
                
        if has_zero_eigenvalue:
            neg_q = True
        else:
            expected_blocks = []
            for lam, size in blocks_A:
                expected_blocks.append((sympy.simplify(det_A / lam), size))
                
            adj_A = A.adjugate()
            P_adj, J_adj = adj_A.jordan_form()
            blocks_adj = extract_blocks(J_adj)
            
            def multisets_match(l1, l2):
                if len(l1) != len(l2): return False
                l2_copy = list(l2)
                for item1 in l1:
                    found = False
                    for i, item2 in enumerate(l2_copy):
                        if sympy.simplify(item1[0] - item2[0]) == 0 and item1[1] == item2[1]:
                            l2_copy.pop(i)
                            found = True
                            break
                    if not found:
                        return False
                return True
                
            q = multisets_match(expected_blocks, blocks_adj)
            neg_q = not q
            
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: A is a square matrix",
    "¬Q: The Jordan canonical form of adj(A) does not have the exact same block structure as J with eigenvalues replaced by det(A)/lambda"
]

N_HYP = 1
NEG_Q_INDEX = 1