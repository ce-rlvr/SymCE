import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, Permutation
from sympy.combinatorics.named_groups import DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
        if len(witness) == 4:
            n, S_n, A_n, x = witness
        elif len(witness) == 2:
            n, x = witness
            S_n = SymmetricGroup(n)
            A_n = AlternatingGroup(n)
        else:
            return [False, False, False, False]
    except Exception:
        return [False, False, False, False]

    # H_1: n is an integer greater than 1
    try:
        h1_ok = isinstance(n, int) and n > 1
    except Exception:
        h1_ok = False

    # H_2: S_n is the symmetric group on n letters
    try:
        h2_ok = (S_n == SymmetricGroup(n))
    except Exception:
        h2_ok = False

    # H_3: A_n is the alternating group on n letters
    try:
        h3_ok = (A_n == AlternatingGroup(n))
    except Exception:
        h3_ok = False

    # ¬Q: The conjugacy class of x in S_n splits into two distinct conjugacy classes of equal size in A_n 
    # if and only if the centralizer of x in S_n is a subgroup of A_n (must FAIL)
    try:
        if not isinstance(x, Permutation) or x not in S_n:
            neg_q_ok = False
        else:
            if n <= 7:
                # Literal evaluation for small n
                C_Sn_x = set()
                for g in S_n.generate():
                    if g * x == x * g:
                        C_Sn_x.add(g)
                rhs = all(g in A_n for g in C_Sn_x)

                K = set()
                for g in S_n.generate():
                    K.add(g * x * g**-1)
                
                if not all(y in A_n for y in K):
                    lhs = False
                else:
                    orbits = []
                    K_unvisited = set(K)
                    while K_unvisited:
                        start = K_unvisited.pop()
                        orbit = set()
                        for g in A_n.generate():
                            orbit.add(g * start * g**-1)
                        orbits.append(orbit)
                        K_unvisited -= orbit
                    
                    if len(orbits) == 2 and len(orbits[0]) == len(orbits[1]):
                        lhs = True
                    else:
                        lhs = False
            else:
                # Fast evaluation using cycle structure theorem for large n
                struct = x.cycle_structure.copy()
                moved = sum(k * v for k, v in struct.items())
                fixed = n - moved
                if fixed > 0:
                    struct[1] = fixed
                
                rhs = True
                for k, v in struct.items():
                    if k % 2 == 0 or v > 1:
                        rhs = False
                        break
                
                if not x.is_even:
                    lhs = False
                else:
                    lhs = rhs
            
            neg_q_ok = not (lhs == rhs)
    except Exception:
        neg_q_ok = False

    return [h1_ok, h2_ok, h3_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: n is an integer greater than 1",
    "H_2: S_n is the symmetric group on n letters",
    "H_3: A_n is the alternating group on n letters",
    "¬Q: The equivalence between the splitting of the conjugacy class and the centralizer being a subgroup fails"
]

N_HYP = 3
NEG_Q_INDEX = 3