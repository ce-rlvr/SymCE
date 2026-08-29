import sympy
import math

class ZmodIdeal:
    def __init__(self, n, gens):
        self.n = n
        if isinstance(gens, (int, sympy.Integer)):
            gens = [int(gens)]
        elif not isinstance(gens, (list, tuple, set)):
            try:
                gens = list(gens)
            except Exception:
                gens = [gens]
        
        clean_gens = []
        for g in gens:
            try:
                clean_gens.append(int(g))
            except Exception:
                pass
                
        self.gens = [g % n if n > 0 else g for g in clean_gens]
        
        g = 0
        for x in self.gens:
            g = math.gcd(g, x)
        if n > 0:
            g = math.gcd(g, n)
            if g == n:
                g = 0
        self.gen = abs(g)

    def __eq__(self, other):
        if not isinstance(other, ZmodIdeal):
            return False
        return self.n == other.n and self.gen == other.gen

    def __mul__(self, other):
        if not isinstance(other, ZmodIdeal) or self.n != other.n:
            raise ValueError("Cannot multiply ideals from different rings")
        return ZmodIdeal(self.n, [self.gen * other.gen])

    def is_zero(self):
        return self.gen == 0

class ZmodRing:
    def __init__(self, n):
        self.n = n
        self.is_commutative = True

    def ideal(self, *gens):
        if len(gens) == 1:
            if isinstance(gens[0], ZmodIdeal):
                return gens[0]
            if isinstance(gens[0], (list, tuple, set)):
                return ZmodIdeal(self.n, gens[0])
        return ZmodIdeal(self.n, gens)

    def __eq__(self, other):
        return isinstance(other, ZmodRing) and self.n == other.n

    def __str__(self):
        return f"Z/{self.n}Z" if self.n > 0 else "Z"

# Top-level setup bindings
ZZ = ZmodRing(0)
Z2 = ZmodRing(2)
Z3 = ZmodRing(3)
Z4 = ZmodRing(4)
Z6 = ZmodRing(6)
Z8 = ZmodRing(8)
Z12 = ZmodRing(12)

def parse_witness(witness):
    if isinstance(witness, tuple) and len(witness) == 3:
        R, I, J = witness
        
        if isinstance(R, ZmodRing):
            return R, R.ideal(I), R.ideal(J)
            
        if R == sympy.S.Integers or str(R) == 'ZZ':
            R_obj = ZZ
            return R_obj, R_obj.ideal(I), R_obj.ideal(J)
            
        if isinstance(R, int):
            R_obj = ZmodRing(R)
            return R_obj, R_obj.ideal(I), R_obj.ideal(J)
            
    if isinstance(witness, tuple) and len(witness) == 2:
        I, J = witness
        R = ZZ
        return R, R.ideal(I), R.ideal(J)
        
    raise ValueError("Unknown witness format")

def conditions(witness) -> list[bool]:
    # Try SymPy ideals first
    try:
        if isinstance(witness, tuple) and len(witness) == 3:
            R, I, J = witness
            if hasattr(R, 'is_commutative') and hasattr(I, 'ring') and hasattr(J, 'ring'):
                h1 = R.is_commutative
                h2 = True
                h3 = True
                h4 = (I == I * J)
                is_z = I.is_zero
                if callable(is_z):
                    is_z = is_z()
                neg_q = not is_z
                return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]
    except Exception:
        pass

    # Try our custom parser
    try:
        R, I, J = parse_witness(witness)
    except Exception:
        return [False] * 5
        
    try:
        h1 = R.is_commutative
    except Exception:
        h1 = False
        
    try:
        h2 = isinstance(I, ZmodIdeal)
    except Exception:
        h2 = False
        
    try:
        h3 = isinstance(J, ZmodIdeal)
    except Exception:
        h3 = False
        
    try:
        h4 = (I == I * J)
    except Exception:
        h4 = False
        
    try:
        neg_q = not I.is_zero()
    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(h4), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is a finitely generated ideal of R",
    "H_3: J is an ideal of R",
    "H_4: I = IJ",
    "¬Q: I != {0}"
]

N_HYP = 4
NEG_Q_INDEX = 4