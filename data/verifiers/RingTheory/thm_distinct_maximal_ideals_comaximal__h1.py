import sympy
from sympy import ZZ
import itertools

class FiniteRing:
    def __init__(self, n, add_table, mul_table):
        self.n = n
        self.add_table = add_table
        self.mul_table = mul_table
        self.elements = list(range(n))
        self._is_ring = None
        
    def is_ring(self):
        if self._is_ring is not None:
            return self._is_ring
            
        n = self.n
        add = self.add_table
        mul = self.mul_table
        
        if len(add) != n or any(len(row) != n for row in add):
            self._is_ring = False
            return False
        if len(mul) != n or any(len(row) != n for row in mul):
            self._is_ring = False
            return False
            
        # Add commutative
        for i in range(n):
            for j in range(n):
                if add[i][j] != add[j][i]:
                    self._is_ring = False
                    return False
                    
        # Add associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if add[add[i][j]][k] != add[i][add[j][k]]:
                        self._is_ring = False
                        return False
                        
        # Zero element
        zeros = [i for i in range(n) if all(add[i][j] == j for j in range(n))]
        if len(zeros) != 1:
            self._is_ring = False
            return False
        zero = zeros[0]
        
        # Add inverse
        for i in range(n):
            if not any(add[i][j] == zero for j in range(n)):
                self._is_ring = False
                return False
                
        # Mul associative
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul[mul[i][j]][k] != mul[i][mul[j][k]]:
                        self._is_ring = False
                        return False
                        
        # Distributive
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    if mul[i][add[j][k]] != add[mul[i][j]][mul[i][k]]:
                        self._is_ring = False
                        return False
                    if mul[add[i][j]][k] != add[mul[i][k]][mul[j][k]]:
                        self._is_ring = False
                        return False
                        
        self._is_ring = True
        return True

    def is_ideal(self, M):
        if not self.is_ring(): return False
        if not M: return False
        M_set = set(M)
        for x in M_set:
            if x < 0 or x >= self.n:
                return False
                
        for a in M_set:
            for b in M_set:
                if self.add_table[a][b] not in M_set:
                    return False
                    
        zeros = [i for i in range(self.n) if all(self.add_table[i][j] == j for j in range(self.n))]
        if not zeros: return False
        if zeros[0] not in M_set: return False
        
        for m in M_set:
            for r in range(self.n):
                if self.mul_table[r][m] not in M_set: return False
                if self.mul_table[m][r] not in M_set: return False
        return True

    def is_maximal_ideal(self, M):
        if not self.is_ideal(M): return False
        if set(M) == set(self.elements): return False
        
        M_set = set(M)
        for x_elem in range(self.n):
            if x_elem in M_set: continue
            gen = set(M_set)
            gen.add(x_elem)
            changed = True
            while changed:
                changed = False
                new_elements = set()
                for a in gen:
                    for b in gen:
                        s = self.add_table[a][b]
                        if s not in gen and s not in new_elements:
                            new_elements.add(s)
                for a in gen:
                    for r in range(self.n):
                        p1 = self.mul_table[r][a]
                        p2 = self.mul_table[a][r]
                        if p1 not in gen and p1 not in new_elements:
                            new_elements.add(p1)
                        if p2 not in gen and p2 not in new_elements:
                            new_elements.add(p2)
                if new_elements:
                    gen.update(new_elements)
                    changed = True
            if gen != set(self.elements):
                return False
        return True

    def sum_ideals(self, M1, M2):
        S = set()
        for a in M1:
            for b in M2:
                S.add(self.add_table[a][b])
        return list(S)

# Standard finite rings
Z2 = FiniteRing(2, [[(i+j)%2 for j in range(2)] for i in range(2)], [[(i*j)%2 for j in range(2)] for i in range(2)])
Z3 = FiniteRing(3, [[(i+j)%3 for j in range(3)] for i in range(3)], [[(i*j)%3 for j in range(3)] for i in range(3)])
Z4 = FiniteRing(4, [[(i+j)%4 for j in range(4)] for i in range(4)], [[(i*j)%4 for j in range(4)] for i in range(4)])
Z6 = FiniteRing(6, [[(i+j)%6 for j in range(6)] for i in range(6)], [[(i*j)%6 for j in range(6)] for i in range(6)])

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            n, add_table, mul_table, M1, M2 = witness
            R = FiniteRing(n, add_table, mul_table)
            M1 = list(M1)
            M2 = list(M2)
        elif isinstance(witness, tuple) and len(witness) == 3:
            R, M1, M2 = witness
            if isinstance(R, FiniteRing):
                M1 = list(M1)
                M2 = list(M2)
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    # H_1: M_1 and M_2 are maximal ideals of R
    try:
        if isinstance(R, FiniteRing):
            h1 = R.is_maximal_ideal(M1) and R.is_maximal_ideal(M2)
        elif R == sympy.ZZ:
            gen1 = M1.gens[0]
            gen2 = M2.gens[0]
            h1 = sympy.isprime(gen1) and sympy.isprime(gen2)
        else:
            h1 = False
    except Exception:
        h1 = False

    # H_2: M_1 and M_2 are distinct
    try:
        if isinstance(R, FiniteRing):
            h2 = set(M1) != set(M2)
        elif R == sympy.ZZ:
            h2 = abs(M1.gens[0]) != abs(M2.gens[0])
        else:
            h2 = False
    except Exception:
        h2 = False

    # neg_Q: The sum of the ideals M_1 and M_2 is not equal to the entire ring R
    try:
        if isinstance(R, FiniteRing):
            sum_M = R.sum_ideals(M1, M2)
            neg_q = set(sum_M) != set(R.elements)
        elif R == sympy.ZZ:
            gen1 = M1.gens[0]
            gen2 = M2.gens[0]
            sum_ideal = sympy.gcd(gen1, gen2)
            neg_q = abs(sum_ideal) != 1
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: M_1 and M_2 are maximal ideals of R",
    "H_2: M_1 and M_2 are distinct",
    "¬Q: The sum of the ideals M_1 and M_2 is not equal to the entire ring R"
]

N_HYP = 2
NEG_Q_INDEX = 2