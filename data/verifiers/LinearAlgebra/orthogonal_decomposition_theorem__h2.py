import sympy
from sympy import Matrix, expand, simplify, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, tuple):
            if len(witness) == 2:
                W, v = witness
            elif len(witness) == 3:
                _, W, v = witness
            else:
                return [False, False, False]
        else:
            return [False, False, False]
            
        if isinstance(W, Matrix):
            W_list = [W[:, i] for i in range(W.shape[1])]
        elif isinstance(W, (list, tuple, set)):
            W_list = list(W)
        else:
            return [False, False, False]
            
        if not isinstance(v, Matrix):
            return [False, False, False]
            
        if W_list and not all(isinstance(x, Matrix) for x in W_list):
            return [False, False, False]
            
        if W_list and any(x.shape != v.shape for x in W_list):
            return [False, False, False]
            
        h1 = True
        h2 = True
        
        valid_pairs = 0
        for w in W_list:
            z = v - w
            is_orthogonal = True
            for x in W_list:
                val = z.dot(x)
                if val != 0:
                    if expand(val) != 0:
                        if simplify(val) != 0:
                            is_orthogonal = False
                            break
            if is_orthogonal:
                valid_pairs += 1
                
        neg_q = (valid_pairs != 1)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: V is an inner product space",
    "H_2: v is a vector in V",
    "¬Q: It is not true that there exist unique w in W and z in W^\\perp such that v = w + z"
]

N_HYP = 2
NEG_Q_INDEX = 2