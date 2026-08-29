import sympy
from sympy import ZZ, QQ
from sympy.polys.domains.domain import Domain

# Top-level setup
Z2 = 2
Z3 = 3
Z4 = 4
Z5 = 5
Z6 = 6

def normalize_cayley(ring):
    e, add, mul = ring
    if not e:
        raise ValueError
    if add[0][0] not in e:
        add = [[e[add[i][j]] for j in range(len(e))] for i in range(len(e))]
        mul = [[e[mul[i][j]] for j in range(len(e))] for i in range(len(e))]
    return e, add, mul

def is_zero_ring(ring):
    try:
        if isinstance(ring, int) or (hasattr(ring, 'is_Integer') and ring.is_Integer):
            return abs(int(ring)) == 1
    except Exception:
        pass
    if isinstance(ring, tuple) and len(ring) == 3:
        try:
            return len(ring[0]) == 1
        except Exception:
            pass
    if isinstance(ring, Domain):
        return False
    if hasattr(ring, 'is_zero_ring'):
        return ring.is_zero_ring()
    return False

def is_integral_domain(ring):
    try:
        if isinstance(ring, int) or (hasattr(ring, 'is_Integer') and ring.is_Integer):
            val = abs(int(ring))
            if val == 1:
                return False
            if val == 0:
                return True
            return sympy.isprime(val)
    except Exception:
        pass
    if isinstance(ring, Domain):
        return True
    if isinstance(ring, tuple) and len(ring) == 3:
        try:
            e, add, mul = normalize_cayley(ring)
            if len(e) == 1:
                return False
            for i in range(len(e)):
                for j in range(len(e)):
                    if mul[i][j] != mul[j][i]:
                        return False
            z_elem = None
            for i, x in enumerate(e):
                if all(add[i][j] == e[j] and add[j][i] == e[j] for j in range(len(e))):
                    z_elem = x
                    break
            if z_elem is None: return False
            id_elem = None
            for i, x in enumerate(e):
                if all(mul[i][j] == e[j] and mul[j][i] == e[j] for j in range(len(e))):
                    id_elem = x
                    break
            if id_elem is None or id_elem == z_elem: return False
            for i in range(len(e)):
                if e[i] == z_elem: continue
                for j in range(len(e)):
                    if e[j] == z_elem: continue
                    if mul[i][j] == z_elem:
                        return False
            return True
        except Exception:
            return False
    return False

def is_product_integral_domain(R, S):
    if isinstance(R, tuple) and len(R) == 3 and isinstance(S, tuple) and len(S) == 3:
        try:
            e_r, add_r, mul_r = normalize_cayley(R)
            e_s, add_s, mul_s = normalize_cayley(S)
            
            def find_zero(e, add):
                for i, x in enumerate(e):
                    if all(add[i][j] == e[j] and add[j][i] == e[j] for j in range(len(e))):
                        return x
                return None
                
            z_r = find_zero(e_r, add_r)
            z_s = find_zero(e_s, add_s)
            if z_r is None or z_s is None:
                return False
                
            for i in range(len(e_r)):
                for j in range(len(e_r)):
                    if mul_r[i][j] != mul_r[j][i]: return False
            for i in range(len(e_s)):
                for j in range(len(e_s)):
                    if mul_s[i][j] != mul_s[j][i]: return False
                    
            def find_identity(e, mul):
                for i, x in enumerate(e):
                    if all(mul[i][j] == e[j] and mul[j][i] == e[j] for j in range(len(e))):
                        return x
                return None
                
            id_r = find_identity(e_r, mul_r)
            id_s = find_identity(e_s, mul_s)
            if id_r is None or id_s is None:
                return False
            if id_r == z_r and id_s == z_s:
                return False
                
            for i1 in range(len(e_r)):
                for j1 in range(len(e_s)):
                    if e_r[i1] == z_r and e_s[j1] == z_s:
                        continue
                    for i2 in range(len(e_r)):
                        for j2 in range(len(e_s)):
                            if e_r[i2] == z_r and e_s[j2] == z_s:
                                continue
                            if mul_r[i1][i2] == z_r and mul_s[j1][j2] == z_s:
                                return False
            return True
        except Exception:
            return False
            
    if is_zero_ring(R):
        return is_integral_domain(S)
    if is_zero_ring(S):
        return is_integral_domain(R)
    return False

def conditions(witness) -> list[bool]:
    try:
        if hasattr(witness, 'R') and hasattr(witness, 'S'):
            R = witness.R
            S = witness.S
        elif isinstance(witness, tuple) and len(witness) == 2:
            R, S = witness
        else:
            return [False, False, False]
            
        h1 = not is_zero_ring(R)
        h2 = not is_zero_ring(S)
        neg_q = is_product_integral_domain(R, S)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R is not the zero ring",
    "H_2: S is not the zero ring",
    "¬Q: The direct product ring R \\times S is an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2