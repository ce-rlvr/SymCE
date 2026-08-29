import sympy
from sympy.ntheory.modular import crt
import math

def parse_witness(witness):
    """
    Parses the witness into a list of a_i and a list of m_i.
    Supports:
    - dict: {m_i: a_i}
    - tuple of lists: ([a_1, ...], [m_1, ...])
    - list of sympy.Eq: [Eq(Mod(x, m_i), a_i), ...]
    - list of tuples: [(a_1, m_1), ...]
    """
    if isinstance(witness, dict):
        return list(witness.values()), list(witness.keys())
    if isinstance(witness, tuple) and len(witness) == 2:
        A, M = witness
        if isinstance(A, list) and isinstance(M, list) and len(A) == len(M):
            return A, M
    if isinstance(witness, list):
        if len(witness) > 0 and all(isinstance(item, sympy.Eq) for item in witness):
            A = []
            M = []
            for eq in witness:
                lhs, rhs = eq.lhs, eq.rhs
                if isinstance(lhs, sympy.Mod):
                    x, m = lhs.args
                    A.append(rhs)
                    M.append(m)
                else:
                    return None, None
            return A, M
        
        A = []
        M = []
        for item in witness:
            if isinstance(item, (tuple, list)) and len(item) == 2:
                A.append(item[0])
                M.append(item[1])
            else:
                return None, None
        return A, M
    return None, None

def is_int(val):
    if isinstance(val, int):
        return True
    if isinstance(val, float):
        return val.is_integer()
    if hasattr(val, 'is_integer') and val.is_integer is True:
        return True
    if isinstance(val, sympy.Rational) and val.q == 1:
        return True
    if isinstance(val, sympy.Integer):
        return True
    try:
        if int(val) == val:
            return True
    except Exception:
        pass
    return False

def conditions(witness) -> list[bool]:
    try:
        A, M = parse_witness(witness)
        if A is None or M is None:
            return [False, False]
            
        # H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers
        h1 = True
        for m in M:
            if not is_int(m) or m <= 0:
                h1 = False
                break
        if h1:
            for i in range(len(M)):
                for j in range(i + 1, len(M)):
                    if math.gcd(int(M[i]), int(M[j])) != 1:
                        h1 = False
                        break
                if not h1:
                    break
                    
        # Q: The system of linear congruences has a unique solution modulo m_1 m_2 ... m_k
        q = True
        for a in A:
            if not is_int(a):
                q = False
                break
                
        if q:
            M_total = 1
            for m in M:
                if not is_int(m) or m <= 0:
                    q = False
                    break
                M_total *= int(m)
                
        if q:
            A_ints = [int(a) for a in A]
            M_ints = [int(m) for m in M]
            res = crt(M_ints, A_ints)
            if res is None:
                q = False
            else:
                sol, lcm_M = res
                if M_total != lcm_M:
                    q = False
                    
        neg_q = not q
        return [h1, neg_q]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: m_1, m_2, ..., m_k are pairwise coprime positive integers",
    "¬Q: The system of linear congruences does not have a unique solution modulo m_1 m_2 ... m_k"
]

N_HYP = 1
NEG_Q_INDEX = 1