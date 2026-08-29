import itertools
import sympy
from sympy import Matrix, eye, zeros

# Top-level setup: named object bindings
class CustomRing:
    def __init__(self, elements, add_op, mul_op):
        self.elements = elements
        self.add = add_op
        self.mul = mul_op

Z2 = CustomRing([0, 1], lambda x, y: (x + y) % 2, lambda x, y: (x * y) % 2)
Z2xZ2 = CustomRing(list(itertools.product([0, 1], repeat=2)), 
                   lambda x, y: tuple((a^b) for a,b in zip(x,y)),
                   lambda x, y: tuple((a&b) for a,b in zip(x,y)))
Z2xZ2xZ2 = CustomRing(list(itertools.product([0, 1], repeat=3)),
                      lambda x, y: tuple((a^b) for a,b in zip(x,y)),
                      lambda x, y: tuple((a&b) for a,b in zip(x,y)))

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def get_ring_ops(witness):
    if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul'):
        return witness.elements, witness.add, witness.mul
    
    if isinstance(witness, (set, tuple)):
        witness = list(witness)
        
    if isinstance(witness, list) and len(witness) > 0:
        unique_elements = []
        for e in witness:
            if e not in unique_elements:
                unique_elements.append(e)
        witness = unique_elements
        
        if isinstance(witness[0], tuple):
            def add(x, y): return tuple((a ^ b) for a, b in zip(x, y))
            def mul(x, y): return tuple((a & b) for a, b in zip(x, y))
            return witness, add, mul
        if hasattr(witness[0], 'is_Matrix'):
            def add(x, y): return (x + y).applyfunc(lambda a: a % 2)
            def mul(x, y): return (x * y).applyfunc(lambda a: a % 2)
            return witness, add, mul
        if isinstance(witness[0], int):
            n = len(witness)
            def add(x, y): return (x + y) % n
            def mul(x, y): return (x * y) % n
            return witness, add, mul
            
    if isinstance(witness, int) and witness > 0:
        elements = list(itertools.product([0, 1], repeat=witness))
        def add(x, y): return tuple((a ^ b) for a, b in zip(x, y))
        def mul(x, y): return tuple((a & b) for a, b in zip(x, y))
        return elements, add, mul
        
    raise ValueError("Unknown ring representation")

def conditions(witness) -> list[bool]:
    try:
        elements, add, mul = get_ring_ops(witness)
    except Exception:
        return [False, False]
        
    h1_ok = False
    try:
        n = len(elements)
        if 0 < n <= 64:
            zero = None
            for e in elements:
                is_zero = True
                for x in elements:
                    try:
                        if add(e, x) != x:
                            is_zero = False
                            break
                    except Exception:
                        is_zero = False
                        break
                if is_zero:
                    zero = e
                    break
            
            one = None
            for e in elements:
                is_one = True
                for x in elements:
                    try:
                        if mul(e, x) != x or mul(x, e) != x:
                            is_one = False
                            break
                    except Exception:
                        is_one = False
                        break
                if is_one:
                    one = e
                    break
            
            if zero is not None and one is not None:
                is_ring = True
                add_table = [[0]*n for _ in range(n)]
                mul_table = [[0]*n for _ in range(n)]
                
                def get_idx(val):
                    for idx, e in enumerate(elements):
                        if e == val: return idx
                    return -1
                
                for i in range(n):
                    for j in range(n):
                        try:
                            res_add = add(elements[i], elements[j])
                            res_mul = mul(elements[i], elements[j])
                        except Exception:
                            is_ring = False
                            break
                        idx_add = get_idx(res_add)
                        idx_mul = get_idx(res_mul)
                        if idx_add == -1 or idx_mul == -1:
                            is_ring = False
                            break
                        add_table[i][j] = idx_add
                        mul_table[i][j] = idx_mul
                    if not is_ring: break
                
                if is_ring:
                    zero_idx = get_idx(zero)
                    for i in range(n):
                        if not is_ring: break
                        if not any(add_table[i][j] == zero_idx for j in range(n)):
                            is_ring = False
                            break
                        if mul_table[i][i] != i:
                            is_ring = False
                            break
                        for j in range(n):
                            if not is_ring: break
                            ij_add = add_table[i][j]
                            ij_mul = mul_table[i][j]
                            if ij_add != add_table[j][i]: 
                                is_ring = False
                                break
                            for k in range(n):
                                if add_table[ij_add][k] != add_table[i][add_table[j][k]]:
                                    is_ring = False
                                    break
                                if mul_table[ij_mul][k] != mul_table[i][mul_table[j][k]]:
                                    is_ring = False
                                    break
                                if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                                    is_ring = False
                                    break
                                if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                                    is_ring = False
                                    break
                h1_ok = is_ring
    except Exception:
        h1_ok = False

    neg_q_ok = False
    try:
        if h1_ok:
            neg_q_ok = (len(elements) != 2)
        else:
            neg_q_ok = (len(elements) != 2)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: R is a Boolean ring",
    "¬Q: R is not isomorphic to Z/2Z"
]

N_HYP = 1
NEG_Q_INDEX = 1