import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
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
        L_separable = False
        deg_L = None
        n = None
        M_normal_closure = False
        deg_M = None

        if isinstance(witness, dict):
            L_separable = witness.get('L_separable', False)
            deg_L = witness.get('deg_L', None)
            n = witness.get('n', None)
            M_normal_closure = witness.get('M_normal_closure', False)
            deg_M = witness.get('deg_M', None)
            
        elif isinstance(witness, tuple):
            if len(witness) == 2 and isinstance(witness[0], PermutationGroup) and isinstance(witness[1], PermutationGroup):
                G, H = witness
                if H.is_subgroup(G):
                    L_separable = True
                    deg_L = G.order() // H.order()
                    n = deg_L
                    
                    core_is_trivial = True
                    for N in G.normal_subgroups():
                        if N.order() > 1 and N.is_subgroup(H):
                            core_is_trivial = False
                            break
                    M_normal_closure = core_is_trivial
                    deg_M = G.order()
            elif len(witness) == 2:
                n, deg_M = witness
                L_separable = True
                deg_L = n
                M_normal_closure = True
            elif len(witness) == 3:
                n, deg_L, deg_M = witness
                L_separable = True
                M_normal_closure = True
            elif len(witness) == 5:
                L_separable, deg_L, n, M_normal_closure, deg_M = witness
                
        else:
            L_separable = getattr(witness, 'L_separable', False)
            deg_L = getattr(witness, 'deg_L', None)
            n = getattr(witness, 'n', None)
            M_normal_closure = getattr(witness, 'M_normal_closure', False)
            deg_M = getattr(witness, 'deg_M', None)

        H1 = bool(L_separable)
        
        try:
            H2 = (int(deg_L) == int(n)) if (deg_L is not None and n is not None) else False
        except Exception:
            H2 = False
            
        H3 = bool(M_normal_closure)
        
        try:
            if n is not None and deg_M is not None and int(n) >= 0:
                n_int = int(n)
                if n_int > 1000:
                    neg_Q = False
                else:
                    fact_n = math.factorial(n_int)
                    d = int(deg_M)
                    if d == 0:
                        neg_Q = True
                    else:
                        neg_Q = (fact_n % d != 0)
            else:
                neg_Q = False
        except Exception:
            neg_Q = False

        return [H1, H2, H3, neg_Q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: L is separable over K",
    "H_2: The degree of L over K is equal to n",
    "H_3: M is the normal closure of L over K",
    "¬Q: The degree of M over K does not divide n!"
]

N_HYP = 3
NEG_Q_INDEX = 3