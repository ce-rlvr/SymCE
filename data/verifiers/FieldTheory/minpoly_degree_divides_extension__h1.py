import sympy as sp

# Top-level setup
I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

N3 = sp.Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])
N3_sq = N3**2

def conditions(witness):
    try:
        if isinstance(witness, dict):
            if 'alpha' in witness and 'E_basis' in witness:
                alpha = witness['alpha']
                E_basis = witness['E_basis']
                
                if not getattr(alpha, 'is_Matrix', False):
                    return [False, False]
                
                vecs = [sp.Matrix(list(b)) for b in E_basis]
                M = sp.Matrix.hstack(*vecs)
                
                alpha_vec = sp.Matrix(list(alpha))
                
                h1 = (M.rank() == sp.Matrix.hstack(M, alpha_vec).rank())
                
                deg_E = M.rank()
                
                I = sp.eye(alpha.shape[0])
                powers = [sp.Matrix(list(I))]
                deg_minpoly = None
                curr_alpha = I
                for d in range(1, deg_E + 2):
                    curr_alpha = curr_alpha * alpha
                    powers.append(sp.Matrix(list(curr_alpha)))
                    P = sp.Matrix.hstack(*powers)
                    if P.rank() < d + 1:
                        deg_minpoly = d
                        break
                
                if deg_minpoly is None:
                    deg_minpoly = float('inf')
                    
                if deg_E == sp.oo or deg_minpoly == float('inf'):
                    divides = False
                elif deg_minpoly == 0:
                    divides = False
                else:
                    divides = (deg_E % deg_minpoly == 0)
                    
                neg_q = not divides
                return [h1, neg_q]
            
            elif 'deg_E_F' in witness and 'deg_minpoly' in witness:
                deg_E = witness['deg_E_F']
                deg_minpoly = witness['deg_minpoly']
                h1 = witness.get('alpha_in_E', True)
                
                if deg_E == sp.oo or deg_minpoly == sp.oo or deg_minpoly == float('inf'):
                    divides = False
                elif deg_minpoly == 0:
                    divides = False
                else:
                    divides = (deg_E % deg_minpoly == 0)
                    
                neg_q = not divides
                return [bool(h1), neg_q]
                
        elif isinstance(witness, tuple) and len(witness) == 2:
            deg_E, deg_minpoly = witness
            h1 = True
            if deg_minpoly == 0:
                divides = False
            else:
                divides = (deg_E % deg_minpoly == 0)
            return [h1, not divides]
                
    except Exception:
        pass
    
    return [False, False]

CONDITION_LABELS = [
    "H_1: alpha is an element of E",
    "not Q: The degree of the minimal polynomial of alpha over F does not divide the degree of E over F"
]

N_HYP = 1
NEG_Q_INDEX = 1