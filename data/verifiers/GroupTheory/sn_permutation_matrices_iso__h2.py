import sympy
from sympy import Matrix, eye, zeros
import math
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

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
        if isinstance(witness, dict):
            n = witness.get('n')
            P_n = witness.get('P_n')
            if n is None or P_n is None:
                return [False, False]
        elif isinstance(witness, tuple) and len(witness) == 2 and isinstance(witness[0], (int, sympy.Integer)):
            n, P_n = witness
        elif isinstance(witness, (list, tuple, set)):
            P_n = witness
            first = Matrix(list(P_n)[0])
            n = first.shape[0]
        else:
            return [False, False]
    except Exception:
        return [False, False]

    # H1: n is a positive integer
    try:
        h1 = isinstance(n, (int, sympy.Integer)) and n > 0
        
        P_n_list = []
        is_valid_Pn = True
        if not isinstance(P_n, (list, tuple, set)):
            is_valid_Pn = False
        else:
            for M in P_n:
                try:
                    mat = Matrix(M)
                    if mat.shape != (n, n):
                        is_valid_Pn = False
                        break
                    P_n_list.append(mat)
                except Exception:
                    is_valid_Pn = False
                    break
        h1 = h1 and is_valid_Pn
    except Exception:
        h1 = False

    # Q: P_n forms a group under matrix multiplication that is isomorphic to S_n
    try:
        if not h1:
            neg_q = True
        else:
            I = eye(n)
            
            # Remove duplicates to find the true order of the set
            unique_P_n = []
            for M in P_n_list:
                if not any(M == U for U in unique_P_n):
                    unique_P_n.append(M)
            P_n_list = unique_P_n
            
            is_group = True
            has_I = False
            for M in P_n_list:
                if M == I:
                    has_I = True
                    break
            if not has_I:
                is_group = False
                
            # Check closure
            if is_group:
                for A in P_n_list:
                    for B in P_n_list:
                        AB = A * B
                        found = False
                        for M in P_n_list:
                            if M == AB:
                                found = True
                                break
                        if not found:
                            is_group = False
                            break
                    if not is_group:
                        break
                        
            # Check inverses
            if is_group:
                for A in P_n_list:
                    has_inv = False
                    for B in P_n_list:
                        if A * B == I and B * A == I:
                            has_inv = True
                            break
                    if not has_inv:
                        is_group = False
                        break
                        
            # Check isomorphism to S_n
            is_iso = False
            if is_group:
                if len(P_n_list) == math.factorial(n):
                    if n <= 2:
                        is_iso = True
                    else:
                        Sn = SymmetricGroup(n)
                        sn_orders = {}
                        for p in Sn.elements:
                            o = p.order()
                            sn_orders[o] = sn_orders.get(o, 0) + 1
                            
                        pn_orders = {}
                        for A in P_n_list:
                            o = 1
                            M = A
                            while M != I and o <= len(P_n_list):
                                M = M * A
                                o += 1
                            pn_orders[o] = pn_orders.get(o, 0) + 1
                            
                        if sn_orders == pn_orders:
                            is_iso = True
                            
            q = is_group and is_iso
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: n is a positive integer",
    "¬Q: P_n does not form a group under matrix multiplication isomorphic to S_n"
]

N_HYP = 1
NEG_Q_INDEX = 1