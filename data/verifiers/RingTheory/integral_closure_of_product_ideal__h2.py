import itertools
import math
import functools
import sympy
from sympy import Rational, Integer
from sympy.abc import x, y, z
from sympy.matrices import eye, zeros
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    zero = 0
    try:
        N, add, mul, I, J = witness
        
        h1 = True
        if not isinstance(N, int) or N < 1 or N > 50:
            h1 = False
        else:
            if not isinstance(add, (list, tuple)) or len(add) != N: h1 = False
            if not isinstance(mul, (list, tuple)) or len(mul) != N: h1 = False
            
            if h1:
                for i in range(N):
                    if not isinstance(add[i], (list, tuple)) or len(add[i]) != N: h1 = False
                    if not isinstance(mul[i], (list, tuple)) or len(mul[i]) != N: h1 = False
                    if not h1: break
                    for j in range(N):
                        if not isinstance(add[i][j], int) or not (0 <= add[i][j] < N): h1 = False
                        if not isinstance(mul[i][j], int) or not (0 <= mul[i][j] < N): h1 = False
            
            if h1:
                for i in range(N):
                    for j in range(N):
                        if add[i][j] != add[j][i]: h1 = False
                        if mul[i][j] != mul[j][i]: h1 = False
            
            if h1:
                for i in range(N):
                    for j in range(N):
                        for k in range(N):
                            if add[add[i][j]][k] != add[i][add[j][k]]: h1 = False
                            if mul[mul[i][j]][k] != mul[i][mul[j][k]]: h1 = False
                            if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]: h1 = False
            
            if h1:
                has_zero = False
                for z_elem in range(N):
                    if all(add[z_elem][i] == i for i in range(N)):
                        has_zero = True
                        zero = z_elem
                        break
                if not has_zero:
                    h1 = False
                else:
                    for i in range(N):
                        if not any(add[i][j] == zero for j in range(N)): h1 = False
                
                if h1:
                    has_one = False
                    for o_elem in range(N):
                        if all(mul[o_elem][i] == i for i in range(N)):
                            has_one = True
                            break
                    if not has_one:
                        h1 = False
    except Exception:
        h1 = False

    try:
        h2 = True
        if not h1:
            h2 = False
        else:
            if not isinstance(J, (list, set, tuple)):
                h2 = False
            else:
                J_set = set(J)
                if not J_set.issubset(range(N)):
                    h2 = False
                elif not J_set:
                    h2 = False
                else:
                    for a in J_set:
                        for b in J_set:
                            if add[a][b] not in J_set:
                                h2 = False
                    if h2:
                        for j in J_set:
                            for r in range(N):
                                if mul[r][j] not in J_set:
                                    h2 = False
    except Exception:
        h2 = False

    try:
        neg_q = False
        if h1 and h2:
            if not isinstance(I, (list, set, tuple)):
                neg_q = False
            else:
                I_set = set(I)
                J_set = set(J)
                if I_set.issubset(range(N)) and J_set.issubset(range(N)):
                    def add_closure_local(S):
                        closure_set = set(S)
                        if zero not in closure_set:
                            closure_set.add(zero)
                        closure = list(closure_set)
                        i = 0
                        while i < len(closure):
                            a = closure[i]
                            for b in closure:
                                c = add[a][b]
                                if c not in closure_set:
                                    closure_set.add(c)
                                    closure.append(c)
                            i += 1
                        return closure_set

                    def get_I_k_seq_local(S, max_k):
                        seq = [None]
                        if max_k >= 1:
                            seq.append(add_closure_local(S))
                        for k in range(2, max_k + 1):
                            prev = seq[-1]
                            prod = {mul[a][b] for a in S for b in prev}
                            seq.append(add_closure_local(prod))
                        return seq

                    def add_sets_local(A, B):
                        res = set()
                        for a in A:
                            for b in B:
                                res.add(add[a][b])
                        return res

                    def integral_closure_local(S):
                        max_n = N + 5
                        S_k = get_I_k_seq_local(S, max_n)
                        closure = set()
                        for x in range(N):
                            x_pow = [None, x]
                            for _ in range(2, max_n + 1):
                                x_pow.append(mul[x_pow[-1]][x])
                            
                            W = S_k[1]
                            is_integral = False
                            if x_pow[1] in W:
                                is_integral = True
                            else:
                                for n in range(2, max_n + 1):
                                    W_x = {mul[w][x] for w in W}
                                    W = add_sets_local(W_x, S_k[n])
                                    if x_pow[n] in W:
                                        is_integral = True
                                        break
                            if is_integral:
                                closure.add(x)
                        return closure

                    I_bar = integral_closure_local(I_set)
                    J_bar = integral_closure_local(J_set)
                    
                    prod_IJ = {mul[i][j] for i in I_set for j in J_set}
                    IJ = add_closure_local(prod_IJ)
                    IJ_bar = integral_closure_local(IJ)
                    
                    subset = True
                    for a in I_bar:
                        for b in J_bar:
                            if mul[a][b] not in IJ_bar:
                                subset = False
                                break
                        if not subset:
                            break
                    
                    neg_q = not subset
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: \\overline{I} \\cdot \\overline{J} \\not\\subseteq \\overline{IJ}"
]

N_HYP = 2
NEG_Q_INDEX = 2