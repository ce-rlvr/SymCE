import sympy
from sympy.matrices import eye, zeros
from sympy import Symbol, Rational, Integer

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)
x = Symbol('x')
y = Symbol('y')

def conditions(witness):
    """
    Checks if the witness is a valid counterexample.
    The witness should represent a finite ring R and an endomorphism f.
    Expected format: a dictionary with keys 'n', 'add_table', 'mul_table', 'f_table'
    or a tuple (n, add_table, mul_table, f_table).
    - n: integer size of the ring (0 < n <= 50)
    - add_table: n x n list of lists for addition
    - mul_table: n x n list of lists for multiplication
    - f_table: list of length n representing the mapping f
    """
    h1 = False
    neg_q = False
    
    try:
        if isinstance(witness, dict):
            n = witness['n']
            add_table = witness['add_table']
            mul_table = witness['mul_table']
            f_table = witness['f_table']
        else:
            n, add_table, mul_table, f_table = witness
    except Exception:
        return [False, False]
        
    try:
        if isinstance(n, (int, sympy.Integer)) and 0 < n <= 50:
            if len(add_table) == n and all(len(row) == n for row in add_table) and \
               len(mul_table) == n and all(len(row) == n for row in mul_table) and \
               len(f_table) == n:
                
                closure = True
                for i in range(n):
                    if f_table[i] not in range(n): closure = False
                    for j in range(n):
                        if add_table[i][j] not in range(n): closure = False
                        if mul_table[i][j] not in range(n): closure = False
                
                if closure:
                    zeros_list = [z for z in range(n) if all(add_table[z][i] == i and add_table[i][z] == i for i in range(n))]
                    ones_list = [o for o in range(n) if all(mul_table[o][i] == i and mul_table[i][o] == i for i in range(n))]
                    
                    if zeros_list and ones_list:
                        zero = zeros_list[0]
                        one = ones_list[0]
                        
                        axioms_ok = True
                        for i in range(n):
                            if not axioms_ok: break
                            if not any(add_table[i][j] == zero for j in range(n)): 
                                axioms_ok = False
                                break
                            for j in range(n):
                                if not axioms_ok: break
                                if add_table[i][j] != add_table[j][i]: 
                                    axioms_ok = False
                                    break
                                for k in range(n):
                                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: 
                                        axioms_ok = False
                                        break
                                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: 
                                        axioms_ok = False
                                        break
                                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: 
                                        axioms_ok = False
                                        break
                                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: 
                                        axioms_ok = False
                                        break
                        
                        if axioms_ok:
                            homo_ok = True
                            if f_table[one] != one: 
                                homo_ok = False
                            else:
                                for i in range(n):
                                    if not homo_ok: break
                                    for j in range(n):
                                        if f_table[add_table[i][j]] != add_table[f_table[i]][f_table[j]]: 
                                            homo_ok = False
                                            break
                                        if f_table[mul_table[i][j]] != mul_table[f_table[i]][f_table[j]]: 
                                            homo_ok = False
                                            break
                            
                            if homo_ok:
                                h1 = True
    except Exception:
        h1 = False
        
    try:
        if isinstance(n, (int, sympy.Integer)) and 0 < n <= 50 and len(f_table) == n:
            if len(set(f_table)) < n:
                neg_q = True
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring and f is an endomorphism",
    "¬Q: f is not surjective"
]

N_HYP = 1
NEG_Q_INDEX = 1