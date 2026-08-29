import math
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
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

def get_elements(group):
    if hasattr(group, 'generate') and callable(group.generate):
        return list(group.generate())
    elif hasattr(group, 'elements'):
        elems = group.elements
        if callable(elems):
            return list(elems())
        return list(elems)
    else:
        return list(group)

def get_order(group):
    if hasattr(group, 'order'):
        if callable(group.order):
            return group.order()
        return group.order
    return len(get_elements(group))

def conditions(witness):
    try:
        if isinstance(witness, dict):
            A = witness.get('A')
            G = witness.get('G')
            action_input = witness.get('action')
            C = witness.get('C')
        else:
            A, G, action_input, C = witness
            
        if callable(action_input):
            action = action_input
        elif isinstance(action_input, dict):
            action = lambda a, g: action_input[a][g]
        else:
            return [False] * 4
    except Exception:
        return [False] * 4

    # H1: A and G are finite groups
    try:
        A_elems = get_elements(A)
        G_elems = get_elements(G)
        order_A = int(get_order(A))
        order_G = int(get_order(G))
        
        h1 = (order_A > 0) and (order_G > 0)
        
        try:
            A_set = set(A_elems)
        except TypeError:
            A_set = A_elems
            
        try:
            G_set = set(G_elems)
        except TypeError:
            G_set = G_elems
        
        closed_A = all((a1 * a2) in A_set for a1 in A_elems for a2 in A_elems)
        closed_G = all((g1 * g2) in G_set for g1 in G_elems for g2 in G_elems)
        
        h1 = h1 and closed_A and closed_G
        
        if hasattr(A, 'identity'):
            id_A = A.identity
        else:
            id_A = None
            for a in A_elems:
                if all((a * x) == x for x in A_elems):
                    id_A = a
                    break
                    
        valid_action = True
        if id_A is not None:
            for g in G_elems:
                if action(id_A, g) != g:
                    valid_action = False
                    break
        else:
            valid_action = False
            
        if valid_action:
            for a in A_elems:
                for g in G_elems:
                    if action(a, g) not in G_set:
                        valid_action = False
                        break
                if not valid_action: break
                
        if valid_action:
            for a1 in A_elems:
                for a2 in A_elems:
                    a12 = a1 * a2
                    for g in G_elems:
                        if action(a12, g) != action(a1, action(a2, g)):
                            valid_action = False
                            break
                    if not valid_action: break
                if not valid_action: break
        h1 = h1 and valid_action
    except Exception:
        h1 = False

    # H2: The orders |A| and |G| are coprime
    try:
        h2 = math.gcd(order_A, order_G) == 1
    except Exception:
        h2 = False

    # H3: C is a conjugacy class of G, and A leaves C invariant
    try:
        C_list = list(C)
        if not C_list:
            h3 = False
        else:
            c = C_list[0]
            conj_class = []
            for g in G_elems:
                try:
                    inv_g = g**-1
                except Exception:
                    inv_g = ~g
                conj_elem = g * c * inv_g
                if conj_elem not in conj_class:
                    conj_class.append(conj_elem)
            
            is_conj_class = (len(C_list) == len(conj_class)) and all(x in conj_class for x in C_list)
            
            leaves_invariant = True
            for a in A_elems:
                for c_elem in C_list:
                    if action(a, c_elem) not in C_list:
                        leaves_invariant = False
                        break
                if not leaves_invariant:
                    break
                    
            h3 = is_conj_class and leaves_invariant
    except Exception:
        h3 = False

    # neg_Q: C does NOT contain any element fixed by the action of A
    try:
        has_fixed_point = False
        for c_elem in C_list:
            fixed = True
            for a in A_elems:
                if action(a, c_elem) != c_elem:
                    fixed = False
                    break
            if fixed:
                has_fixed_point = True
                break
        neg_q = not has_fixed_point
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: A and G are finite groups",
    "H_2: The orders |A| and |G| are coprime",
    "H_3: A leaves a conjugacy class C of G invariant",
    "¬Q: The conjugacy class C does not contain any element fixed by the action of A"
]

N_HYP = 3
NEG_Q_INDEX = 3