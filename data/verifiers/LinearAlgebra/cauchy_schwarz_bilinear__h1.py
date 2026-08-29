import sympy

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness is expected to be a tuple (B, u, v) where:
      - B is a sympy Matrix representing the symmetric bilinear form.
      - u, v are sympy Matrices representing the vectors in V.
    """
    try:
        B, u, v = witness
    except Exception:
        return [False, False, False]

    # H_1: B is a symmetric bilinear form on V
    h1 = False
    try:
        if hasattr(B, 'is_square') and B.is_square:
            h1 = bool(B == B.T)
    except Exception:
        pass

    # H_2: B is positive definite
    h2 = False
    try:
        if hasattr(B, 'is_square') and B.is_square:
            is_pd = True
            # Sylvester's criterion: all leading principal minors must be strictly positive
            for i in range(1, B.rows + 1):
                minor_det = B[:i, :i].det()
                try:
                    if bool(minor_det <= 0):
                        is_pd = False
                        break
                except TypeError:
                    # If minor_det is complex or symbolic such that <= 0 cannot be evaluated
                    is_pd = False
                    break
            h2 = is_pd
    except Exception:
        pass

    # ¬Q: There exist u, v in V such that (B(u,v))^2 > B(u,u)B(v,v)
    neg_q = False
    try:
        if hasattr(B, 'is_square') and B.is_square:
            if not isinstance(u, sympy.Matrix):
                u_mat = sympy.Matrix(u)
            else:
                u_mat = u
            if not isinstance(v, sympy.Matrix):
                v_mat = sympy.Matrix(v)
            else:
                v_mat = v
                
            # Evaluate the bilinear form B(x, y) = x^T * B * y
            B_uv = (u_mat.T * B * v_mat)[0, 0]
            B_uu = (u_mat.T * B * u_mat)[0, 0]
            B_vv = (v_mat.T * B * v_mat)[0, 0]

            lhs = B_uv**2
            rhs = B_uu * B_vv
            diff = sympy.simplify(lhs - rhs)
            
            try:
                if bool(diff > 0):
                    neg_q = True
            except TypeError:
                # Fallback for complex numbers with zero imaginary part
                try:
                    c = complex(diff)
                    if abs(c.imag) < 1e-9 and c.real > 0:
                        neg_q = True
                except Exception:
                    pass
    except Exception:
        pass

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: B is a symmetric bilinear form on V",
    "H_2: B is positive definite",
    "¬Q: There exist u, v in V such that (B(u,v))^2 > B(u,u)B(v,v)"
]

N_HYP = 2
NEG_Q_INDEX = 2