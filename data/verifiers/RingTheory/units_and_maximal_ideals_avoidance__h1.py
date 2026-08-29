import sympy
from sympy import Matrix, eye, zeros, gcd, fraction

class FiniteRing:
    def __init__(self, elements, add, mul):
        self.elements = list(elements)
        self.add = add
        self.mul = mul
        n = len(self.elements)
        self.add_table = [[0]*n for _ in range(n)]
        self.mul_table = [[0]*n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                self.add_table[i][j] = self.elements.index(self.add(self.elements[i], self.elements[j]))
                self.mul_table[i][j] = self.elements.index(self.mul(self.elements[i], self.elements[j]))
        
        self.zero = None
        for i in range(n):
            if all(self.add_table[j][i] == j and self.add_table[i][j] == j for j in range(n)):
                self.zero = self.elements[i]
                break
                
        self.one = None
        for i in range(n):
            if all(self.mul_table[j][i] == j and self.mul_table[i][j] == j for j in range(n)):
                self.one = self.elements[i]
                break

    def is_unit(self, u):
        if self.one is None:
            return False
        if u not in self.elements:
            return False
        u_idx = self.elements.index(u)
        one_idx = self.elements.index(self.one)
        for x_idx in range(len(self.elements)):
            if self.mul_table[u_idx][x_idx] == one_idx and self.mul_table[x_idx][u_idx] == one_idx:
                return True
        return False

    def ideals(self):
        n = len(self.elements)
        principal_ideals = []
        for i in range(n):
            mask = 1 << i
            while True:
                new_mask = mask
                for a in range(n):
                    if (mask & (1 << a)):
                        for b in range(n):
                            if (mask & (1 << b)):
                                c = self.add_table[a][b]
                                new_mask |= (1 << c)
                for a in range(n):
                    if (mask & (1 << a)):
                        for r in range(n):
                            c1 = self.mul_table[r][a]
                            c2 = self.mul_table[a][r]
                            new_mask |= (1 << c1)
                            new_mask |= (1 << c2)
                if new_mask == mask:
                    break
                mask = new_mask
            principal_ideals.append(mask)
        
        all_ideals = set(principal_ideals)
        while True:
            new_ideals = set(all_ideals)
            for m1 in all_ideals:
                for m2 in all_ideals:
                    sum_mask = 0
                    for a in range(n):
                        if (m1 & (1 << a)):
                            for b in range(n):
                                if (m2 & (1 << b)):
                                    c = self.add_table[a][b]
                                    sum_mask |= (1 << c)
                    new_ideals.add(sum_mask)
            if len(new_ideals) == len(all_ideals):
                break
            all_ideals = new_ideals
            
        res = []
        for mask in all_ideals:
            ideal = [self.elements[i] for i in range(n) if (mask & (1 << i))]
            res.append(ideal)
        return res

    def maximal_ideals(self):
        ids = self.ideals()
        proper_ids = [I for I in ids if len(I) < len(self.elements)]
        max_ids = []
        for I in proper_ids:
            is_max = True
            for J in proper_ids:
                if I != J and all(x in J for x in I):
                    is_max = False
                    break
            if is_max:
                max_ids.append(I)
        return max_ids

R_2Z8 = FiniteRing([0, 2, 4, 6], lambda x, y: (x + y) % 8, lambda x, y: (x * y) % 8)
R_2Z6 = FiniteRing([0, 2, 4], lambda x, y: (x + y) % 6, lambda x, y: (x * y) % 6)

def conditions(witness) -> list[bool]:
    try:
        u = witness
        if isinstance(witness, tuple):
            if len(witness) == 2:
                R, u = witness
                if hasattr(R, 'elements'):
                    h1 = u in R.elements
                    is_unit = R.is_unit(u)
                    max_ids = R.maximal_ideals()
                    in_max = any(u in M for M in max_ids)
                    neg_q = (is_unit == in_max)
                    return [h1, neg_q]
        
        if hasattr(u, 'is_Matrix') and u.is_Matrix:
            if not u.is_square or u.rows == 0:
                return [False, False]
            h1 = True
            is_unit = bool(u.det() != 0)
            
            has_frac = False
            for val in u:
                num, den = fraction(val)
                if den != 1:
                    has_frac = True
                    break
            
            is_zero = all(val == 0 for val in u)
            if has_frac:
                in_max = is_zero
            else:
                entries_gcd = u[0]
                for val in u:
                    entries_gcd = gcd(entries_gcd, val)
                in_max = is_zero or (entries_gcd != 1 and entries_gcd != -1 and entries_gcd != 0)
                
            neg_q = (is_unit == in_max)
            return [h1, neg_q]
            
        if isinstance(witness, int) or (hasattr(witness, 'is_Integer') and witness.is_Integer):
            u = int(witness)
            R = R_2Z8
            h1 = u in R.elements
            if h1:
                is_unit = R.is_unit(u)
                max_ids = R.maximal_ideals()
                in_max = any(u in M for M in max_ids)
                neg_q = (is_unit == in_max)
                return [h1, neg_q]
                
    except Exception:
        pass

    return [False, False]

CONDITION_LABELS = [
    "H_1: u is an element of R",
    "¬Q: u is a unit in R <=> u is in some maximal ideal of R (conclusion fails)"
]

N_HYP = 1
NEG_Q_INDEX = 1