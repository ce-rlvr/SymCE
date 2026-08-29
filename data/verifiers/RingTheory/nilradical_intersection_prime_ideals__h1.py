import itertools
from sympy import ImmutableMatrix, eye, zeros

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def _make_m2_f2():
    elements = []
    for entries in itertools.product([0, 1], repeat=4):
        elements.append(ImmutableMatrix(2, 2, entries))
    
    def add(A, B):
        return ImmutableMatrix((A + B).applyfunc(lambda x: x % 2))
        
    def mul(A, B):
        return ImmutableMatrix((A * B).applyfunc(lambda x: x % 2))
        
    zero = ImmutableMatrix(2, 2, [0, 0, 0, 0])
    return (elements, add, mul, zero)

M2_F2 = _make_m2_f2()

def _make_z4():
    elements = [0, 1, 2, 3]
    def add(a, b): return (a + b) % 4
    def mul(a, b): return (a * b) % 4
    zero = 0
    return (elements, add, mul, zero)

Z4 = _make_z4()

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 4:
            elements_raw, add_func, mul_func, zero_raw = witness
        elif hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero'):
            elements_raw = witness.elements
            add_func = witness.add
            mul_func = witness.mul
            zero_raw = witness.zero
        else:
            elements_raw = list(witness)
            add_func = lambda x, y: x + y
            mul_func = lambda x, y: x * y
            zero_raw = None
            for e in elements_raw:
                is_zero = True
                for x in elements_raw:
                    try:
                        if add_func(e, x) != x or add_func(x, e) != x:
                            is_zero = False
                            break
                    except Exception:
                        is_zero = False
                        break
                if is_zero:
                    zero_raw = e
                    break
            if zero_raw is None:
                return [False, False]
    except Exception:
        return [False, False]

    try:
        unique_elements = []
        for e in elements_raw:
            if e not in unique_elements:
                unique_elements.append(e)
        elements = unique_elements
        n_elems = len(elements)
        
        if n_elems == 0 or n_elems > 256:
            return [False, False]

        try:
            elem_to_idx = {e: i for i, e in enumerate(elements)}
            def get_idx(e):
                return elem_to_idx.get(e, -1)
        except TypeError:
            def get_idx(e):
                for i, x in enumerate(elements):
                    if x == e:
                        return i
                return -1

        add_table = [[0]*n_elems for _ in range(n_elems)]
        mul_table = [[0]*n_elems for _ in range(n_elems)]
        
        for i in range(n_elems):
            for j in range(n_elems):
                s = add_func(elements[i], elements[j])
                p = mul_func(elements[i], elements[j])
                s_idx = get_idx(s)
                p_idx = get_idx(p)
                if s_idx == -1 or p_idx == -1:
                    return [False, False]
                add_table[i][j] = s_idx
                mul_table[i][j] = p_idx
                
        zero_idx = get_idx(zero_raw)
        if zero_idx == -1:
            return [False, False]

        # Check ring axioms
        for i in range(n_elems):
            has_inv = False
            for j in range(n_elems):
                if add_table[i][j] == zero_idx and add_table[j][i] == zero_idx:
                    has_inv = True
                    break
            if not has_inv:
                return [False, False]
                
        if n_elems <= 64:
            for i in range(n_elems):
                for j in range(n_elems):
                    if add_table[i][j] != add_table[j][i]:
                        return [False, False]
                    for k in range(n_elems):
                        if add_table[add_table[i][j]][k] != add_table[i][add_table[j][k]]:
                            return [False, False]
                        if mul_table[mul_table[i][j]][k] != mul_table[i][mul_table[j][k]]:
                            return [False, False]
                        if mul_table[i][add_table[j][k]] != add_table[mul_table[i][j]][mul_table[i][k]]:
                            return [False, False]
                        if mul_table[add_table[i][j]][k] != add_table[mul_table[i][k]][mul_table[j][k]]:
                            return [False, False]
                            
        h1_ok = True
    except Exception:
        return [False, False]

    try:
        # Compute N (nilradical)
        N = set()
        for i in range(n_elems):
            curr = i
            is_nil = False
            for _ in range(n_elems):
                if curr == zero_idx:
                    is_nil = True
                    break
                curr = mul_table[curr][i]
            if is_nil:
                N.add(i)
                
        # Compute ideals
        def closure(seed_set):
            ideal = set(seed_set)
            added = True
            while added:
                added = False
                new_elements = set()
                for a in ideal:
                    for b in ideal:
                        s = add_table[a][b]
                        if s not in ideal and s not in new_elements:
                            new_elements.add(s)
                for a in ideal:
                    for r in range(n_elems):
                        p1 = mul_table[r][a]
                        if p1 not in ideal and p1 not in new_elements:
                            new_elements.add(p1)
                        p2 = mul_table[a][r]
                        if p2 not in ideal and p2 not in new_elements:
                            new_elements.add(p2)
                if new_elements:
                    ideal.update(new_elements)
                    added = True
            return frozenset(ideal)

        principal_ideals = set()
        for i in range(n_elems):
            principal_ideals.add(closure([i]))
            
        ideals = set(principal_ideals)
        added = True
        while added:
            added = False
            new_ideals = set()
            for I1 in ideals:
                for I2 in ideals:
                    sum_ideal = set()
                    for a in I1:
                        for b in I2:
                            sum_ideal.add(add_table[a][b])
                    sum_ideal = frozenset(sum_ideal)
                    if sum_ideal not in ideals and sum_ideal not in new_ideals:
                        new_ideals.add(sum_ideal)
                        if len(ideals) + len(new_ideals) > 1000:
                            return [False, False]
            if new_ideals:
                ideals.update(new_ideals)
                added = True

        # Find prime ideals
        prime_ideals = []
        for P in ideals:
            if len(P) == n_elems:
                continue
            is_prime = True
            for A in ideals:
                for B in ideals:
                    subset = True
                    for a in A:
                        for b in B:
                            if mul_table[a][b] not in P:
                                subset = False
                                break
                        if not subset:
                            break
                    if subset:
                        if not (A.issubset(P) or B.issubset(P)):
                            is_prime = False
                            break
                if not is_prime:
                    break
            if is_prime:
                prime_ideals.append(P)
                
        if not prime_ideals:
            intersection = set(range(n_elems))
        else:
            intersection = set(prime_ideals[0])
            for P in prime_ideals[1:]:
                intersection = intersection.intersection(P)
                
        neg_q_ok = (N != intersection)
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: Let N be the nilradical of R, consisting of all nilpotent elements of R",
    "¬Q: N is not equal to the intersection of all prime ideals of R"
]
N_HYP = 1
NEG_Q_INDEX = 1