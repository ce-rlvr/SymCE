import itertools
from sympy.combinatorics import PermutationGroup, Permutation, DirectProduct
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

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
V4 = DirectProduct(Z2, Z2)

def get_all_normal_subgroups(G, elements):
    id_elem = None
    for e in elements:
        if e * e == e:
            id_elem = e
            break
            
    classes = []
    unseen = set(elements)
    while unseen:
        x = unseen.pop()
        c = set()
        for g in elements:
            c.add(g * x * ~g)
        classes.append(c)
        unseen -= c
        
    class_list = list(classes)
    n_classes = len(class_list)
    
    id_class_idx = -1
    for i, c in enumerate(class_list):
        if id_elem in c:
            id_class_idx = i
            break
            
    elem_to_class = {}
    for i, c in enumerate(class_list):
        for e in c:
            elem_to_class[e] = i
            
    class_mult = {}
    for i in range(n_classes):
        a = next(iter(class_list[i]))
        for j in range(n_classes):
            mask = 0
            for b in class_list[j]:
                mask |= (1 << elem_to_class[a * b])
            class_mult[(i, j)] = mask
            
    gen_by_class = []
    for i in range(n_classes):
        mask = (1 << id_class_idx) | (1 << i)
        while True:
            new_mask = mask
            for x in range(n_classes):
                if (mask & (1 << x)):
                    for y in range(n_classes):
                        if (mask & (1 << y)):
                            new_mask |= class_mult[(x, y)]
            if new_mask == mask:
                break
            mask = new_mask
        gen_by_class.append(mask)
        
    all_normal_masks = set()
    queue = list(gen_by_class)
    all_normal_masks.update(gen_by_class)
    
    while queue:
        current = queue.pop(0)
        for g in gen_by_class:
            mask = 0
            for x in range(n_classes):
                if (current & (1 << x)):
                    for y in range(n_classes):
                        if (g & (1 << y)):
                            mask |= class_mult[(x, y)]
            if mask not in all_normal_masks:
                all_normal_masks.add(mask)
                queue.append(mask)
                
    normal_subgroups = []
    for mask in all_normal_masks:
        subset = set()
        for i in range(n_classes):
            if mask & (1 << i):
                subset.update(class_list[i])
        normal_subgroups.append(subset)
        
    return normal_subgroups

def is_semisimple(G):
    elements = list(G.generate_dimino())
    order = len(elements)
    normal_subgroups = get_all_normal_subgroups(G, elements)
    for N in normal_subgroups:
        has_complement = False
        for M in normal_subgroups:
            if len(N) * len(M) == order and len(N.intersection(M)) == 1:
                has_complement = True
                break
        if not has_complement:
            return False
    return True

def conditions(witness):
    try:
        G, N, M = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a finite group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: G is a semisimple group
    try:
        h2 = is_semisimple(G)
    except Exception:
        h2 = False
        
    # H3: M is the normal complement of N in G, meaning G is the internal direct product of N and M
    try:
        g_elements = set(G.generate_dimino())
        
        if hasattr(N, 'generate_dimino'):
            n_elements = set(N.generate_dimino())
        else:
            n_elements = set(N)
            
        if hasattr(M, 'generate_dimino'):
            m_elements = set(M.generate_dimino())
        else:
            m_elements = set(M)
            
        is_subgroups = n_elements.issubset(g_elements) and m_elements.issubset(g_elements)
        
        is_n_closed = all(a * b in n_elements for a in n_elements for b in n_elements)
        is_m_closed = all(a * b in m_elements for a in m_elements for b in m_elements)
        
        is_n_normal = all(g * n * ~g in n_elements for g in g_elements for n in n_elements)
        is_m_normal = all(g * m * ~g in m_elements for g in g_elements for m in m_elements)
        
        is_trivial_intersection = len(n_elements.intersection(m_elements)) == 1
        
        is_product_G = len(n_elements) * len(m_elements) == len(g_elements)
        
        h3 = is_subgroups and is_n_closed and is_m_closed and is_n_normal and is_m_normal and is_trivial_intersection and is_product_G
    except Exception:
        h3 = False
        
    # Conclusion: C_G(N) is equal to M
    try:
        c_g_n_elements = set()
        for g in g_elements:
            commutes = True
            for n in n_elements:
                if g * n != n * g:
                    commutes = False
                    break
            if commutes:
                c_g_n_elements.add(g)
                
        neg_q = c_g_n_elements != m_elements
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "H_2: G is a semisimple group",
    "H_3: M is the normal complement of N in G, meaning G is the internal direct product of N and M",
    "¬Q: The centralizer C_G(N) is not equal to M"
]

N_HYP = 3
NEG_Q_INDEX = 3