import itertools
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros

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

def conditions(witness) -> list[bool]:
    """
    witness should be a tuple: (add_table, mul_table, zero_idx, N_indices, n)
    where:
      - add_table: 2D list of integers representing the addition table of a finite ring R
      - mul_table: 2D list of integers representing the multiplication table of R
      - zero_idx: integer index of the zero element in the tables
      - N_indices: list of integers representing the elements of N
      - n: integer
    """
    try:
        add_table, mul_table, zero_idx, N_indices, n = witness
        
        m = len(add_table)
        if m < 1 or len(mul_table) != m:
            return [False, False, False]
        for row in add_table:
            if len(row) != m: return [False, False, False]
        for row in mul_table:
            if len(row) != m: return [False, False, False]
            
        # Check ring axioms to ensure R is a valid ring
        for i in range(m):
            if add_table[i][zero_idx] != i or add_table[zero_idx][i] != i:
                return [False, False, False]
        for i in range(m):
            has_inv = False
            for j in range(m):
                if add_table[i][j] == zero_idx and add_table[j][i] == zero_idx:
                    has_inv = True
                    break
            if not has_inv:
                return [False, False, False]
        for i in range(m):
            for j in range(m):
                if add_table[i][j] != add_table[j][i]:
                    return [False, False, False]
        for i in range(m):
            for j in range(m):
                for k in range(m):
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                        return [False, False, False]
        for i in range(m):
            for j in range(m):
                for k in range(m):
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                        return [False, False, False]
        for i in range(m):
            for j in range(m):
                for k in range(m):
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                        return [False, False, False]
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                        return [False, False, False]

        # H1: N is the nilradical (set of nilpotent elements) of R
        is_nilpotent = []
        for i in range(m):
            curr = i
            nilp = False
            for _ in range(m + 1):
                if curr == zero_idx:
                    nilp = True
                    break
                curr = mul_table[curr][i]
            is_nilpotent.append(nilp)
            
        actual_N = set(i for i in range(m) if is_nilpotent[i])
        h1 = (set(N_indices) == actual_N)
        
        # H2: n is a positive integer
        h2 = isinstance(n, int) and n > 0
        
        # neg_Q: The lower nilradical of M_n(R) is NOT equal to M_n(N)
        # By standard ring theory, the lower nilradical of M_n(R) is M_n(L(R)),
        # where L(R) is the lower nilradical of R.
        # Thus, M_n(L(R)) != M_n(N) if and only if L(R) != N.
        
        elements = list(range(m))
        
        def principal_ideal(x):
            ideal = {x}
            while True:
                new_ideal = set(ideal)
                for a in ideal:
                    for r in elements:
                        new_ideal.add(mul_table[r][a])
                        new_ideal.add(mul_table[a][r])
                    for b in ideal:
                        new_ideal.add(add_table[a][b])
                if len(new_ideal) == len(ideal):
                    break
                ideal = new_ideal
            return ideal

        def is_nilpotent_ideal(ideal):
            current_power = set(ideal)
            for _ in range(m + 1):
                if current_power == {zero_idx}:
                    return True
                next_prods = set()
                for a in current_power:
                    for b in ideal:
                        next_prods.add(mul_table[a][b])
                closure = set(next_prods)
                while True:
                    new_closure = set(closure)
                    for x in closure:
                        for y in closure:
                            new_closure.add(add_table[x][y])
                    if len(new_closure) == len(closure):
                        break
                    closure = new_closure
                current_power = closure
            return False

        lower_nilradical = set()
        for x in elements:
            if is_nilpotent_ideal(principal_ideal(x)):
                lower_nilradical.add(x)
                
        neg_q = (lower_nilradical != actual_N)
        
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: N is the nilradical of R",
    "H_2: n is a positive integer",
    "¬Q: The lower nilradical of M_n(R) is not equal to M_n(N)"
]

N_HYP = 2
NEG_Q_INDEX = 2