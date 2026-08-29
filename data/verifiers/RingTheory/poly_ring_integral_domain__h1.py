import sympy
from sympy import isprime, QQ, ZZ
from sympy.abc import x, y, z
import re

def is_integral_domain(witness):
    if isinstance(witness, int):
        if witness == 0: return True
        if witness == 1 or witness == -1: return False
        return isprime(abs(witness))
        
    if isinstance(witness, str):
        if witness in ["Z", "Q", "R", "C", "ZZ", "QQ", "RR", "CC"]: 
            return True
        m = re.match(r"Z/(\d+)Z", witness)
        if m:
            n = int(m.group(1))
            if n == 0: return True
            if n == 1 or n == -1: return False
            return isprime(n)
            
    try:
        if witness in [sympy.S.Integers, sympy.S.Reals, sympy.S.Rationals, sympy.S.Complexes]:
            return True
    except Exception:
        pass

    try:
        from sympy.polys.domains import Domain
        if isinstance(witness, Domain):
            if hasattr(witness, 'is_IntegralDomain'):
                return witness.is_IntegralDomain
            return True
    except Exception:
        pass
        
    if isinstance(witness, tuple) and len(witness) == 3:
        elements, add_table, mul_table = witness
        n = len(elements)
        if n <= 1: return False
        
        zero = None
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)):
                zero = i
                break
        if zero is None: return False
        
        for i in range(n):
            for j in range(n):
                if mul_table[i][j] != mul_table[j][i]:
                    return False
                    
        one = None
        for i in range(n):
            if all(mul_table[i][j] == j for j in range(n)):
                one = i
                break
        if one is None or one == zero: return False
        
        for i in range(n):
            if i == zero: continue
            for j in range(n):
                if j == zero: continue
                if mul_table[i][j] == zero:
                    return False
        return True
        
    return False

def conditions(witness) -> list[bool]:
    try:
        h1 = bool(is_integral_domain(witness))
    except Exception:
        h1 = False
        
    try:
        q = bool(is_integral_domain(witness))
        neg_q = not q
    except Exception:
        neg_q = False
        
    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: R is an integral domain",
    "¬Q: The polynomial ring over R is not an integral domain"
]

N_HYP = 1
NEG_Q_INDEX = 1