import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools

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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False

    try:
        if isinstance(witness, tuple):
            G = witness[0]
            H = witness[1]
            g = witness[2]
            h = witness[3]
        else:
            G = witness.G
            H = witness.H
            g = witness.g
            h = witness.h
    except Exception:
        return [False, False, False]

    # H1: g is an element of G
    try:
        if hasattr(G, 'elements'):
            G_list = list(G.elements)
        else:
            G_list = list(G)
        h1 = g in G_list
    except Exception:
        h1 = False
        G_list = []

    # H2: h is an element of H
    try:
        if hasattr(H, 'elements'):
            H_list = list(H.elements)
        else:
            H_list = list(H)
        h2 = h in H_list
    except Exception:
        h2 = False
        H_list = []

    # Conclusion: The conjugacy class of (g, h) in G × H is the Cartesian product of the conjugacy class of g in G and the conjugacy class of h in H.
    try:
        # Check if conjugacy classes are explicitly provided in the witness
        if isinstance(witness, tuple) and len(witness) >= 7:
            C_G_g = set(witness[4])
            C_H_h = set(witness[5])
            C_GxH_gh = set(witness[6])
            cartesian = {(x, y) for x in C_G_g for y in C_H_h}
            neg_q = (C_GxH_gh != cartesian)
            return [bool(h1), bool(h2), bool(neg_q)]
            
        if not isinstance(witness, tuple) and hasattr(witness, 'C_G_g') and hasattr(witness, 'C_H_h') and hasattr(witness, 'C_GxH_gh'):
            C_G_g = set(witness.C_G_g)
            C_H_h = set(witness.C_H_h)
            C_GxH_gh = set(witness.C_GxH_gh)
            cartesian = {(x, y) for x in C_G_g for y in C_H_h}
            neg_q = (C_GxH_gh != cartesian)
            return [bool(h1), bool(h2), bool(neg_q)]

        # Otherwise, compute them
        if isinstance(witness, tuple):
            GxH = witness[4] if len(witness) > 4 else None
            gh = witness[5] if len(witness) > 5 else (g, h)
        else:
            GxH = getattr(witness, 'GxH', None)
            gh = getattr(witness, 'gh', (g, h))

        def get_cc(elem, cont, cont_list=None):
            if hasattr(cont, 'conjugacy_class'):
                res = cont.conjugacy_class(elem)
                return set(res) if res is not None else set()
            if hasattr(elem, 'conjugacy_class'):
                res = elem.conjugacy_class(cont)
                return set(res) if res is not None else set()
            
            if cont_list is None:
                cont_list = list(cont) if not hasattr(cont, 'elements') else list(cont.elements)
                
            c = set()
            computed = False
            
            # Try group definition
            for x in cont_list:
                try:
                    c.add(x * elem * x**-1)
                    computed = True
                except Exception:
                    try:
                        c.add(x * elem * ~x)
                        computed = True
                    except Exception:
                        pass
            if computed: return c
            
            # Try semigroup definition
            for x in cont_list:
                for y in cont_list:
                    try:
                        xy = x * y
                        computed = True
                        if xy == elem:
                            c.add(y * x)
                    except Exception:
                        pass
            if computed: return c
            
            raise ValueError("Cannot compute CC")

        C_G_g = get_cc(g, G, G_list)
        C_H_h = get_cc(h, H, H_list)
        cartesian = {(x, y) for x in C_G_g for y in C_H_h}

        if GxH is not None:
            C_GxH_gh = get_cc(gh, GxH)
        else:
            C_GxH_gh = set()
            computed_group = False
            computed_semi = False
            
            # Try group definition for pairs
            for x in G_list:
                for y in H_list:
                    try:
                        c_g = x * g * x**-1
                        c_h = y * h * y**-1
                        C_GxH_gh.add((c_g, c_h))
                        computed_group = True
                    except Exception:
                        try:
                            c_g = x * g * ~x
                            c_h = y * h * ~y
                            C_GxH_gh.add((c_g, c_h))
                            computed_group = True
                        except Exception:
                            pass
                            
            if not computed_group:
                # Try semigroup definition for pairs
                for x in G_list:
                    for u in H_list:
                        for y in G_list:
                            for v in H_list:
                                try:
                                    xy = x * y
                                    uv = u * v
                                    computed_semi = True
                                    if xy == g and uv == h:
                                        C_GxH_gh.add((y * x, v * u))
                                except Exception:
                                    pass
            
            if not computed_group and not computed_semi:
                raise ValueError("Could not compute C_GxH_gh")
                                    
        neg_q = (C_GxH_gh != cartesian)
        
    except Exception:
        neg_q = False

    return [bool(h1), bool(h2), bool(neg_q)]

CONDITION_LABELS = [
    "H_1: g is an element of G",
    "H_2: h is an element of H",
    "¬Q: The conjugacy class of (g, h) in G × H is NOT the Cartesian product of the conjugacy class of g in G and the conjugacy class of h in H"
]

N_HYP = 2
NEG_Q_INDEX = 2