import sympy
from sympy import Matrix, Mod, simplify, Symbol, Rational, Integer
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup for linear algebra
I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        # Case 1: witness is a tuple (Matrix, mod) representing a matrix over Z/mZ
        if isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], int):
            try:
                M = Matrix(witness[0])
            except Exception:
                return [False, False]
            mod = witness[1]
            n = M.shape[0]
            if M.shape[1] != n:
                return [False, False]
            
            def is_zero_mod(mat):
                for val in mat:
                    try:
                        if (val % mod) != 0:
                            return False
                    except Exception:
                        return False
                return True
            
            is_nilp = False
            curr = M.applyfunc(lambda val: val % mod)
            for _ in range(max(n + 2, 20)):
                if is_zero_mod(curr):
                    is_nilp = True
                    break
                curr = (curr * M).applyfunc(lambda val: val % mod)
            
            if n == 0:
                M_n = sympy.eye(0)
            else:
                M_n = M.applyfunc(lambda val: val % mod)
                for _ in range(n - 1):
                    M_n = (M_n * M).applyfunc(lambda val: val % mod)
                    
            neg_q = not is_zero_mod(M_n)
            return [is_nilp, neg_q]
            
        # Case 2: witness is a tuple (Matrix, dict) representing a matrix over a quotient ring
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[1], dict):
            try:
                M = Matrix(witness[0])
            except Exception:
                return [False, False]
            subs_dict = witness[1]
            n = M.shape[0]
            if M.shape[1] != n:
                return [False, False]
            
            def is_zero_subs(mat):
                mat = mat.subs(subs_dict)
                mat = mat.expand().subs(subs_dict)
                for val in mat:
                    try:
                        if simplify(val) != 0:
                            return False
                    except Exception:
                        return False
                return True
            
            is_nilp = False
            curr = M.expand().subs(subs_dict)
            for _ in range(max(n + 2, 20)):
                if is_zero_subs(curr):
                    is_nilp = True
                    break
                curr = (curr * M).expand().subs(subs_dict)
            
            if n == 0:
                M_n = sympy.eye(0)
            else:
                M_n = M.expand().subs(subs_dict)
                for _ in range(n - 1):
                    M_n = (M_n * M).expand().subs(subs_dict)
                    
            neg_q = not is_zero_subs(M_n)
            return [is_nilp, neg_q]
            
        # Case 3: witness is a standard Matrix (or convertible to one)
        else:
            try:
                M = Matrix(witness)
            except Exception:
                return [False, False]
            
            n = M.shape[0]
            if M.shape[1] != n:
                return [False, False]
            
            def is_zero_mat(mat):
                for val in mat:
                    try:
                        if val == 0:
                            continue
                        if isinstance(val, Mod):
                            if val.args[0] % val.args[1] != 0:
                                return False
                            continue
                        if simplify(val) != 0:
                            return False
                    except Exception:
                        return False
                return True
            
            is_nilp = False
            curr = M
            for _ in range(max(n + 2, 20)):
                if is_zero_mat(curr):
                    is_nilp = True
                    break
                curr = curr * M
                
            M_n = M**n
            neg_q = not is_zero_mat(M_n)
            return [is_nilp, neg_q]
            
    except Exception:
        pass
    return [False, False]

CONDITION_LABELS = [
    "H_1: N is a nilpotent linear operator",
    "¬Q: N^n != 0, meaning the index of nilpotency exceeds the dimension n"
]

N_HYP = 1
NEG_Q_INDEX = 1