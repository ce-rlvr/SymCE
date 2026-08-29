import itertools
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    try:
        N = witness['N']
        H = witness['H']
        phi = witness['phi']
        psi = witness['psi']
        alpha = witness['alpha']
        N_op = witness.get('N_op', None)
        H_op = witness.get('H_op', None)
    except Exception:
        return [False, False, False]

    def apply_op(op, a, b):
        if op is None: return a * b
        if isinstance(op, dict): return op[(a, b)]
        return op(a, b)

    def make_op(op_obj):
        return lambda a, b: apply_op(op_obj, a, b)

    def apply_map1(m, a):
        if isinstance(m, dict): return m[a]
        return m(a)

    def apply_map2(m, a, b):
        if isinstance(m, dict):
            val = m[a]
            if isinstance(val, dict): return val[b]
            return val(b)
        try:
            return m(a, b)
        except Exception:
            return m(a)(b)

    def is_group(elements, op):
        elements = list(elements)
        if not elements: return False
        # closure
        for a in elements:
            for b in elements:
                try:
                    if op(a, b) not in elements: return False
                except Exception:
                    return False
        # associativity
        for a in elements:
            for b in elements:
                for c in elements:
                    try:
                        if op(op(a, b), c) != op(a, op(b, c)):
                            return False
                    except Exception:
                        return False
        # identity
        identity = None
        for e in elements:
            try:
                is_id = True
                for a in elements:
                    if op(e, a) != a or op(a, e) != a:
                        is_id = False
                        break
                if is_id:
                    identity = e
                    break
            except Exception:
                pass
        if identity is None: return False
        # inverses
        for a in elements:
            has_inv = False
            for b in elements:
                try:
                    if op(a, b) == identity and op(b, a) == identity:
                        has_inv = True
                        break
                except Exception:
                    pass
            if not has_inv: return False
        return True

    # H_1: N and H are groups
    try:
        N_list = list(N)
        H_list = list(H)
        if len(N_list) > 100 or len(H_list) > 100:
            h1 = False
        else:
            h1 = is_group(N_list, make_op(N_op)) and is_group(H_list, make_op(H_op))
    except Exception:
        h1 = False

    # H_2: alpha in Aut(N) and psi(h) = alpha o phi(h) o alpha^-1
    try:
        N_list = list(N)
        H_list = list(H)
        N_op_fn = make_op(N_op)
        
        alpha_img = [apply_map1(alpha, n) for n in N_list]
        is_bijection = True
        for n in N_list:
            if alpha_img.count(n) != 1:
                is_bijection = False
                break
        
        is_homo = True
        for a in N_list:
            for b in N_list:
                if apply_map1(alpha, N_op_fn(a, b)) != N_op_fn(apply_map1(alpha, a), apply_map1(alpha, b)):
                    is_homo = False
                    break
            if not is_homo: break
            
        alpha_is_aut = is_bijection and is_homo

        conjugate_holds = True
        for h in H_list:
            for n in N_list:
                left = apply_map2(psi, h, apply_map1(alpha, n))
                right = apply_map1(alpha, apply_map2(phi, h, n))
                if left != right:
                    conjugate_holds = False
                    break
            if not conjugate_holds: break
            
        h2 = alpha_is_aut and conjugate_holds
    except Exception:
        h2 = False

    # ¬Q: The semidirect products N rtimes_phi H and N rtimes_psi H are not isomorphic groups
    try:
        N_list = list(N)
        H_list = list(H)
        SDP_elements = list(itertools.product(N_list, H_list))
        N_op_fn = make_op(N_op)
        H_op_fn = make_op(H_op)
        
        def op_phi(x, y):
            n1, h1_el = x
            n2, h2_el = y
            phi_h1_n2 = apply_map2(phi, h1_el, n2)
            n_res = N_op_fn(n1, phi_h1_n2)
            h_res = H_op_fn(h1_el, h2_el)
            return (n_res, h_res)
            
        def op_psi(x, y):
            n1, h1_el = x
            n2, h2_el = y
            psi_h1_n2 = apply_map2(psi, h1_el, n2)
            n_res = N_op_fn(n1, psi_h1_n2)
            h_res = H_op_fn(h1_el, h2_el)
            return (n_res, h_res)

        is_g_phi = is_group(SDP_elements, op_phi)
        is_g_psi = is_group(SDP_elements, op_psi)
        
        if not is_g_phi or not is_g_psi:
            are_isomorphic = False
        else:
            def get_orders(elements, op):
                identity = None
                for e in elements:
                    is_id = True
                    for a in elements:
                        if op(e, a) != a or op(a, e) != a:
                            is_id = False
                            break
                    if is_id:
                        identity = e
                        break
                orders = []
                for a in elements:
                    curr = a
                    order = 1
                    while curr != identity and order <= len(elements):
                        curr = op(curr, a)
                        order += 1
                    orders.append(order)
                return sorted(orders)
            
            orders_phi = get_orders(SDP_elements, op_phi)
            orders_psi = get_orders(SDP_elements, op_psi)
            
            if orders_phi != orders_psi:
                are_isomorphic = False
            else:
                are_isomorphic = True
                
        neg_q = not are_isomorphic
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: alpha is an automorphism of N and psi(h) = alpha o phi(h) o alpha^-1",
    "¬Q: The semidirect products N rtimes_phi H and N rtimes_psi H are not isomorphic groups"
]

N_HYP = 2
NEG_Q_INDEX = 2