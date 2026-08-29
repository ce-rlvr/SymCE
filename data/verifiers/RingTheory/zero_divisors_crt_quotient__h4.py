import math
import sympy
from sympy import Rational, Integer

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            m = int(witness['m'])
            I_list = [int(a) for a in witness['I_list']]
            x = int(witness['x'])
        else:
            m = int(witness[0])
            I_list = [int(a) for a in witness[1]]
            x = int(witness[2])
            
        if len(I_list) < 2:
            return [False, False, False, False]
            
        # H1: R is a commutative ring
        # Z/mZ is always a commutative ring.
        h1 = True
        
        # H2: I_1, ..., I_n are pairwise comaximal ideals of R
        h2 = True
        for i in range(len(I_list)):
            for j in range(i + 1, len(I_list)):
                if m == 0:
                    g = math.gcd(I_list[i], I_list[j])
                else:
                    g = math.gcd(math.gcd(I_list[i], I_list[j]), m)
                if g != 1:
                    h2 = False
                    break
            if not h2:
                break
                
        # H3: I = \bigcap_{k=1}^n I_k
        # We compute the intersection ideal generator mod_I
        h3 = True
        
        m_k = []
        for a in I_list:
            if m == 0:
                m_k.append(abs(a))
            else:
                m_k.append(math.gcd(a, m))
                
        mod_I = 1
        if m == 0 and any(mk == 0 for mk in m_k):
            mod_I = 0
        else:
            for mk in m_k:
                if mod_I == 0:
                    break
                mod_I = abs(mod_I * mk) // math.gcd(mod_I, mk)
                
        # Evaluate conclusion
        def is_zd_or_zero(val, mod):
            mod = abs(mod)
            if mod == 1:
                return True
            elif mod == 0:
                return val == 0
            else:
                return math.gcd(val % mod, mod) > 1
                
        lhs = is_zd_or_zero(x, mod_I)
        rhs = any(is_zd_or_zero(x, mk) for mk in m_k)
        
        neg_q = bool(lhs != rhs)
        
        return [h1, h2, h3, neg_q]
    except Exception:
        return [False, False, False, False]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: I_1, ..., I_n are pairwise comaximal ideals of R",
    "H_3: I = \\bigcap_{k=1}^n I_k",
    "¬Q: Image of x is zero/zero-divisor in R/I is NOT equivalent to being so in some R/I_k"
]

N_HYP = 3
NEG_Q_INDEX = 3