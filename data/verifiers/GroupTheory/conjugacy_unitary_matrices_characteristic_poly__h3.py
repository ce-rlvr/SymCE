import sympy
from sympy import eye, zeros
from itertools import product

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

CONDITION_LABELS = [
    "H_1: A and B are square matrices of the same size n >= 1",
    "¬Q: A and B have the same characteristic polynomial but are not conjugate in U(n)"
]
N_HYP = 1
NEG_Q_INDEX = 1

def conditions(witness):
    try:
        if not isinstance(witness, (list, tuple)):
            return [False, False]
        
        if len(witness) == 2:
            A, B = witness
        elif len(witness) == 3:
            _, A, B = witness
        else:
            return [False, False]
            
        try:
            if not isinstance(A, sympy.MatrixBase):
                A = sympy.Matrix(A)
            if not isinstance(B, sympy.MatrixBase):
                B = sympy.Matrix(B)
        except Exception:
            return [False, False]
            
        if A.rows != A.cols or B.rows != B.cols:
            h1 = False
        elif A.rows != B.rows or A.rows < 1:
            h1 = False
        else:
            h1 = True
            
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            x = sympy.Symbol('x')
            char_A = A.charpoly(x)
            char_B = B.charpoly(x)
            
            if char_A != char_B:
                neg_q = False
            else:
                n = A.rows
                A_dag = A.H
                B_dag = B.H
                
                char_AA = (A * A_dag).charpoly(x)
                char_BB = (B * B_dag).charpoly(x)
                
                if char_AA != char_BB:
                    not_conj = True
                else:
                    A_mats = [A, A_dag]
                    B_mats = [B, B_dag]
                    not_conj = False
                    
                    max_len = 7 if n <= 3 else (5 if n <= 5 else 4)
                    for length in range(1, max_len):
                        if not_conj:
                            break
                        for indices in product([0, 1], repeat=length):
                            W_A = sympy.eye(n)
                            W_B = sympy.eye(n)
                            for idx in indices:
                                W_A = W_A * A_mats[idx]
                                W_B = W_B * B_mats[idx]
                            
                            diff = sympy.expand(W_A.trace() - W_B.trace())
                            if diff != 0:
                                if sympy.simplify(diff) != 0:
                                    not_conj = True
                                    break
                
                neg_q = not_conj
                
    except Exception:
        neg_q = False

    return [h1, neg_q]