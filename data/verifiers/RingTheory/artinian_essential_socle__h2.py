import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy import eye, zeros, Rational, Integer
import itertools

# Top-level setup for named objects
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

CONDITION_LABELS = [
    "H_1: R is a right Artinian ring",
    "¬Q: Soc(R_R) is not an essential right ideal of R"
]

N_HYP = 1
NEG_Q_INDEX = 1

def get_elements(witness):
    if hasattr(witness, 'elements'):
        return list(witness.elements)
    if hasattr(witness, 'elements_list'):
        return list(witness.elements_list())
    if isinstance(witness, list):
        return witness
    if hasattr(witness, '__iter__'):
        return list(witness)
    return None

def conditions(witness):
    try:
        raw_elements = get_elements(witness)
        if raw_elements is None:
            return [False, False]
            
        N = len(raw_elements)
        if N == 0:
            return [False, False]
            
        if hasattr(witness, 'add'):
            raw_add = witness.add
        else:
            raw_add = lambda x, y: x + y
            
        if hasattr(witness, 'mul'):
            raw_mul = witness.mul
        else:
            raw_mul = lambda x, y: x * y
            
        # Find zero element
        if hasattr(witness, 'zero'):
            raw_zero = witness.zero
        else:
            raw_zero = None
            for e in raw_elements:
                is_z = True
                for x in raw_elements:
                    if raw_add(e, x) != x:
                        is_z = False
                        break
                if is_z:
                    raw_zero = e
                    break
            if raw_zero is None:
                return [False, False]
                
        def find_index(obj):
            for i, e in enumerate(raw_elements):
                if obj == e:
                    return i
            return -1
            
        zero_idx = find_index(raw_zero)
        if zero_idx == -1:
            return [False, False]
            
        # Precompute Cayley tables to work with integer indices (avoids hashability issues)
        add_table = [[-1] * N for _ in range(N)]
        mul_table = [[-1] * N for _ in range(N)]
        
        for i in range(N):
            for j in range(N):
                res_add = raw_add(raw_elements[i], raw_elements[j])
                idx_add = find_index(res_add)
                if idx_add == -1: return [False, False]
                add_table[i][j] = idx_add
                
                res_mul = raw_mul(raw_elements[i], raw_elements[j])
                idx_mul = find_index(res_mul)
                if idx_mul == -1: return [False, False]
                mul_table[i][j] = idx_mul
                
        # Check ring axioms
        for i in range(N):
            if add_table[i][zero_idx] != i or add_table[zero_idx][i] != i:
                return [False, False]
                
        for i in range(N):
            for j in range(N):
                if add_table[i][j] != add_table[j][i]:
                    return [False, False]
                    
        subset = list(range(N)) if N <= 30 else list(range(15))
        for i in subset:
            for j in subset:
                for k in subset:
                    if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]: return [False, False]
                    if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]: return [False, False]
                    if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]: return [False, False]
                    if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]: return [False, False]
                    
        inverses = [-1] * N
        for i in range(N):
            for j in range(N):
                if add_table[i][j] == zero_idx:
                    inverses[i] = j
                    break
            if inverses[i] == -1:
                return [False, False]
                
        # H1: R is a right Artinian ring (any finite ring is Artinian)
        h1 = True
        
        # Compute all principal right ideals
        principal_ideals = []
        for x in range(N):
            ideal = {x, zero_idx}
            queue = [x, zero_idx]
            queue_idx = 0
            while queue_idx < len(queue):
                curr = queue[queue_idx]
                queue_idx += 1
                new_elements = set()
                
                for y in ideal:
                    s = add_table[curr][y]
                    if s not in ideal and s not in new_elements:
                        new_elements.add(s)
                        
                inv = inverses[curr]
                if inv not in ideal and inv not in new_elements:
                    new_elements.add(inv)
                    
                for r in range(N):
                    p = mul_table[curr][r]
                    if p not in ideal and p not in new_elements:
                        new_elements.add(p)
                        
                for n in new_elements:
                    ideal.add(n)
                    queue.append(n)
            principal_ideals.append(frozenset(ideal))
            
        # Compute all right ideals by taking sums
        ideals = set(principal_ideals)
        queue = list(principal_ideals)
        queue_idx = 0
        while queue_idx < len(queue):
            curr = queue[queue_idx]
            queue_idx += 1
            for pi in principal_ideals:
                sum_ideal = set()
                for a in curr:
                    for b in pi:
                        sum_ideal.add(add_table[a][b])
                sum_ideal = frozenset(sum_ideal)
                if sum_ideal not in ideals:
                    ideals.add(sum_ideal)
                    queue.append(sum_ideal)
                    
        # Find minimal non-zero right ideals
        non_zero_ideals = [I for I in ideals if I != frozenset([zero_idx])]
        minimal_ideals = []
        for M in non_zero_ideals:
            is_minimal = True
            for N_ideal in non_zero_ideals:
                if N_ideal != M and N_ideal.issubset(M):
                    is_minimal = False
                    break
            if is_minimal:
                minimal_ideals.append(M)
                
        # Compute Soc(R_R)
        socle = set([zero_idx])
        for M in minimal_ideals:
            new_socle = set()
            for a in socle:
                for b in M:
                    new_socle.add(add_table[a][b])
            socle = new_socle
        socle = frozenset(socle)
        
        # Check if Soc(R_R) is an essential right ideal
        essential = True
        for I in non_zero_ideals:
            intersection = socle.intersection(I)
            if len(intersection) <= 1:  # Only contains zero_idx
                essential = False
                break
                
        neg_q = not essential
        
        return [h1, neg_q]
        
    except Exception:
        return [False, False]