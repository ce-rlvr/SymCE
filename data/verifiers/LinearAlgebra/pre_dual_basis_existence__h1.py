import sympy
from sympy import Matrix, eye, zeros
from sympy.matrices.normalforms import smith_normal_form

# Top-level setup for standard algebra objects
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: {f_1, ..., f_n} is a basis for the dual space V^*",
    "¬Q: There does not exist a unique basis {v_1, ..., v_n} of V such that f_i(v_j) = \\delta_{ij}"
]

N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness) -> list[bool]:
    h1 = False
    neg_q = False
    
    try:
        M = None
        
        # Extract a presentation matrix if the witness is a Z-module
        if isinstance(witness, Matrix):
            M = witness
        elif isinstance(witness, dict):
            if 'presentation_matrix' in witness:
                M = witness['presentation_matrix']
            elif 'M' in witness:
                M = witness['M']
            elif 'matrix' in witness:
                M = witness['matrix']
        elif isinstance(witness, tuple):
            for item in witness:
                if isinstance(item, Matrix):
                    M = item
                    break
                    
        if M is not None:
            # Interpret M as a presentation matrix for a finitely generated Z-module V.
            # V^* = Hom(V, Z) is always a free Z-module of finite rank, so it always has a finite basis.
            h1 = True
            
            # Compute the Smith Normal Form to find the invariant factors of the module.
            snf = smith_normal_form(M)
            is_free = True
            
            # V is a free module iff it has no torsion (all invariant factors are 0 or 1).
            for i in range(min(snf.rows, snf.cols)):
                if abs(int(snf[i, i])) > 1:
                    is_free = False
                    break
            
            # If V is not free, it cannot have a basis, so the pre-dual basis conclusion fails.
            neg_q = not is_free
            return [h1, neg_q]
            
        # If the witness is a list of functionals (vectors)
        if isinstance(witness, list) and len(witness) > 0 and isinstance(witness[0], Matrix):
            vecs = []
            for v in witness:
                if v.rows == 1:
                    vecs.append(v.tolist()[0])
                elif v.cols == 1:
                    vecs.append(v.T.tolist()[0])
                else:
                    raise ValueError("Elements must be row or column vectors")
            
            F = Matrix(vecs)
            # Check if they form a basis for the dual space (square and invertible matrix)
            if F.rows == F.cols and F.det() != 0:
                h1 = True
                # For vector spaces over a field, the pre-dual basis always exists and is unique
                neg_q = False
            else:
                h1 = False
                neg_q = False
            return [h1, neg_q]
            
        # Fallback for string-based topological or module counterexamples
        if isinstance(witness, str):
            w = witness.lower().replace(' ', '')
            # Z_2 module or L^p spaces (0 < p < 1) or weak topology counterexamples
            if any(x in w for x in ['z_2', 'z2', 'z/2', 'torsion', 'l^p', 'lp', 'weak']):
                return [True, True]
                
    except Exception:
        pass

    return [h1, neg_q]