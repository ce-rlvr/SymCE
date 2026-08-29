import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
from sympy.matrices import eye, zeros

# Top-level setup
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = AbelianGroup(2, 2)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def get_identity(G):
    if hasattr(G, 'identity'):
        return G.identity
    elems = list(G.elements)
    if not elems:
        return None
    for g in elems:
        if g * elems[0] == elems[0]:
            return g
    return None

def get_phi_h_n(phi, h, n):
    if isinstance(phi, dict):
        if h not in phi:
            raise ValueError("h not in phi")
        phi_h = phi[h]
        if isinstance(phi_h, dict):
            if n not in phi_h:
                raise ValueError("n not in phi_h")
            return phi_h[n]
        elif callable(phi_h):
            return phi_h(n)
    elif callable(phi):
        phi_h = phi(h)
        if isinstance(phi_h, dict):
            if n not in phi_h:
                raise ValueError("n not in phi_h")
            return phi_h[n]
        elif callable(phi_h):
            return phi_h(n)
    raise ValueError("Invalid phi format")

def conditions(witness):
    try:
        if isinstance(witness, dict):
            N = witness['N']
            H = witness['H']
            phi = witness['phi']
        elif isinstance(witness, tuple):
            if len(witness) == 3:
                N, H, phi = witness
            elif len(witness) == 4:
                _, N, H, phi = witness
            else:
                return [False, False, False]
        else:
            N = witness.N
            H = witness.H
            phi = witness.phi
    except Exception:
        return [False, False, False]

    # H1: N and H are groups
    try:
        h1_ok = hasattr(N, 'elements') and get_identity(N) is not None and \
                hasattr(H, 'elements') and get_identity(H) is not None
    except Exception:
        h1_ok = False

    # H2: G = N \rtimes_\phi H is the external semidirect product of N and H
    try:
        if not h1_ok:
            h2_ok = False
        else:
            N_elems = list(N.elements)
            H_elems = list(H.elements)
            h2_ok = True
            
            for h in H_elems:
                mapped = []
                for n in N_elems:
                    mapped_n = get_phi_h_n(phi, h, n)
                    if mapped_n not in N_elems:
                        h2_ok = False
                        break
                    mapped.append(mapped_n)
                if not h2_ok: break
                
                if len(set(mapped)) != len(N_elems):
                    h2_ok = False
                    break
                
                for n1 in N_elems:
                    for n2 in N_elems:
                        if get_phi_h_n(phi, h, n1 * n2) != get_phi_h_n(phi, h, n1) * get_phi_h_n(phi, h, n2):
                            h2_ok = False
                            break
                    if not h2_ok: break
                if not h2_ok: break
                
            if h2_ok:
                for h1 in H_elems:
                    for h2_elem in H_elems:
                        h1h2 = h1 * h2_elem
                        for n in N_elems:
                            if get_phi_h_n(phi, h1h2, n) != get_phi_h_n(phi, h1, get_phi_h_n(phi, h2_elem, n)):
                                h2_ok = False
                                break
                        if not h2_ok: break
                    if not h2_ok: break
    except Exception:
        h2_ok = False

    # neg_Q: The centralizer of N x {1_H} in the subgroup {1_N} x H is NOT equal to {1_N} x ker(phi)
    try:
        if not h1_ok:
            neg_q = False
        else:
            N_elems = list(N.elements)
            H_elems = list(H.elements)
            N_id = get_identity(N)
            H_id = get_identity(H)
            
            C = []
            for h in H_elems:
                is_in_C = True
                for n in N_elems:
                    # (1, h) * (n, 1) = (phi(h)(n), h)
                    left_n = get_phi_h_n(phi, h, n)
                    left_h = h
                    
                    # (n, 1) * (1, h) = (n * phi(1)(1), h)
                    right_n = n * get_phi_h_n(phi, H_id, N_id)
                    right_h = h
                    
                    if left_n != right_n or left_h != right_h:
                        is_in_C = False
                        break
                if is_in_C:
                    C.append(h)
                    
            ker_phi = []
            for h in H_elems:
                is_in_ker = True
                for n in N_elems:
                    if get_phi_h_n(phi, h, n) != n:
                        is_in_ker = False
                        break
                if is_in_ker:
                    ker_phi.append(h)
                    
            # We compare the H-components since both sets are of the form {1_N} x S
            neg_q = set(C) != set(ker_phi)
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: G = N ⋊_φ H is the external semidirect product of N and H",
    "¬Q: The centralizer of N x {1_H} in {1_N} x H is not equal to {1_N} x ker(φ)"
]

N_HYP = 2
NEG_Q_INDEX = 2