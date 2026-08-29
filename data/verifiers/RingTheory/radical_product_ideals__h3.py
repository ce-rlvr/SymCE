import math
import sympy
from sympy.ntheory import factorint

x, y, z = sympy.symbols('x y z')
ZZ = sympy.ZZ
QQ = sympy.QQ

class IdealZZ:
    def __init__(self, gen):
        self.gen = abs(int(gen))
    
    def __eq__(self, other):
        if isinstance(other, IdealZZ):
            return self.gen == other.gen
        if isinstance(other, (set, list, tuple)):
            if self.gen == 0 and set(other) == {0}:
                return True
            return False
        return False

    def __contains__(self, item):
        if self.gen == 0:
            return item == 0
        return item % self.gen == 0

    def intersection(self, other):
        if isinstance(other, IdealZZ):
            if self.gen == 0 or other.gen == 0:
                return IdealZZ(0)
            return IdealZZ(abs(self.gen * other.gen) // math.gcd(self.gen, other.gen))
        elif isinstance(other, (set, list, tuple)):
            return {val for val in other if val in self}
        else:
            raise TypeError("Unsupported type for intersection")

def rad_int(n):
    if n == 0:
        return 0
    factors = factorint(abs(n))
    res = 1
    for p in factors:
        res *= p
    return res

def radical_of_set(J):
    rad = set()
    for y in J:
        y = int(y)
        if y == 0:
            rad.add(0)
        elif y == 1:
            rad.add(1)
            rad.add(-1)
        elif y == -1:
            rad.add(-1)
        else:
            rad.add(y)
            max_n = int(math.log2(abs(y))) + 1
            for n in range(2, max_n + 1):
                if y < 0 and n % 2 == 0:
                    continue
                x = int(round(abs(y)**(1.0/n)))
                if x**n == abs(y):
                    if y > 0:
                        rad.add(x)
                        if n % 2 == 0:
                            rad.add(-x)
                    else:
                        rad.add(-x)
    return rad

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            R, I, J = witness
        else:
            return [False, False, False]
    except Exception:
        return [False, False, False]
        
    try:
        h1 = (R in ('ZZ', 'Z') or R == sympy.ZZ or str(R) == 'ZZ')
    except Exception:
        h1 = False
        
    try:
        if isinstance(I, (list, tuple, set)):
            I_val = 0
            for val in I:
                I_val = math.gcd(I_val, int(val))
        else:
            I_val = int(I)
        h2 = True
    except Exception:
        h2 = False
        
    try:
        I_ideal = IdealZZ(I_val)
        
        if isinstance(J, (int, sympy.Integer)):
            J_ideal = IdealZZ(int(J))
            IJ = IdealZZ(I_ideal.gen * J_ideal.gen)
            rad_J = IdealZZ(rad_int(J_ideal.gen))
        elif isinstance(J, (set, list, tuple)):
            J_set = set(int(val) for val in J)
            if not J_set:
                IJ = IdealZZ(0)
            else:
                gen = 0
                for j in J_set:
                    gen = math.gcd(gen, I_ideal.gen * j)
                IJ = IdealZZ(gen)
            rad_J = radical_of_set(J_set)
        else:
            neg_q = False
            return [h1, h2, neg_q]
            
        rad_IJ = IdealZZ(rad_int(IJ.gen))
        rad_I = IdealZZ(rad_int(I_ideal.gen))
        
        intersection = rad_I.intersection(rad_J)
        
        if isinstance(intersection, IdealZZ):
            q = (rad_IJ.gen == intersection.gen)
        else:
            if rad_IJ.gen == 0 and intersection == {0}:
                q = True
            else:
                q = False
                
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I is an ideal of R",
    "¬Q: The radical of the product ideal IJ is not equal to \\sqrt{I} \\cap \\sqrt{J}"
]

N_HYP = 2
NEG_Q_INDEX = 2