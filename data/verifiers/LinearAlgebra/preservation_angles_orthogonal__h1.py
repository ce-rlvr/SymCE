import sympy
from sympy import Matrix, eye, zeros, sqrt
import math

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            u = witness.get('u')
            v = witness.get('v')
            Q = witness.get('Q')
        else:
            u, v, Q = witness
    except Exception:
        return [False, False, False]

    try:
        h1 = (isinstance(u, Matrix) and isinstance(v, Matrix) and isinstance(Q, Matrix) and
              u.shape[1] == 1 and v.shape[1] == 1 and 
              u.shape[0] == v.shape[0] and Q.shape == (u.shape[0], u.shape[0]) and
              not all(x == 0 for x in u) and not all(x == 0 for x in v) and
              all(x.is_real for x in u) and all(x.is_real for x in v) and all(x.is_real for x in Q))
    except Exception:
        h1 = False

    try:
        # The second hypothesis defines theta as the angle between u and v.
        # This is well-defined as long as u and v are valid non-zero real vectors.
        h2 = h1
    except Exception:
        h2 = False

    try:
        Qu = Q * u
        Qv = Q * v
        
        # If either Qu or Qv is the zero vector, the angle between them is undefined,
        # so it cannot be exactly theta.
        if all(x == 0 for x in Qu) or all(x == 0 for x in Qv):
            neg_q = True
        else:
            dot_uv = sum(u[i]*v[i] for i in range(u.shape[0]))
            norm_u = sqrt(sum(u[i]**2 for i in range(u.shape[0])))
            norm_v = sqrt(sum(v[i]**2 for i in range(v.shape[0])))
            cos_theta = dot_uv / (norm_u * norm_v)
            
            dot_QuQv = sum(Qu[i]*Qv[i] for i in range(Qu.shape[0]))
            norm_Qu = sqrt(sum(Qu[i]**2 for i in range(Qu.shape[0])))
            norm_Qv = sqrt(sum(Qv[i]**2 for i in range(Qv.shape[0])))
            cos_phi = dot_QuQv / (norm_Qu * norm_Qv)
            
            diff = cos_theta - cos_phi
            # If the cosines of the angles are different, the angles are different.
            neg_q = abs(complex(diff.evalf())) > 1e-9
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: u and v are non-zero vectors in R^n",
    "H_2: theta is the angle between u and v",
    "¬Q: The angle between Qu and Qv is not exactly theta"
]

N_HYP = 2
NEG_Q_INDEX = 2