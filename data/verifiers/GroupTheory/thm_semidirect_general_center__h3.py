import math
import itertools
import functools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
from sympy import Rational, Integer, Symbol

# Top-level setup for named objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation(0, 1)(2, 3), Permutation(0, 2)(1, 3))
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
    "H_1: N is a valid group/subgroup",
    "H_2: H is a valid group/subgroup",
    "H_3: The action of H on N is a valid homomorphism to Aut(N)",
    "H_4: G is the semidirect product of N and H",
    "¬Q: Z(G) is not isomorphic to (Z(N) \\cap C_N(H)) \\times (Z(H) \\cap \\ker(\\phi))"
]

N_HYP = 4
NEG_Q_INDEX = 4

def check_internal(G, N, H):
    # H1: N is a subgroup of G
    try:
        H1 = all(g in G for g in N.generators)
    except Exception:
        H1 = False

    # H2: H is a subgroup of G
    try:
        H2 = all(g in G for g in H.generators)
    except Exception:
        H2 = False

    # H3: N is normal in G (conjugation is a valid action)
    try:
        if H1:
            H3 = True
            for n in N.generators:
                for g in G.generators:
                    if (g * n * ~g) not in N:
                        H3 = False
                        break
                if not H3:
                    break
        else:
            H3 = False
    except Exception:
        H3 = False

    # H4: N \cap H = {1} and G = NH
    try:
        N_elements = set(N.elements)
        H_elements = set(H.elements)
        intersection = N_elements.intersection(H_elements)
        H4 = (len(intersection) == 1) and (N.order() * H.order() == G.order())
    except Exception:
        H4 = False

    # neg_Q: Z(G) is not isomorphic to (Z(N) \cap C_N(H)) \times (Z(H) \cap \ker(\phi))
    try:
        if not (H1 and H2 and H3 and H4):
            return [H1, H2, H3, H4, False]

        Z_G = G.center()
        Z_N = N.center()
        Z_H = H.center()
        
        C_N_H_elements = []
        for n in N.elements:
            if all(h * n * ~h == n for h in H.generators):
                C_N_H_elements.append(n)
                
        ker_phi_elements = []
        for h in H.elements:
            if all(h * n * ~h == n for n in N.generators):
                ker_phi_elements.append(h)
                
        Z_N_elements = set(Z_N.elements)
        A_elements = [n for n in C_N_H_elements if n in Z_N_elements]
        
        Z_H_elements = set(Z_H.elements)
        B_elements = [h for h in ker_phi_elements if h in Z_H_elements]
        
        Z_G_orders = sorted([g.order() for g in Z_G.elements])
        
        def get_lcm(a, b):
            return (a * b) // math.gcd(a, b)
            
        AB_orders = []
        for a in A_elements:
            for b in B_elements:
                AB_orders.append(get_lcm(a.order(), b.order()))
        AB_orders.sort()
        
        neg_Q = (Z_G_orders != AB_orders)
    except Exception:
        neg_Q = False

    return [H1, H2, H3, H4, neg_Q]

def check_external(N, H, phi):
    # H1: N is a valid group
    try:
        H1 = hasattr(N, 'elements') and hasattr(N, 'identity')
    except Exception:
        H1 = False

    # H2: H is a valid group
    try:
        H2 = hasattr(H, 'elements') and hasattr(H, 'identity')
    except Exception:
        H2 = False

    # H3: phi is a valid homomorphism H -> Aut(N)
    try:
        def get_phi(h, n):
            if callable(phi):
                return phi(h, n)
            else:
                return phi[h][n]
                
        H3 = True
        id_N = N.identity
        id_H = H.identity
        for n in N.elements:
            if get_phi(id_H, n) != n:
                H3 = False
                break
        if H3:
            for h in H.elements:
                for n1 in N.elements:
                    for n2 in N.elements:
                        if get_phi(h, n1 * n2) != get_phi(h, n1) * get_phi(h, n2):
                            H3 = False
                            break
                    if not H3: break
                if not H3: break
        if H3:
            for h1 in H.elements:
                for h2 in H.elements:
                    for n in N.elements:
                        if get_phi(h1, get_phi(h2, n)) != get_phi(h1 * h2, n):
                            H3 = False
                            break
                    if not H3: break
                if not H3: break
    except Exception:
        H3 = False

    # H4: G is the semidirect product (trivially true for external construction)
    H4 = True if (H1 and H2 and H3) else False
    
    # neg_Q: Z(G) is not isomorphic to (Z(N) \cap C_N(H)) \times (Z(H) \cap \ker(\phi))
    try:
        if not (H1 and H2 and H3 and H4):
            return [H1, H2, H3, H4, False]
            
        Z_G_elements = []
        for n in N.elements:
            for h in H.elements:
                if any(h * k != k * h for k in H.elements):
                    continue
                is_central = True
                for m in N.elements:
                    for k in H.elements:
                        left = n * get_phi(h, m)
                        right = m * get_phi(k, n)
                        if left != right:
                            is_central = False
                            break
                    if not is_central: break
                if is_central:
                    Z_G_elements.append((n, h))
                    
        Z_G_orders = []
        for n, h in Z_G_elements:
            curr_n, curr_h = n, h
            order = 1
            while curr_n != id_N or curr_h != id_H:
                curr_n = curr_n * get_phi(curr_h, n)
                curr_h = curr_h * h
                order += 1
                if order > N.order() * H.order():
                    break
            Z_G_orders.append(order)
        Z_G_orders.sort()
        
        Z_N = N.center()
        C_N_H = []
        for n in N.elements:
            if all(get_phi(h, n) == n for h in H.elements):
                C_N_H.append(n)
        Z_N_elements = set(Z_N.elements)
        A_elements = [n for n in C_N_H if n in Z_N_elements]
        
        Z_H = H.center()
        ker_phi = []
        for h in H.elements:
            if all(get_phi(h, n) == n for n in N.elements):
                ker_phi.append(h)
        Z_H_elements = set(Z_H.elements)
        B_elements = [h for h in ker_phi if h in Z_H_elements]
        
        def get_lcm(a, b):
            return (a * b) // math.gcd(a, b)
            
        AB_orders = []
        for a in A_elements:
            for b in B_elements:
                AB_orders.append(get_lcm(a.order(), b.order()))
        AB_orders.sort()
        
        neg_Q = (Z_G_orders != AB_orders)
    except Exception:
        neg_Q = False

    return [H1, H2, H3, H4, neg_Q]

def conditions(witness) -> list[bool]:
    try:
        if len(witness) == 3:
            if hasattr(witness[2], 'generators') and hasattr(witness[2], 'elements'):
                return check_internal(witness[0], witness[1], witness[2])
            else:
                return check_external(witness[0], witness[1], witness[2])
    except Exception:
        pass
    return [False] * 5