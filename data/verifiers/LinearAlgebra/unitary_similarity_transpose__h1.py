import sympy as sp

I2 = sp.eye(2)
I3 = sp.eye(3)
O2 = sp.zeros(2, 2)
O3 = sp.zeros(3, 3)

def conditions(witness):
    try:
        n = witness.shape[0]
        I = sp.eye(n)
        prod = witness * witness.H
        if prod == I:
            H1 = True
        else:
            diff = sp.simplify(prod - I)
            H1 = all(diff[i, j] == 0 for i in range(n) for j in range(n))
    except Exception:
        H1 = False

    try:
        # neg_Q: There does NOT exist a unitary matrix V such that V U V^* = U^T
        # This is equivalent to saying U and U^T are NOT unitarily similar.
        # We check this by comparing the traces of words in {U, U^*} and {U^T, (U^T)^*}.
        # By Specht's theorem, if they are unitarily similar, all corresponding words must have equal traces.
        n = witness.shape[0]
        U = witness
        U_T = witness.T
        U_adj = witness.H
        U_T_adj = U_T.H
        
        neg_Q = False
        current_U = [U, U_adj]
        current_UT = [U_T, U_T_adj]
        
        for length in range(1, 6):
            for wU, wUT in zip(current_U, current_UT):
                diff = wU.trace() - wUT.trace()
                if diff != 0:
                    if hasattr(diff, 'simplify'):
                        diff = sp.simplify(diff)
                    if diff != 0:
                        neg_Q = True
                        break
            if neg_Q:
                break
            
            if length < 5:
                next_U = []
                next_UT = []
                for wU, wUT in zip(current_U, current_UT):
                    next_U.extend([wU * U, wU * U_adj])
                    next_UT.extend([wUT * U_T, wUT * U_T_adj])
                current_U = next_U
                current_UT = next_UT
                
    except Exception:
        neg_Q = False

    return [H1, neg_Q]

CONDITION_LABELS = [
    "H_1: U is a unitary matrix",
    "¬Q: There does not exist a unitary matrix V such that V U V^* = U^T"
]

N_HYP = 1
NEG_Q_INDEX = 1