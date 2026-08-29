import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, tuple) and len(witness) == 5:
            G, op, X, action, x = witness
        else:
            G = witness.G
            op = witness.op
            X = witness.X
            action = witness.action
            x = witness.x
    except Exception:
        return [False, False, False, False]

    # H1: X is a set
    try:
        h1 = hasattr(X, '__iter__') and hasattr(X, '__len__') and len(X) > 0
    except Exception:
        h1 = False

    # H2: G acts on X
    try:
        h2 = False
        if hasattr(G, '__iter__') and hasattr(G, '__len__'):
            if 0 < len(G) <= 200:
                G_elements = []
                for g in G:
                    if g not in G_elements:
                        G_elements.append(g)
                
                X_elements = []
                for y in X:
                    if y not in X_elements:
                        X_elements.append(y)
                
                # Check closure of op
                closed = True
                for g1 in G_elements:
                    for g2 in G_elements:
                        if op(g1, g2) not in G_elements:
                            closed = False
                            break
                    if not closed: break
                
                if closed:
                    # Check associativity
                    assoc = True
                    for g1 in G_elements:
                        for g2 in G_elements:
                            for g3 in G_elements:
                                if op(g1, op(g2, g3)) != op(op(g1, g2), g3):
                                    assoc = False
                                    break
                            if not assoc: break
                        if not assoc: break
                    
                    if assoc:
                        # Find identity
                        e = None
                        for g in G_elements:
                            is_e = True
                            for h in G_elements:
                                if op(g, h) != h or op(h, g) != h:
                                    is_e = False
                                    break
                            if is_e:
                                e = g
                                break
                        
                        if e is not None:
                            # Check action closure
                            act_closed = True
                            for g in G_elements:
                                for y in X_elements:
                                    if action(g, y) not in X_elements:
                                        act_closed = False
                                        break
                                if not act_closed: break
                            
                            if act_closed:
                                # Check action identity
                                act_id = True
                                for y in X_elements:
                                    if action(e, y) != y:
                                        act_id = False
                                        break
                                
                                if act_id:
                                    # Check action compatibility
                                    act_comp = True
                                    for g1 in G_elements:
                                        for g2 in G_elements:
                                            for y in X_elements:
                                                if action(g1, action(g2, y)) != action(op(g1, g2), y):
                                                    act_comp = False
                                                    break
                                            if not act_comp: break
                                        if not act_comp: break
                                    
                                    if act_comp:
                                        h2 = True
    except Exception:
        h2 = False

    # H3: x is an element of X
    try:
        h3 = False
        if hasattr(X, '__iter__'):
            for y in X:
                if x == y:
                    h3 = True
                    break
    except Exception:
        h3 = False

    # neg_Q: The map g*Stab_G(x) |-> g.x is NOT a bijection.
    try:
        neg_q = False
        if h2 and h3:
            G_elements = []
            for g in G:
                if g not in G_elements:
                    G_elements.append(g)
            
            stab = [g for g in G_elements if action(g, x) == x]
            
            cosets_list = []
            for g in G_elements:
                coset = []
                for s in stab:
                    val = op(g, s)
                    if val not in coset:
                        coset.append(val)
                cosets_list.append(coset)
            
            def cosets_equal(c1, c2):
                if len(c1) != len(c2): return False
                for item in c1:
                    if item not in c2: return False
                return True

            # Check injectivity
            for i in range(len(G_elements)):
                for j in range(len(G_elements)):
                    g1 = G_elements[i]
                    g2 = G_elements[j]
                    if action(g1, x) == action(g2, x):
                        if not cosets_equal(cosets_list[i], cosets_list[j]):
                            neg_q = True
                            break
                if neg_q:
                    break
            
            # Check well-definedness
            if not neg_q:
                for i in range(len(G_elements)):
                    for j in range(len(G_elements)):
                        g1 = G_elements[i]
                        g2 = G_elements[j]
                        if cosets_equal(cosets_list[i], cosets_list[j]):
                            if action(g1, x) != action(g2, x):
                                neg_q = True
                                break
                    if neg_q:
                        break
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: X is a set",
    "H_2: G acts on X",
    "H_3: x is an element of X",
    "¬Q: The map g*Stab_G(x) |-> g.x is not a bijection"
]

N_HYP = 3
NEG_Q_INDEX = 3