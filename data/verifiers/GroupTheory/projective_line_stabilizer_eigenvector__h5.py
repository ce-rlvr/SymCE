import sympy
from sympy import Matrix, eye, zeros

# Top-level setup
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        # Parse witness
        T = None
        if isinstance(witness, dict):
            v = witness.get('v')
            u = witness.get('u') or witness.get('L')
            T = witness.get('T')
        elif isinstance(witness, (list, tuple)):
            if len(witness) == 2:
                v, u = witness
            elif len(witness) == 3:
                v, u, T = witness
            else:
                return [False] * 5
        else:
            return [False] * 5

        if isinstance(u, (list, tuple)) and len(u) == 1 and isinstance(u[0], (list, tuple)):
            u = u[0]
            
        v = Matrix(v)
        if v.shape[0] == 1 and v.shape[1] >= 1:
            v = v.T
            
        u = Matrix(u)
        if u.shape[0] == 1 and u.shape[1] >= 1:
            u = u.T
            
        if T is not None:
            T = Matrix(T)
            
        # H1: V is a vector space (v and u are column vectors of the same dimension)
        h1 = bool(v.shape[1] == 1 and u.shape[1] == 1 and 
                  v.shape[0] == u.shape[0] and v.shape[0] >= 1)
              
        # H2: GL(V) is the general linear group of V (structural, true if H1 holds)
        h2 = h1
        
        # H3: P(V) is the projective space, L is a 1-dimensional subspace
        # This requires u to be a non-zero vector so that span(u) is 1-dimensional.
        h3 = bool(h1 and not all(x == 0 for x in u))
        
        # H4: GL(V) acts on P(V) (structural, true if H1 holds)
        h4 = h1
        
        # neg_Q: The stabilizer of L in GL(V) does NOT consist exactly of those 
        # linear transformations in GL(V) for which v is an eigenvector.
        neg_q = False
        if h1 and h3:
            if T is not None:
                # Check if T is in GL(V)
                if T.shape[0] == T.shape[1] and T.shape[0] == v.shape[0] and T.det() != 0:
                    # T in S_L iff T(u) is in span(u)
                    in_S_L = (u.row_join(T * u).rank() == 1)
                    
                    # T in E_v iff v != 0 and T(v) is in span(v)
                    if all(x == 0 for x in v):
                        in_E_v = False
                    else:
                        in_E_v = (v.row_join(T * v).rank() == 1)
                        
                    neg_q = bool(in_S_L != in_E_v)
            else:
                # If T is not provided, we check if S_L != E_v globally.
                # S_L == E_v iff L = span(v) and v != 0.
                if all(x == 0 for x in v):
                    neg_q = True
                else:
                    M = v.row_join(u)
                    neg_q = bool(M.rank() == 2)
                    
        return [h1, h2, h3, h4, neg_q]
    except Exception:
        return [False, False, False, False, False]

CONDITION_LABELS = [
    "H_1: V is a vector space over a field F",
    "H_2: GL(V) is the general linear group of V",
    "H_3: P(V) is the projective space of V, consisting of all 1-dimensional subspaces",
    "H_4: GL(V) acts on P(V) via T * span(u) = span(T(u))",
    "¬Q: The stabilizer of L in GL(V) does not consist exactly of those linear transformations for which v is an eigenvector"
]

N_HYP = 4
NEG_Q_INDEX = 4