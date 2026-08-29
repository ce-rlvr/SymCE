import sympy
import sympy.combinatorics as comb
import itertools

# Standard algebra objects
S3 = comb.SymmetricGroup(3)
S4 = comb.SymmetricGroup(4)
A4 = comb.AlternatingGroup(4)
D4 = comb.DihedralGroup(4)
C4 = comb.CyclicGroup(4)
V4 = comb.AlternatingGroup(4)
Z2 = comb.CyclicGroup(2)
Z3 = comb.CyclicGroup(3)
Z4 = comb.CyclicGroup(4)
Z6 = comb.CyclicGroup(6)
trivial = comb.CyclicGroup(1)

I2 = sympy.eye(2)
I3 = sympy.eye(3)
O2 = sympy.zeros(2, 2)
O3 = sympy.zeros(3, 3)

def conditions(witness):
    try:
        def eq(a, b):
            return a == b

        # Duck-typing to support both custom ring objects and simple tuples (S, x)
        if hasattr(witness, 'elements') and hasattr(witness, 'add') and hasattr(witness, 'mul') and hasattr(witness, 'zero') and hasattr(witness, 'x'):
            raw_elements = []
            for i, e in enumerate(witness.elements):
                if i > 1000: return [False, False, False]
                raw_elements.append(e)
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            x = witness.x
        else:
            S, x = witness
            raw_elements = []
            for i, e in enumerate(S):
                if i > 1000: return [False, False, False]
                raw_elements.append(e)
            if not raw_elements:
                return [False, False, False]
            
            def add(a, b): return a + b
            def mul(a, b): return a * b
            
            zero = None
            for e in raw_elements:
                if all(eq(add(e, a), a) for a in raw_elements) and all(eq(add(a, e), a) for a in raw_elements):
                    zero = e
                    break
            if zero is None:
                return [False, False, False]

        # Deduplicate elements
        elements = []
        for e in raw_elements:
            if not any(eq(e, u) for u in elements):
                elements.append(e)
        n = len(elements)
        if n == 0: return [False, False, False]

        def get_idx(e):
            for i, el in enumerate(elements):
                if eq(e, el): return i
            return -1

        # Precompute addition and multiplication tables
        add_table = [[0]*n for _ in range(n)]
        mul_table = [[0]*n for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                s = add(elements[i], elements[j])
                idx = get_idx(s)
                if idx == -1: return [False, False, False]
                add_table[i][j] = idx
                
                p = mul(elements[i], elements[j])
                idx = get_idx(p)
                if idx == -1: return [False, False, False]
                mul_table[i][j] = idx

        zero_idx = get_idx(zero)
        if zero_idx == -1: return [False, False, False]
        
        x_idx = get_idx(x)
        if x_idx == -1: return [False, False, False]

        # Find additive inverses
        neg_table = [-1]*n
        for i in range(n):
            for j in range(n):
                if add_table[i][j] == zero_idx and add_table[j][i] == zero_idx:
                    neg_table[i] = j
                    break
            if neg_table[i] == -1:
                return [False, False, False]

        # Find two-sided identity
        id_idx = -1
        for i in range(n):
            is_id = True
            for j in range(n):
                if mul_table[i][j] != j or mul_table[j][i] != j:
                    is_id = False
                    break
            if is_id:
                id_idx = i
                break

        # Generate two-sided ideals
        def generate_ideal(gen_indices):
            ideal = set(gen_indices)
            ideal.add(zero_idx)
            changed = True
            while changed:
                changed = False
                new_elems = set()
                for i in ideal:
                    for j in ideal:
                        diff = add_table[i][neg_table[j]]
                        if diff not in ideal and diff not in new_elems:
                            new_elems.add(diff)
                        summ = add_table[i][j]
                        if summ not in ideal and summ not in new_elems:
                            new_elems.add(summ)
                for i in ideal:
                    for r in range(n):
                        p1 = mul_table[i][r]
                        if p1 not in ideal and p1 not in new_elems:
                            new_elems.add(p1)
                        p2 = mul_table[r][i]
                        if p2 not in ideal and p2 not in new_elems:
                            new_elems.add(p2)
                if new_elems:
                    ideal.update(new_elems)
                    changed = True
            return frozenset(ideal)

        all_ideals = set()
        for i in range(n):
            all_ideals.add(generate_ideal([i]))
            
        changed = True
        while changed:
            changed = False
            new_ideals = set()
            for I1 in all_ideals:
                for I2 in all_ideals:
                    union_gen = I1.union(I2)
                    I3 = generate_ideal(union_gen)
                    if I3 not in all_ideals and I3 not in new_ideals:
                        new_ideals.add(I3)
            if new_ideals:
                all_ideals.update(new_ideals)
                changed = True

        proper_ideals = [I for I in all_ideals if len(I) < n]
        maximal_ideals = []
        for I in proper_ideals:
            is_max = True
            for J in proper_ideals:
                if I != J and I.issubset(J):
                    is_max = False
                    break
            if is_max:
                maximal_ideals.append(I)

        if not maximal_ideals:
            intersection_max_ideals = frozenset(range(n))
        else:
            intersection_max_ideals = frozenset.intersection(*maximal_ideals)

        # Compute Jacobson Radical J(R)
        def is_quasi_regular(q):
            for b in range(n):
                qb = mul_table[q][b]
                neg_qb = neg_table[qb]
                sum1 = add_table[add_table[q][b]][neg_qb]
                
                bq = mul_table[b][q]
                neg_bq = neg_table[bq]
                sum2 = add_table[add_table[q][b]][neg_bq]
                
                if sum1 == zero_idx and sum2 == zero_idx:
                    return True
            return False

        JR = set()
        for a in range(n):
            a_in_JR = True
            for y in range(n):
                ay = mul_table[a][y]
                if not is_quasi_regular(ay):
                    a_in_JR = False
                    break
            if a_in_JR:
                JR.add(a)
        JR = frozenset(JR)

        # Evaluate hypotheses
        h1 = (JR == intersection_max_ideals)
        h2 = (x_idx in JR)

        # Evaluate conclusion
        def is_unit(u):
            if id_idx == -1: return False
            for v in range(n):
                if mul_table[u][v] == id_idx and mul_table[v][u] == id_idx:
                    return True
            return False

        if id_idx == -1:
            neg_Q = True
        else:
            all_units = True
            for y in range(n):
                xy = mul_table[x_idx][y]
                neg_xy = neg_table[xy]
                one_minus_xy = add_table[id_idx][neg_xy]
                if not is_unit(one_minus_xy):
                    all_units = False
                    break
            neg_Q = not all_units

        return [bool(h1), bool(h2), bool(neg_Q)]
    except Exception:
        return [False, False, False]

CONDITION_LABELS = [
    "H_1: J(R) is the intersection of all maximal ideals of R",
    "H_2: x in J(R)",
    "¬Q: 1 - xy is not a unit for some y in R (or 1 does not exist)"
]

N_HYP = 2
NEG_Q_INDEX = 2