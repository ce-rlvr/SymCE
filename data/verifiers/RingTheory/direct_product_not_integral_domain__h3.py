import sympy
from sympy import abc

# Top-level setup
# Rings can be represented by sympy domains (ZZ, QQ), integers n (for Z/nZ, where 0 means Z),
# or {0} for the zero ring.
ZZ = sympy.ZZ
QQ = sympy.QQ
ZeroRing = {0}

def parse_ring(r):
    """
    Parses a ring representation and returns a tuple of booleans:
    (is_commutative_ring_with_identity, is_zero_ring, is_integral_domain)
    """
    if r is sympy.ZZ or r is sympy.QQ:
        return True, False, True
    if str(r) in ['ZZ', 'QQ', 'Z', 'Q']:
        return True, False, True
        
    if isinstance(r, (set, list, tuple)):
        if len(r) == 1:
            elem = list(r)[0]
            if hasattr(elem, 'is_Integer') and elem.is_Integer:
                elem = int(elem)
            if elem == 0 or str(elem) == '0':
                return True, True, False
                
    if hasattr(r, 'is_Integer') and r.is_Integer:
        r = int(r)
    if isinstance(r, int):
        if r == 0:
            return True, False, True  # Z/0Z is isomorphic to Z
        elif r == 1:
            return True, True, False  # Z/1Z is the zero ring
        elif r > 1:
            return True, False, sympy.isprime(r)
            
    if isinstance(r, str):
        r = r.strip().lower()
        if r in ['z', 'zz', 'q', 'qq', 'r', 'c']:
            return True, False, True
        if r in ['0', 'zero', 'zeroring', '{0}', '[0]']:
            return True, True, False
            
    return False, False, False

def conditions(witness) -> list[bool]:
    try:
        if not (isinstance(witness, tuple) and len(witness) == 2):
            return [False, False, False]
        
        r, s = witness
        r_comm, r_zero, r_idom = parse_ring(r)
        s_comm, s_zero, s_idom = parse_ring(s)
        
        # Both must be valid commutative rings with identity
        if not (r_comm and s_comm):
            return [False, False, False]
            
        # H_1: R and S are commutative rings with identity
        h1 = True
        
        # H_2: R is not the zero ring
        h2 = not r_zero
        
        # ¬Q: The direct product ring R \times S IS an integral domain.
        # R \times S is an integral domain if and only if one of the rings is an integral domain
        # and the other is the zero ring. (The zero ring itself is not an integral domain).
        if r_zero and s_zero:
            neg_q = False
        elif not r_zero and not s_zero:
            neg_q = False
        elif r_zero:
            neg_q = s_idom
        elif s_zero:
            neg_q = r_idom
        else:
            neg_q = False
            
        return [h1, h2, neg_q]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: R and S are commutative rings with identity",
    "H_2: R is not the zero ring",
    r"¬Q: The direct product ring R \times S is an integral domain"
]

N_HYP = 2
NEG_Q_INDEX = 2