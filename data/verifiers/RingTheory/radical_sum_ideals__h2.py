import sympy
import math
from functools import reduce
from sympy.ntheory import factorint

# Top-level setup
Z = sympy.S.Integers
QQ = sympy.S.Rationals

def compute_radical_I(I_set):
    rad = set()
    for i in I_set:
        if i == 0:
            rad.add(0)
        elif i == 1:
            rad.add(1)
            rad.add(-1)
        elif i == -1:
            rad.add(-1)
            rad.add(1)
        else:
            rad.add(i)
            max_x = int(math.isqrt(abs(i)))
            for x in range(-max_x, max_x + 1):
                if x in [0, 1, -1]:
                    continue
                n = 2
                while abs(x)**n <= abs(i):
                    if x**n == i:
                        rad.add(x)
                    n += 1
    return rad

def compute_radical_J_gen(J_gen):
    if J_gen == 0:
        return 0
    factors = factorint(abs(J_gen))
    rad = 1
    for p in factors:
        rad *= p
    return rad

def in_radical_I_plus_J(x, I_set, J_gen):
    if J_gen == 0:
        if x in I_set: return True
        if x in [0, 1, -1]:
            return (x**1 in I_set) or (x**2 in I_set)
        max_val = max([abs(i) for i in I_set] + [0])
        n = 1
        while abs(x)**n <= max_val:
            if x**n in I_set:
                return True
            n += 1
        return False
    else:
        J_gen = abs(J_gen)
        val = x % J_gen
        I_mod = set(i % J_gen for i in I_set)
        for n in range(1, J_gen + 2):
            if val in I_mod:
                return True
            val = (val * x) % J_gen
        return False

def parse_witness(witness):
    if isinstance(witness, tuple):
        if len(witness) == 3:
            R_obj, I_obj, J_obj = witness
        elif len(witness) == 2:
            I_obj, J_obj = witness
        else:
            raise ValueError
    elif isinstance(witness, dict):
        I_obj = witness.get('I')
        J_obj = witness.get('J')
    else:
        raise ValueError
        
    if hasattr(J_obj, 'gens'):
        gens = J_obj.gens
        if len(gens) >= 1:
            J_gen = reduce(math.gcd, [int(x) for x in gens])
        else:
            J_gen = 0
    elif hasattr(J_obj, 'gen'):
        J_gen = J_obj.gen
    elif hasattr(J_obj, 'args') and len(J_obj.args) == 1 and hasattr(J_obj, 'is_Ideal'):
        J_gen = J_obj.args[0]
    elif isinstance(J_obj, (list, set, tuple)):
        if len(J_obj) == 0:
            J_gen = 0
        else:
            J_gen = reduce(math.gcd, [int(x) for x in J_obj])
    else:
        J_gen = J_obj
        
    J_gen = int(J_gen)
    
    if abs(J_gen) > 1000:
        raise ValueError("J_gen is too large")
    
    if isinstance(I_obj, int) or (hasattr(I_obj, 'is_Integer') and I_obj.is_Integer):
        raise ValueError("I must be a set or list, not a single integer")
        
    if hasattr(I_obj, 'is_finite') and I_obj.is_finite is False:
        raise ValueError("I must be a finite set")
        
    I_set = set()
    for count, i in enumerate(I_obj):
        if count > 1000:
            raise ValueError("I is too large")
        I_set.add(int(i))
        
    return I_set, J_gen

def conditions(witness) -> list[bool]:
    try:
        I_set, J_gen = parse_witness(witness)
    except Exception:
        return [False, False, False]
        
    # H1: R is a commutative ring (We evaluate in Z, which is commutative)
    h1 = True
    
    # H2: J is an ideal of R (J_gen is an integer, which generates an ideal in Z)
    h2 = True
    
    try:
        rad_I = compute_radical_I(I_set)
        rad_J_gen = compute_radical_J_gen(J_gen)
        
        if J_gen == 0:
            neg_q = False
        else:
            neg_q = False
            for x in range(abs(J_gen)):
                lhs = in_radical_I_plus_J(x, I_set, J_gen)
                rhs = in_radical_I_plus_J(x, rad_I, rad_J_gen)
                if lhs != rhs:
                    neg_q = True
                    break
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: J is an ideal of R",
    "¬Q: The radical of I + J is not equal to the radical of \\sqrt{I} + \\sqrt{J}"
]

N_HYP = 2
NEG_Q_INDEX = 2