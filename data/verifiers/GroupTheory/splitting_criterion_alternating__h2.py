import sympy
from sympy.combinatorics import AlternatingGroup, SymmetricGroup, Permutation
from sympy.combinatorics.named_groups import DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.abc import x, y, z
import math
import itertools
import functools

# Top-level setup
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
    try:
        n, A_n, x_val = witness
    except Exception:
        return [False, False, False, False]

    # H1: n is an integer greater than 1
    try:
        h1_ok = isinstance(n, int) and n > 1
    except Exception:
        h1_ok = False

    # H2: A_n is the alternating group on n letters
    try:
        h2_ok = (A_n == AlternatingGroup(n))
    except Exception:
        h2_ok = False

    # H3: x is an element of A_n
    try:
        h3_ok = x_val in A_n
    except Exception:
        h3_ok = False

    # neg_Q: The conclusion FAILS at the witness
    try:
        S_n = SymmetricGroup(n)
        
        if n <= 6:
            S_n_elements = list(S_n.generate())
            A_n_elements = list(A_n.generate())
            
            # Conjugacy class of x in S_n
            K = set()
            for g in S_n_elements:
                K.add(g * x_val * ~g)
                
            # Partition K into A_n conjugacy classes
            unvisited = set(K)
            A_n_classes = []
            while unvisited:
                y_elem = unvisited.pop()
                y_class = set()
                for h in A_n_elements:
                    y_class.add(h * y_elem * ~h)
                A_n_classes.append(y_class)
                unvisited -= y_class
                
            splits = (len(A_n_classes) == 2) and (len(A_n_classes[0]) == len(A_n_classes[1]))
            
            # Centralizer of x in S_n is a subgroup of A_n
            centralizer_in_An = True
            for g in S_n_elements:
                if g * x_val == x_val * g:
                    if g not in A_n_elements:
                        centralizer_in_An = False
                        break
        else:
            # For larger n, use cycle type logic to ensure fast execution
            cycles = x_val.cyclic_form
            lengths = [len(c) for c in cycles]
            fixed = n - sum(lengths)
            lengths.extend([1] * fixed)
            
            all_odd = all(l % 2 == 1 for l in lengths)
            all_distinct = len(lengths) == len(set(lengths))
            
            splits = all_odd and all_distinct
            centralizer_in_An = all_odd and all_distinct
            
        conclusion = (splits == centralizer_in_An)
        neg_q_ok = not conclusion
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: A_n is the alternating group on n letters",
    "H_3: x is an element of A_n",
    "¬Q: The conjugacy class of x in S_n splits into two distinct conjugacy classes of equal size in A_n does NOT hold if and only if the centralizer of x in S_n is a subgroup of A_n"
]

N_HYP = 3
NEG_Q_INDEX = 3