import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        if not isinstance(witness, (int, sympy.Integer)):
            return [False, False]
        n = int(witness)
        h1 = (n >= 1)
    except Exception:
        h1 = False

    try:
        if not h1:
            neg_q = False
        else:
            a_perm = []
            for i in range(2*n):
                a_perm.append((i + 1) % (2*n))
            for i in range(2*n):
                a_perm.append(((i + 1) % (2*n)) + 2*n)
                
            x_perm = [0]*(4*n)
            for i in range(2*n):
                x_perm[i] = (-i % (2*n)) + 2*n
                x_perm[i + 2*n] = (n - i) % (2*n)
                
            G = PermutationGroup(Permutation(a_perm), Permutation(x_perm))
            
            try:
                c_order = G.center().order()
            except AttributeError:
                gens = G.generators
                c_order = 0
                for g in G.generate():
                    if all(g*gen == gen*g for gen in gens):
                        c_order += 1
                        
            neg_q = (c_order != 2)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is an integer >= 1 (defining Dic_n)",
    "¬Q: The center of Dic_n does not have order 2"
]

N_HYP = 1
NEG_Q_INDEX = 1