import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        if isinstance(witness, dict):
            B = sp.Matrix(witness.get('B'))
            T = sp.Matrix(witness.get('T'))
            S = sp.Matrix(witness.get('S'))
            T_star = witness.get('T_star')
            S_star = witness.get('S_star')
            if T_star is not None:
                T_star = sp.Matrix(T_star)
            if S_star is not None:
                S_star = sp.Matrix(S_star)
        elif isinstance(witness, (tuple, list)) and len(witness) == 5:
            B = sp.Matrix(witness[0])
            T = sp.Matrix(witness[1])
            S = sp.Matrix(witness[2])
            T_star = sp.Matrix(witness[3])
            S_star = sp.Matrix(witness[4])
        elif isinstance(witness, (tuple, list)) and len(witness) == 3:
            B = sp.Matrix(witness[0])
            T = sp.Matrix(witness[1])
            S = sp.Matrix(witness[2])
            T_star = None
            S_star = None
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H1: V is a finite-dimensional vector space over a field F
    try:
        n = B.rows
        h1 = bool(n > 0 and B.cols == n and 
                  T.rows == n and T.cols == n and 
                  S.rows == n and S.cols == n)
    except Exception:
        h1 = False

    # H2: B is a non-degenerate bilinear form on V
    try:
        h2 = bool(h1 and B.det() != 0)
    except Exception:
        h2 = False

    # H3: T^* and S^* are the adjoints of T and S respectively with respect to B
    try:
        if h2:
            B_inv = B.inv()
            
            def1_T = def2_T = def3_T = def4_T = False
            def1_S = def2_S = def3_S = def4_S = False
            
            if T_star is not None and S_star is not None:
                if T_star.rows == n and T_star.cols == n and S_star.rows == n and S_star.cols == n:
                    def1_T = (B * T_star == T.transpose() * B)
                    def2_T = (B.transpose() * T_star == T.transpose() * B)
                    def3_T = (B.transpose() * T_star == T.transpose() * B.transpose())
                    def4_T = (B * T_star == T.transpose() * B.transpose())
                    
                    def1_S = (B * S_star == S.transpose() * B)
                    def2_S = (B.transpose() * S_star == S.transpose() * B)
                    def3_S = (B.transpose() * S_star == S.transpose() * B.transpose())
                    def4_S = (B * S_star == S.transpose() * B.transpose())
            else:
                T_star = B_inv * T.transpose() * B
                S_star = B_inv * S.transpose() * B
                def1_T = def1_S = True
                
            h3 = bool((def1_T and def1_S) or (def2_T and def2_S) or (def3_T and def3_S) or (def4_T and def4_S))
        else:
            h3 = False
    except Exception:
        h3 = False

    # neg_Q: (T \circ S)^* \neq S^* \circ T^*
    try:
        neg_q = False
        if h3:
            TS = T * S
            if def1_T and def1_S:
                lhs = B * (S_star * T_star)
                rhs = TS.transpose() * B
                neg_q = bool(lhs != rhs)
            elif def2_T and def2_S:
                lhs = B.transpose() * (S_star * T_star)
                rhs = TS.transpose() * B
                neg_q = bool(lhs != rhs)
            elif def3_T and def3_S:
                lhs = B.transpose() * (S_star * T_star)
                rhs = TS.transpose() * B.transpose()
                neg_q = bool(lhs != rhs)
            elif def4_T and def4_S:
                lhs = B * (S_star * T_star)
                rhs = TS.transpose() * B.transpose()
                neg_q = bool(lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: V is a finite-dimensional vector space over a field F",
    "H_2: B is a non-degenerate bilinear form on V",
    "H_3: T^* and S^* are the adjoints of T and S respectively with respect to B",
    "¬Q: (T \\circ S)^* \\neq S^* \\circ T^*"
]

N_HYP = 3
NEG_Q_INDEX = 3