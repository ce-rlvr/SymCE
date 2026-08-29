import sympy
from sympy import eye, zeros

# Top-level setup for potential witness expressions
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def build_tables(elements, I_elements):
    n = len(elements)
    def get_idx(x):
        for i, e in enumerate(elements):
            if e == x:
                return i
        raise ValueError(f"Element {x} not found in ring")
        
    add_table = [[0]*n for _ in range(n)]
    mult_table = [[0]*n for _ in range(n)]
    
    for i, m1 in enumerate(elements):
        for j, m2 in enumerate(elements):
            add_table[i][j] = get_idx(m1 + m2)
            mult_table[i][j] = get_idx(m1 * m2)
            
    I_indices = [get_idx(m) for m in I_elements]
    return n, add_table, mult_table, I_indices

def is_ideal(n, add_table, mult_table, subset):
    if not subset: 
        return False
    # Check closure under addition
    for i in subset:
        for j in subset:
            if add_table[i][j] not in subset:
                return False
    # Find zero element
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
    if zero is None or zero not in subset:
        return False
    # Check closure under additive inverse
    for i in subset:
        inv = None
        for j in range(n):
            if add_table[i][j] == zero:
                inv = j
                break
        if inv is None or inv not in subset:
            return False
    # Check absorbing property (two-sided)
    for i in subset:
        for r in range(n):
            if mult_table[r][i] not in subset:
                return False
            if mult_table[i][r] not in subset:
                return False
    return True

def generate_ideal(n, add_table, mult_table, generators):
    ideal = set(generators)
    zero = None
    for i in range(n):
        if all(add_table[i][j] == j for j in range(n)):
            zero = i
            break
            
    changed = True
    while changed:
        changed = False
        new_elements = set()
        for i in ideal:
            for j in ideal:
                new_elements.add(add_table[i][j])
            for r in range(n):
                new_elements.add(mult_table[r][i])
                new_elements.add(mult_table[i][r])
        if zero is not None:
            for i in ideal:
                for j in range(n):
                    if add_table[i][j] == zero:
                        new_elements.add(j)
                        break
        if not new_elements.issubset(ideal):
            ideal.update(new_elements)
            changed = True
    return frozenset(ideal)

def get_all_ideals(n, add_table, mult_table):
    principal_ideals = set()
    for i in range(n):
        principal_ideals.add(generate_ideal(n, add_table, mult_table, [i]))
    
    ideals = set(principal_ideals)
    changed = True
    while changed:
        changed = False
        new_ideals = set()
        for I1 in ideals:
            for I2 in ideals:
                sum_ideal = set()
                for i in I1:
                    for j in I2:
                        sum_ideal.add(add_table[i][j])
                sum_ideal = generate_ideal(n, add_table, mult_table, sum_ideal)
                if sum_ideal not in ideals:
                    new_ideals.add(sum_ideal)
        if new_ideals:
            ideals.update(new_ideals)
            changed = True
    return ideals

def is_prime_ideal(n, add_table, mult_table, P, all_ideals):
    if len(P) == n:
        return False
    for A in all_ideals:
        for B in all_ideals:
            ab_in_P = True
            for a in A:
                for b in B:
                    if mult_table[a][b] not in P:
                        ab_in_P = False
                        break
                if not ab_in_P:
                    break
            if ab_in_P:
                if not (A.issubset(P) or B.issubset(P)):
                    return False
    return True

def conditions(witness):
    """
    witness can be either:
      - A tuple (elements, I_elements) where elements is a list of ring elements 
        (e.g. SymPy matrices) closed under + and *, and I_elements is a sublist.
      - A tuple (n, add_table, mult_table, I_indices) representing a finite ring directly.
    """
    try:
        if len(witness) == 2:
            elements, I_elements = witness
            n, add_table, mult_table, I_indices = build_tables(elements, I_elements)
        elif len(witness) == 4:
            n, add_table, mult_table, I_indices = witness
        else:
            return [False, False]
            
        # H_1: I is a proper ideal of R
        h1 = is_ideal(n, add_table, mult_table, I_indices) and len(set(I_indices)) < n
        
        # Conclusion: The radical of I is equal to the intersection of all prime ideals of R that contain I.
        all_ideals = get_all_ideals(n, add_table, mult_table)
        primes = [P for P in all_ideals if is_prime_ideal(n, add_table, mult_table, P, all_ideals)]
        primes_containing_I = [P for P in primes if set(I_indices).issubset(P)]
        
        if not primes_containing_I:
            intersection = set(range(n))
        else:
            intersection = set(primes_containing_I[0])
            for P in primes_containing_I[1:]:
                intersection = intersection.intersection(P)
                
        rad = set()
        for r in range(n):
            current = r
            found = False
            for power in range(1, n + 2):
                if current in I_indices:
                    found = True
                    break
                current = mult_table[current][r]
            if found:
                rad.add(r)
                
        neg_q = (rad != intersection)
        
        return [bool(h1), bool(neg_q)]
    except Exception:
        return [False, False]

CONDITION_LABELS = [
    "H_1: I is a proper ideal of R",
    "¬Q: The radical of I is not equal to the intersection of all prime ideals of R that contain I"
]

N_HYP = 1
NEG_Q_INDEX = 1