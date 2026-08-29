import sympy
from sympy import Matrix, MatrixBase, eye, zeros, fraction, simplify
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: B is a non-degenerate symmetric bilinear form on V",
    "H_2: T is a linear operator on V",
    "¬Q: There does not exist a unique linear operator T* such that B(T(x), y) = B(x, T*(y))"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    # 1. Duck-typing check for custom infinite-dimensional or abstract counterexamples
    if hasattr(witness, "is_non_degenerate_symmetric_bilinear_form"):
        try:
            h1 = bool(witness.is_non_degenerate_symmetric_bilinear_form())
            h2 = bool(witness.is_linear_operator())
            if hasattr(witness, "adjoint_exists"):
                neg_q = not bool(witness.adjoint_exists())
            elif hasattr(witness, "has_adjoint"):
                neg_q = not bool(witness.has_adjoint())
            else:
                neg_q = False
            return [h1, h2, neg_q]
        except Exception:
            pass

    # 2. Matrix check for finite-dimensional modules over rings (e.g., Z or R[x])
    try:
        B_raw, T_raw = None, None
        if isinstance(witness, (list, tuple)) and len(witness) >= 2:
            B_raw, T_raw = witness[0], witness[1]
        elif isinstance(witness, dict) and "B" in witness and "T" in witness:
            B_raw = witness["B"]
            T_raw = witness["T"]
            
        if B_raw is not None and T_raw is not None:
            if not isinstance(B_raw, MatrixBase):
                B = Matrix(B_raw)
            else:
                B = B_raw
            if not isinstance(T_raw, MatrixBase):
                T = Matrix(T_raw)
            else:
                T = T_raw
                
            if B.is_square and T.is_square and B.shape == T.shape:
                diff = simplify(B - B.transpose())
                is_sym = all(val == 0 for val in diff)
                det_B = simplify(B.det())
                
                # H1: B is symmetric and non-degenerate (injective map to dual <=> det != 0)
                h1 = is_sym and (det_B != 0)
                
                # H2: T is a linear operator (represented by a square matrix)
                h2 = True
                
                try:
                    # The adjoint T* must satisfy B * T* = T^T * B  =>  T* = B^{-1} * T^T * B
                    T_star = simplify(B.inv() * T.transpose() * B)
                    
                    # Determine if the base ring is Z (only integers)
                    base_ring_is_Z = True
                    for mat in (B, T):
                        for val in mat:
                            if any(not n.is_integer for n in val.atoms(sympy.Number)):
                                base_ring_is_Z = False
                                break
                        if not base_ring_is_Z:
                            break
                            
                    # Check if T* exists within the same ring
                    is_in_ring = True
                    for val in T_star:
                        if base_ring_is_Z:
                            # If base ring is Z, T* cannot have rational fractions
                            if any(not n.is_integer for n in val.atoms(sympy.Number)):
                                is_in_ring = False
                                break
                        
                        # Check for division by non-units (e.g., polynomials)
                        n_expr, d_expr = fraction(val)
                        if d_expr != 1:
                            if not d_expr.is_number:
                                is_in_ring = False
                                break
                                
                    neg_q = not is_in_ring
                except Exception:
                    # If B is not invertible over the field of fractions, we can't easily compute T*
                    neg_q = False
                    
                return [h1, h2, neg_q]
    except Exception:
        pass

    return [h1, h2, neg_q]