import itertools

class FiniteRing:
    def __init__(self, elements, add_table, mul_table, name=""):
        self.elements = list(elements)
        self.add_table = add_table
        self.mul_table = mul_table
        self.name = name
        self.zero = self.elements[0]
        self.one = None
        for e in self.elements:
            is_id = True
            for x in self.elements:
                if self.mul(e, x) != x or self.mul(x, e) != x:
                    is_id = False
                    break
            if is_id:
                self.one = e
                break

    def add(self, a, b):
        return self.add_table[a][b]

    def mul(self, a, b):
        return self.mul_table[a][b]

    def is_field(self):
        if self.one is None or self.one == self.zero:
            return False
        for a in self.elements:
            for b in self.elements:
                if self.mul(a, b) != self.mul(b, a):
                    return False
        for a in self.elements:
            if a == self.zero:
                continue
            has_inv = False
            for b in self.elements:
                if self.mul(a, b) == self.one:
                    has_inv = True
                    break
            if not has_inv:
                return False
        return True

    def is_subring(self, other):
        if not isinstance(other, FiniteRing):
            return False
        for e in self.elements:
            if e not in other.elements:
                return False
        for a in self.elements:
            for b in self.elements:
                if self.add(a, b) != other.add(a, b):
                    return False
                if self.mul(a, b) != other.mul(a, b):
                    return False
        if self.one != other.one:
            return False
        return True

    def power(self, a, n):
        if n == 0:
            return self.one
        res = self.one
        for _ in range(n):
            res = self.mul(res, a)
        return res

    def is_integral_over(self, R):
        if not R.is_subring(self):
            return False
        for s in self.elements:
            found_poly = False
            max_deg = len(self.elements)
            for d in range(1, max_deg + 1):
                for coeffs in itertools.product(R.elements, repeat=d):
                    val = self.power(s, d)
                    for i, c in enumerate(coeffs):
                        term = self.mul(c, self.power(s, i))
                        val = self.add(val, term)
                    if val == self.zero:
                        found_poly = True
                        break
                if found_poly:
                    break
            if not found_poly:
                return False
        return True

    def __str__(self):
        return self.name or "FiniteRing"

    def __repr__(self):
        return self.__str__()


# Define Z2 and Z2 x Z2
Z2_elements = [0, 1]
Z2_add = {0: {0: 0, 1: 1}, 1: {0: 1, 1: 0}}
Z2_mul = {0: {0: 0, 1: 0}, 1: {0: 0, 1: 1}}
Z2 = FiniteRing(Z2_elements, Z2_add, Z2_mul, "Z2")

Z2xZ2_elements = [(0,0), (0,1), (1,0), (1,1)]
Z2xZ2_add = {a: {b: (Z2_add[a[0]][b[0]], Z2_add[a[1]][b[1]]) for b in Z2xZ2_elements} for a in Z2xZ2_elements}
Z2xZ2_mul = {a: {b: (Z2_mul[a[0]][b[0]], Z2_mul[a[1]][b[1]]) for b in Z2xZ2_elements} for a in Z2xZ2_elements}
Z2_x_Z2 = FiniteRing(Z2xZ2_elements, Z2xZ2_add, Z2xZ2_mul, "Z2_x_Z2")

Z2_diag_elements = [(0,0), (1,1)]
Z2_diag_add = {a: {b: Z2xZ2_add[a][b] for b in Z2_diag_elements} for a in Z2_diag_elements}
Z2_diag_mul = {a: {b: Z2xZ2_mul[a][b] for b in Z2_diag_elements} for a in Z2_diag_elements}
Z2_diag = FiniteRing(Z2_diag_elements, Z2_diag_add, Z2_diag_mul, "Z2_diag")

# Define Z3 and Z3 x Z3
Z3_elements = [0, 1, 2]
Z3_add = {a: {b: (a+b)%3 for b in Z3_elements} for a in Z3_elements}
Z3_mul = {a: {b: (a*b)%3 for b in Z3_elements} for a in Z3_elements}
Z3 = FiniteRing(Z3_elements, Z3_add, Z3_mul, "Z3")

Z3xZ3_elements = [(a,b) for a in Z3_elements for b in Z3_elements]
Z3xZ3_add = {a: {b: (Z3_add[a[0]][b[0]], Z3_add[a[1]][b[1]]) for b in Z3xZ3_elements} for a in Z3xZ3_elements}
Z3xZ3_mul = {a: {b: (Z3_mul[a[0]][b[0]], Z3_mul[a[1]][b[1]]) for b in Z3xZ3_elements} for a in Z3xZ3_elements}
Z3_x_Z3 = FiniteRing(Z3xZ3_elements, Z3xZ3_add, Z3xZ3_mul, "Z3_x_Z3")

Z3_diag_elements = [(0,0), (1,1), (2,2)]
Z3_diag_add = {a: {b: Z3xZ3_add[a][b] for b in Z3_diag_elements} for a in Z3_diag_elements}
Z3_diag_mul = {a: {b: Z3xZ3_mul[a][b] for b in Z3_diag_elements} for a in Z3_diag_elements}
Z3_diag = FiniteRing(Z3_diag_elements, Z3_diag_add, Z3_diag_mul, "Z3_diag")

# Define Z4
Z4_elements = [0, 1, 2, 3]
Z4_add = {a: {b: (a+b)%4 for b in Z4_elements} for a in Z4_elements}
Z4_mul = {a: {b: (a*b)%4 for b in Z4_elements} for a in Z4_elements}
Z4 = FiniteRing(Z4_elements, Z4_add, Z4_mul, "Z4")


def conditions(witness):
    try:
        R, S = witness
    except Exception:
        return [False, False, False]
    
    try:
        h1 = R.is_subring(S)
    except Exception:
        h1 = False
        
    try:
        h2 = S.is_integral_over(R)
    except Exception:
        h2 = False
        
    try:
        r_field = R.is_field()
        s_field = S.is_field()
        neg_q = (r_field != s_field)
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a subring of S",
    "H_2: S is integral over R",
    "¬Q: Exactly one of R and S is a field"
]

N_HYP = 2
NEG_Q_INDEX = 2