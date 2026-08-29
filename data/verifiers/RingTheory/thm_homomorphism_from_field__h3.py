import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy.ntheory import isprime

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AlternatingGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_order(obj):
    if hasattr(obj, 'order'):
        return int(obj.order() if callable(obj.order) else obj.order)
    elif hasattr(obj, 'mod'):
        return int(obj.mod() if callable(obj.mod) else obj.mod)
    elif isinstance(obj, (list, tuple, set)):
        return len(obj)
    else:
        return int(obj)

def conditions(witness):
    try:
        F_obj, S_obj, f_map = witness
        
        F_n = get_order(F_obj)
        S_n = get_order(S_obj)
            
        # H1: F is a field (we check if F_n is prime, which means Z_{F_n} is a field)
        h1 = isprime(F_n)
        
        # H2: S is a non-trivial ring where 1_S != 0_S
        h2 = S_n > 1
        
        # Evaluate f
        if callable(f_map):
            mapping = {i: int(f_map(i)) % S_n for i in range(F_n)}
        elif isinstance(f_map, dict):
            mapping = {int(k): int(v) % S_n for k, v in f_map.items()}
        else:
            mapping = {i: int(v) % S_n for i, v in enumerate(f_map)}
            
        if not all(i in mapping for i in range(F_n)):
            return [h1, h2, False]
            
        # Check if f is a ring homomorphism
        is_homo = True
        if mapping.get(1, 0) != 1 % S_n:
            is_homo = False
            
        for a in range(F_n):
            for b in range(F_n):
                if mapping[(a + b) % F_n] != (mapping[a] + mapping[b]) % S_n:
                    is_homo = False
                if mapping[(a * b) % F_n] != (mapping[a] * mapping[b]) % S_n:
                    is_homo = False
                    
        # Check if f is injective
        is_inj = len(set(mapping.values())) == F_n
        
        neg_q = not (is_homo and is_inj)
        
        return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: S is a non-trivial ring where 1_S != 0_S",
    "¬Q: f is not an injective ring homomorphism"
]

N_HYP = 2
NEG_Q_INDEX = 2