import sympy
from sympy import eye, zeros, Rational, Integer, Symbol
from sympy.abc import x, y, z

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        # Attempt to convert list of lists to a sympy Matrix
        if isinstance(witness, (list, tuple)):
            try:
                if len(witness) > 0 and isinstance(witness[0], (list, tuple)):
                    witness = sympy.Matrix(witness)
            except Exception:
                pass
        
        if hasattr(witness, 'is_Matrix') and witness.is_Matrix:
            # A minimal polynomial over R is only well-defined for square matrices
            if witness.shape[0] != witness.shape[1]:
                neg_q = False
            else:
                n = witness.shape[0]
                I_mat = sympy.eye(n)
                
                # Helper to split matrix entries into real and imaginary parts
                # to ensure we are checking linear dependence over the Reals.
                def get_ri_vec(m):
                    vec = []
                    for i in range(n):
                        for j in range(n):
                            val = m[i, j]
                            if hasattr(val, 'as_real_imag'):
                                try:
                                    re_part, im_part = val.as_real_imag()
                                    vec.append(re_part)
                                    vec.append(im_part)
                                except Exception:
                                    vec.append(val)
                                    vec.append(0)
                            else:
                                vec.append(val)
                                vec.append(0)
                    return sympy.Matrix(vec)

                v1 = get_ri_vec(I_mat)
                v2 = get_ri_vec(witness)
                v3 = get_ri_vec(witness**2)
                
                # If the matrix satisfies a polynomial of degree 1 or 2 over R,
                # then I, M, and M^2 must be linearly dependent over R.
                mat = sympy.Matrix.hstack(v1, v2, v3)
                has_deg_1_2 = (mat.rank() <= 2)
                neg_q = not has_deg_1_2

        elif hasattr(witness, 'is_Expr') and witness.is_Expr:
            if witness.is_number:
                # Any real or complex number has a minimal polynomial over R of degree 1 or 2
                neg_q = False
            else:
                # Symbolic expressions are transcendental over R (degree is not 1 or 2)
                neg_q = True
                
        elif isinstance(witness, sympy.Poly):
            # Polynomials are transcendental over R
            neg_q = True
            
        else:
            # Not a valid mathematical object for this context
            neg_q = False
            
    except Exception:
        neg_q = False

    return [neg_q]

CONDITION_LABELS = [
    "¬Q: The minimal polynomial of alpha over R does not have degree 1 or 2"
]

N_HYP = 0
NEG_Q_INDEX = 0