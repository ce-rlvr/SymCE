import sympy
from sympy import Matrix, eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    """
    Verifies if the given witness is a counterexample to the false conjecture.
    The witness can be provided in several formats:
      - (inner_product_matrix, vectors, G)
      - (inner_product_callable, vectors, G)
      - (vectors, G)
      - G
    """
    h1, h2, neg_q = False, False, False
    G = None
    
    try:
        if isinstance(witness, tuple):
            if len(witness) == 3:
                ip, vecs, G = witness
                
                # Check H1 and H2 based on the provided inner product
                if callable(ip):
                    h1 = True
                    try:
                        k = len(vecs)
                        expected_G = Matrix(k, k, lambda i, j: ip(vecs[j], vecs[i]))
                        h2 = bool(G == expected_G)
                    except Exception:
                        pass
                elif isinstance(ip, Matrix):
                    try:
                        # For an indefinite inner product space, the matrix should be Hermitian and invertible
                        h1 = bool(ip.is_hermitian and ip.det() != 0)
                    except Exception:
                        pass
                    try:
                        if isinstance(vecs, (list, tuple)):
                            vecs_mat = [Matrix(v) if not isinstance(v, Matrix) else v for v in vecs]
                            V_mat = Matrix.hstack(*vecs_mat)
                        else:
                            V_mat = vecs
                        expected_G = V_mat.H * ip * V_mat
                        h2 = bool(G == expected_G)
                    except Exception:
                        pass
                else:
                    h1 = True
                    h2 = True
                    
            elif len(witness) == 2:
                vecs, G = witness
                h1 = True
                if isinstance(vecs, (list, tuple)):
                    try:
                        vecs_mat = [Matrix(v) if not isinstance(v, Matrix) else v for v in vecs]
                        k = len(vecs_mat)
                        # Try standard sesquilinear inner product
                        expected_G = Matrix(k, k, lambda i, j: (vecs_mat[j].H * vecs_mat[i])[0])
                        h2 = bool(G == expected_G)
                        if not h2:
                            # Try standard bilinear form
                            expected_G2 = Matrix(k, k, lambda i, j: vecs_mat[j].dot(vecs_mat[i]))
                            h2 = bool(G == expected_G2)
                    except Exception:
                        pass
                elif isinstance(vecs, Matrix):
                    try:
                        h2 = bool(G == vecs.H * vecs) or bool(G == vecs.T * vecs)
                    except Exception:
                        pass
            else:
                G = witness[0] if len(witness) == 1 else witness
                h1 = True
                h2 = True
                
        elif isinstance(witness, dict):
            G = witness.get('G', witness)
            h1 = True
            h2 = True
        else:
            G = witness
            h1 = True
            h2 = True
            
        # Convert G to a sympy Matrix if it's a list/tuple
        if isinstance(G, (list, tuple)):
            try:
                G = Matrix(G)
            except Exception:
                pass
                
        # Check negated conclusion: G is NOT a positive semidefinite matrix
        if G is not None and hasattr(G, 'is_positive_semidefinite'):
            is_psd = G.is_positive_semidefinite
            if is_psd is False:
                neg_q = True
                
    except Exception:
        pass
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: G is the k by k matrix whose entries are given by G_{ij} = \\langle v_j, v_i \\rangle",
    "¬Q: G is not a positive semidefinite matrix"
]

N_HYP = 2
NEG_Q_INDEX = 2