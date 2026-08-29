import itertools
from sympy import Rational, Integer
from sympy.abc import x, y, z

class FiniteRing:
    def __init__(self, elements, add_table, mul_table):
        self.elements = elements
        self.add_table = add_table
        self.mul_table = mul_table

class Ideal:
    def __init__(self, ring, elements):
        self.ring = ring
        self.elements = elements

def create_Zn(n):
    elements = list(range(n))
    add_table = [[(i+j)%n for j in range(n)] for i in range(n)]
    mul_table = [[(i*j)%n for j in range(n)] for i in range(n)]
    return FiniteRing(elements, add_table, mul_table)

# Standard rings
Z2 = create_Zn(2)
Z3 = create_Zn(3)
Z4 = create_Zn(4)
Z6 = create_Zn(6)

# A ring with zero multiplication (counterexample to the conjecture)
Z2_zero_mul = FiniteRing(
    elements=[0, 1],
    add_table=[[0, 1], [1, 0]],
    mul_table=[[0, 0], [0, 0]]
)

def get_zero(elements, add_table):
    n = len(elements)
    for i in range(n):
        is_zero = True
        for j in range(n):
            if add_table[i][j] != elements[j] or add_table[j][i] != elements[j]:
                is_zero = False
                break
        if is_zero:
            return elements[i]
    return None

def is_ring(elements, add_table, mul_table):
    try:
        n = len(elements)
        if len(set(elements)) != n: return False
        
        # Check add commutativity
        for i in range(n):
            for j in range(n):
                if add_table[i][j] != add_table[j][i]: return False
                
        # Check add associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    ij = elements.index(add_table[i][j])
                    jk = elements.index(add_table[j][k])
                    if add_table[ij][k] != add_table[i][jk]: return False
                    
        # Check zero
        zero = get_zero(elements, add_table)
        if zero is None: return False
        
        # Check add inverses
        for i in range(n):
            has_inv = False
            for j in range(n):
                if add_table[i][j] == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        # Check mul associativity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    ij = elements.index(mul_table[i][j])
                    jk = elements.index(mul_table[j][k])
                    if mul_table[ij][k] != mul_table[i][jk]: return False
                    
        # Check distributivity
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    jk = elements.index(add_table[j][k])
                    ij = elements.index(mul_table[i][j])
                    ik = elements.index(mul_table[i][k])
                    if mul_table[i][jk] != add_table[ij][ik]: return False
                    
                    ij_add = elements.index(add_table[i][j])
                    ik_mul = elements.index(mul_table[i][k])
                    jk_mul = elements.index(mul_table[j][k])
                    if mul_table[ij_add][k] != add_table[ik_mul][jk_mul]: return False
                    
        return True
    except Exception:
        return False

def is_ideal(elements, add_table, mul_table, ideal_elements):
    try:
        if not ideal_elements: return False
        zero = get_zero(elements, add_table)
        if zero is None or zero not in ideal_elements: return False
        
        for a in ideal_elements:
            for b in ideal_elements:
                i = elements.index(a)
                j = elements.index(b)
                if add_table[i][j] not in ideal_elements: return False
                
        for a in ideal_elements:
            i = elements.index(a)
            has_inv = False
            for b in ideal_elements:
                j = elements.index(b)
                if add_table[i][j] == zero and add_table[j][i] == zero:
                    has_inv = True
                    break
            if not has_inv: return False
            
        for r in elements:
            for x in ideal_elements:
                i = elements.index(r)
                j = elements.index(x)
                if mul_table[i][j] not in ideal_elements: return False
                if mul_table[j][i] not in ideal_elements: return False
                
        return True
    except Exception:
        return False

def is_proper_ideal(elements, add_table, mul_table, ideal_elements):
    try:
        if not is_ring(elements, add_table, mul_table): return False
        if not is_ideal(elements, add_table, mul_table, ideal_elements): return False
        ideal_set = set(ideal_elements)
        if not ideal_set.issubset(set(elements)): return False
        if len(ideal_set) == len(elements): return False
        return True
    except Exception:
        return False

def is_maximal_ideal(elements, add_table, mul_table, ideal_elements):
    try:
        if not is_proper_ideal(elements, add_table, mul_table, ideal_elements): return False
        n = len(elements)
        ideal_set = set(ideal_elements)
        for r in range(len(ideal_set) + 1, n):
            for subset in itertools.combinations(elements, r):
                subset_set = set(subset)
                if ideal_set.issubset(subset_set):
                    if is_ideal(elements, add_table, mul_table, list(subset)):
                        return False
        return True
    except Exception:
        return False

def quotient_is_field(elements, add_table, mul_table, ideal_elements):
    try:
        cosets = []
        for a in elements:
            i = elements.index(a)
            coset = set()
            for x in ideal_elements:
                j = elements.index(x)
                coset.add(add_table[i][j])
            if coset not in cosets:
                cosets.append(coset)
                
        if len(cosets) < 2:
            return False
            
        zero = get_zero(elements, add_table)
        zero_idx = elements.index(zero)
        zero_coset = set()
        for x in ideal_elements:
            j = elements.index(x)
            zero_coset.add(add_table[zero_idx][j])
            
        def mul_cosets(C1, C2):
            a = sorted(list(C1), key=lambda x: elements.index(x))[0]
            b = sorted(list(C2), key=lambda x: elements.index(x))[0]
            i = elements.index(a)
            j = elements.index(b)
            prod = mul_table[i][j]
            for C in cosets:
                if prod in C:
                    return C
            return None
            
        identity_coset = None
        for C in cosets:
            is_id = True
            for A in cosets:
                m1 = mul_cosets(C, A)
                m2 = mul_cosets(A, C)
                if m1 is None or m2 is None or m1 != A or m2 != A:
                    is_id = False
                    break
            if is_id:
                identity_coset = C
                break
                
        if identity_coset is None or identity_coset == zero_coset:
            return False
            
        for C in cosets:
            if C == zero_coset: continue
            has_inv = False
            for D in cosets:
                m1 = mul_cosets(C, D)
                m2 = mul_cosets(D, C)
                if m1 == identity_coset and m2 == identity_coset:
                    has_inv = True
                    break
            if not has_inv:
                return False
                
        for C in cosets:
            for D in cosets:
                m1 = mul_cosets(C, D)
                m2 = mul_cosets(D, C)
                if m1 is None or m2 is None or m1 != m2:
                    return False
                    
        return True
    except Exception:
        return False

def conditions(witness):
    try:
        if isinstance(witness, dict):
            elements = witness["elements"]
            add_table = witness["add"]
            mul_table = witness["mul"]
            ideal_elements = witness["ideal"]
        elif isinstance(witness, (tuple, list)) and len(witness) == 4:
            elements, add_table, mul_table, ideal_elements = witness
        elif isinstance(witness, (tuple, list)) and len(witness) == 2 and hasattr(witness[0], "add_table"):
            elements = witness[0].elements
            add_table = witness[0].add_table
            mul_table = witness[0].mul_table
            ideal_elements = witness[1]
        elif hasattr(witness, "ring") and hasattr(witness, "elements"):
            elements = witness.ring.elements
            add_table = witness.ring.add_table
            mul_table = witness.ring.mul_table
            ideal_elements = witness.elements
        else:
            return [False, False]
            
        h1 = is_proper_ideal(elements, add_table, mul_table, ideal_elements)
        
        try:
            is_max = is_maximal_ideal(elements, add_table, mul_table, ideal_elements)
            is_field = quotient_is_field(elements, add_table, mul_table, ideal_elements)
            q = (is_max == is_field)
            neg_q = not q
        except Exception:
            neg_q = False
            
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: M is a proper ideal of R",
    "¬Q: It is NOT the case that (M is a maximal ideal iff R/M is a field)"
]
N_HYP = 1
NEG_Q_INDEX = 1