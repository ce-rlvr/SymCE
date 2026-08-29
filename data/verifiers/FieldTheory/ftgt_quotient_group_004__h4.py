import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import itertools

# Top-level setup: named object bindings for witness expressions
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))

def get_quotient_table(G, N):
    """Computes the Cayley table of the quotient group G/N."""
    elements = sorted(list(G.generate()), key=lambda p: p.array_form)
    N_elements = sorted(list(N.generate()), key=lambda p: p.array_form)
    
    cosets = []
    coset_map = {}
    for g in elements:
        if g in coset_map:
            continue
        coset = frozenset(g * n for n in N_elements)
        cosets.append(coset)
        for c in coset:
            coset_map[c] = coset
            
    n_cosets = len(cosets)
    table = [[0] * n_cosets for _ in range(n_cosets)]
    for i in range(n_cosets):
        rep_i = sorted(list(cosets[i]), key=lambda p: p.array_form)[0]
        for j in range(n_cosets):
            rep_j = sorted(list(cosets[j]), key=lambda p: p.array_form)[0]
            prod = rep_i * rep_j
            prod_coset = coset_map[prod]
            table[i][j] = cosets.index(prod_coset)
    return table

def are_isomorphic(table1, table2):
    """Checks if two Cayley tables represent isomorphic groups."""
    n = len(table1)
    if len(table2) != n:
        return False
    if n == 1:
        return True
    
    def find_id(table):
        for i in range(n):
            if all(table[i][j] == j for j in range(n)) and all(table[j][i] == j for j in range(n)):
                return i
        return None
    
    id1 = find_id(table1)
    id2 = find_id(table2)
    if id1 is None or id2 is None:
        return False

    def get_element_orders(table, id_elem):
        orders = []
        for i in range(n):
            curr = i
            order = 1
            while curr != id_elem:
                curr = table[curr][i]
                order += 1
                if order > n:
                    break
            orders.append(order)
        return orders

    orders1 = get_element_orders(table1, id1)
    orders2 = get_element_orders(table2, id2)
    
    if sorted(orders1) != sorted(orders2):
        return False

    by_order1 = {}
    by_order2 = {}
    for i, o in enumerate(orders1):
        if i != id1:
            by_order1.setdefault(o, []).append(i)
    for i, o in enumerate(orders2):
        if i != id2:
            by_order2.setdefault(o, []).append(i)
            
    order_classes = list(by_order1.keys())
    class_perms = []
    for o in order_classes:
        class_perms.append(list(itertools.permutations(by_order2[o])))
        
    max_iters = 100000
    iters = 0
    for combo in itertools.product(*class_perms):
        iters += 1
        if iters > max_iters:
            return False
            
        mapping = {id1: id2}
        for o, perm in zip(order_classes, combo):
            for e1, e2 in zip(by_order1[o], perm):
                mapping[e1] = e2
                
        is_iso = True
        for i in range(n):
            for j in range(n):
                if mapping[table1[i][j]] != table2[mapping[i]][mapping[j]]:
                    is_iso = False
                    break
            if not is_iso:
                break
        if is_iso:
            return True
    return False

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            E_subgroup = witness.get('E_subgroup')
            H = witness.get('H')
        else:
            G, E_subgroup, H = witness
    except Exception:
        return [False, False, False, False]

    # H_1: K/F is a finite Galois extension with Galois group G
    try:
        h1 = isinstance(G, PermutationGroup) and G.order() > 0
    except Exception:
        h1 = False

    # H_2: E is an intermediate field such that F \subseteq E \subseteq K
    try:
        h2 = E_subgroup.is_subgroup(G)
    except Exception:
        h2 = False

    # H_3: The extension E/F is a normal extension
    try:
        h3 = E_subgroup.is_normal(G)
    except Exception:
        h3 = False

    # ¬Q: The Galois group Gal(E/F) is NOT isomorphic to the quotient group G/H
    try:
        if not isinstance(H, PermutationGroup):
            neg_q = True
        else:
            try:
                h_is_sub = H.is_subgroup(G)
            except Exception:
                h_is_sub = False
                
            if not h_is_sub:
                neg_q = True
            else:
                try:
                    h_is_norm = H.is_normal(G)
                except Exception:
                    h_is_norm = False
                    
                if not h_is_norm:
                    neg_q = True
                elif not E_subgroup.is_normal(G):
                    neg_q = True
                else:
                    table_E = get_quotient_table(G, E_subgroup)
                    table_H = get_quotient_table(G, H)
                    neg_q = not are_isomorphic(table_E, table_H)
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: K/F is a finite Galois extension with Galois group G",
    "H_2: E is an intermediate field such that F \\subseteq E \\subseteq K",
    "H_3: The extension E/F is a normal extension",
    "¬Q: The Galois group Gal(E/F) is NOT isomorphic to the quotient group G/H"
]

N_HYP = 3
NEG_Q_INDEX = 3