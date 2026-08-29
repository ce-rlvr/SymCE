import sympy
from sympy import QQ, ZZ, Rational, Integer
from sympy.abc import x, y, z

CONDITION_LABELS = [
    "H_1: R is a commutative ring with identity",
    "H_2: I and J are ideals of R",
    "H_3: I \\cap J = \\{0\\}",
    "¬Q: There does not exist a unique idempotent e such that I = <1-e> and J = <e>"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    """
    Checks if the provided witness is a valid counterexample.
    The witness should be a tuple (R, I, J).
    - If R is an integer n >= 2, it represents the ring Z_n, and I, J should be lists of elements in the ideals.
    - If R is sympy.ZZ or sympy.QQ, I and J should be lists of generators for the ideals.
    """
    try:
        if len(witness) != 3:
            return [False, False, False, False]
        R, I, J = witness
        
        # Case 1: R is an integer >= 2 (representing Z_n)
        if isinstance(R, (int, Integer)):
            n = int(R)
            if n < 2:
                return [False, False, False, False]
                
            I_set = set(int(i) % n for i in I)
            J_set = set(int(j) % n for j in J)
            
            h1 = True
            
            def is_ideal(S):
                if not S: return False
                if 0 not in S: return False
                for a in S:
                    for b in S:
                        if (a + b) % n not in S: return False
                for a in S:
                    for r in range(n):
                        if (r * a) % n not in S: return False
                return True
                
            h2 = is_ideal(I_set) and is_ideal(J_set)
            h3 = (I_set.intersection(J_set) == {0})
            
            def gen_ideal(a):
                return set((r * a) % n for r in range(n))
                
            idempotents = [e for e in range(n) if (e * e) % n == e]
            matching_e_count = 0
            for e in idempotents:
                if gen_ideal((1 - e) % n) == I_set and gen_ideal(e) == J_set:
                    matching_e_count += 1
                    
            neg_q = (matching_e_count != 1)
            return [h1, h2, h3, neg_q]
            
        # Case 2: R is sympy.ZZ or sympy.QQ
        elif R in (ZZ, QQ):
            def is_zero(gens):
                if not gens: return True
                return all(g == 0 for g in gens)
                
            I_zero = is_zero(I)
            J_zero = is_zero(J)
            
            if R == QQ:
                gen_I = 0 if I_zero else 1
                gen_J = 0 if J_zero else 1
            else:
                def get_gen(gens):
                    if not gens: return 0
                    g = gens[0]
                    for a in gens[1:]:
                        g = sympy.gcd(g, a)
                    return abs(g)
                gen_I = get_gen(I)
                gen_J = get_gen(J)
                
            h1 = True
            h2 = True
            
            if R == QQ:
                h3 = I_zero or J_zero
            else:
                h3 = (gen_I == 0 or gen_J == 0)
                
            idempotents = [0, 1]
            matching_e_count = 0
            for e in idempotents:
                I_e = abs(1 - e)
                J_e = abs(e)
                if gen_I == I_e and gen_J == J_e:
                    matching_e_count += 1
                    
            neg_q = (matching_e_count != 1)
            return [h1, h2, h3, neg_q]
            
        else:
            return [False, False, False, False]
            
    except Exception:
        return [False, False, False, False]