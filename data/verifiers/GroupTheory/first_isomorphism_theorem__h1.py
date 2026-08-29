import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
import functools
import math

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            if 'G_elements' in witness:
                G_elements = witness['G_elements']
                G_op = witness['G_op']
                H = witness['H']
                phi = witness['phi']
            else:
                G = witness['G']
                H = witness['H']
                phi = witness['phi']
                G_elements = list(G.elements)
                G_op = lambda x, y: x * y
        elif len(witness) == 4:
            G_elements, G_op, H, phi = witness
        elif len(witness) == 3:
            G, H, phi = witness
            G_elements = list(G.elements)
            G_op = lambda x, y: x * y
        else:
            return [False, False, False]
            
        def op(x, y):
            if callable(G_op):
                return G_op(x, y)
            else:
                return G_op[(x, y)]
                
        def get_phi(x):
            if callable(phi):
                return phi(x)
            else:
                return phi[x]
    except Exception:
        return [False, False, False]

    # H_1: H is a group
    try:
        h1 = hasattr(H, 'identity')
    except Exception:
        h1 = False

    # H_2: \phi is a group homomorphism from G to H
    try:
        h2 = True
        for x in G_elements:
            for y in G_elements:
                xy = op(x, y)
                if get_phi(xy) != get_phi(x) * get_phi(y):
                    h2 = False
                    break
            if not h2:
                break
    except Exception:
        h2 = False

    # neg_Q: The kernel \ker(\phi) is a normal subgroup of G, and G/\ker(\phi) \cong \phi(G).
    try:
        def same_multiset(l1, l2):
            if len(l1) != len(l2): return False
            l2_copy = list(l2)
            for item in l1:
                if item in l2_copy:
                    l2_copy.remove(item)
                else:
                    return False
            return True

        H_id = H.identity
        ker = [x for x in G_elements if get_phi(x) == H_id]
        
        identities = []
        for e_cand in G_elements:
            is_id = True
            for x in G_elements:
                if op(e_cand, x) != x or op(x, e_cand) != x:
                    is_id = False
                    break
            if is_id:
                identities.append(e_cand)
        
        q = True
        if not identities:
            q = False
        else:
            e = identities[0]
            
            # Check if G is a group
            is_G_group = True
            assoc = True
            for a in G_elements:
                for b in G_elements:
                    for c in G_elements:
                        if op(op(a, b), c) != op(a, op(b, c)):
                            assoc = False
                            break
                    if not assoc: break
                if not assoc: break
            if not assoc:
                is_G_group = False
            else:
                has_inverses_G = all(any(op(x, y) == e and op(y, x) == e for y in G_elements) for x in G_elements)
                if not has_inverses_G:
                    is_G_group = False
            
            if not is_G_group:
                q = False
            elif e not in ker:
                q = False
            else:
                closed = all(op(x, y) in ker for x in ker for y in ker)
                if not closed:
                    q = False
                else:
                    has_inverses = all(any(op(x, y) == e and op(y, x) == e for y in ker) for x in ker)
                    if not has_inverses:
                        q = False
                    else:
                        is_normal = True
                        for g in G_elements:
                            left = [op(g, k) for k in ker]
                            right = [op(k, g) for k in ker]
                            if not same_multiset(left, right):
                                is_normal = False
                                break
                        if not is_normal:
                            q = False
                        else:
                            well_defined = True
                            cosets = []
                            for g in G_elements:
                                c = [op(g, k) for k in ker]
                                is_in = False
                                for existing_c in cosets:
                                    if same_multiset(c, existing_c):
                                        is_in = True
                                        break
                                if not is_in:
                                    cosets.append(c)
                            
                            for a in G_elements:
                                for b in G_elements:
                                    a_ker = [op(a, k) for k in ker]
                                    b_ker = [op(b, k) for k in ker]
                                    ab_ker = [op(op(a, b), k) for k in ker]
                                    for a1 in a_ker:
                                        for b1 in b_ker:
                                            a1b1_ker = [op(op(a1, b1), k) for k in ker]
                                            if not same_multiset(a1b1_ker, ab_ker):
                                                well_defined = False
                                                break
                                        if not well_defined: break
                                if not well_defined: break
                            
                            if not well_defined:
                                q = False
                            else:
                                im_phi = []
                                for x in G_elements:
                                    val = get_phi(x)
                                    if val not in im_phi:
                                        im_phi.append(val)
                                if len(cosets) != len(im_phi):
                                    q = False
                                else:
                                    q = True
        neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: H is a group",
    "H_2: \\phi is a group homomorphism from G to H",
    "¬Q: The kernel \\ker(\\phi) is not a normal subgroup of G, or G/\\ker(\\phi) is not isomorphic to \\phi(G)"
]

N_HYP = 2
NEG_Q_INDEX = 2