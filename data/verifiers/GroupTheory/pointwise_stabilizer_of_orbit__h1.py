import sympy
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools

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

I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    try:
        if isinstance(witness, dict):
            G = witness.get('G')
            X = witness.get('X')
            action = witness.get('action')
            x = witness.get('x')
            O_x = witness.get('O_x')
        else:
            G, X, action, x, O_x = witness
    except Exception:
        return [False, False, False]

    # H_1: x is an element of X
    try:
        h1 = x in X
    except Exception:
        h1 = False

    # Extract elements of G safely
    try:
        if hasattr(G, 'elements'):
            raw_G = list(G.elements)
        elif hasattr(G, 'generate'):
            raw_G = list(G.generate())
        else:
            raw_G = list(G)
            
        G_elements = []
        for g in raw_G:
            if g not in G_elements:
                G_elements.append(g)
    except Exception:
        return [h1, False, False]

    def act(g, y):
        if callable(action):
            return action(g, y)
        else:
            return action[(g, y)]

    # H_2: O_x is the orbit of x under G
    try:
        orbit = []
        for g in G_elements:
            val = act(g, x)
            if val not in orbit:
                orbit.append(val)
        
        O_x_list = list(O_x)
        h2 = True
        for val in orbit:
            if val not in O_x_list:
                h2 = False
                break
        if h2:
            for val in O_x_list:
                if val not in orbit:
                    h2 = False
                    break
    except Exception:
        h2 = False

    # ¬Q: The pointwise stabilizer of O_x in G is NOT the normal core of G_x in G
    try:
        # Pointwise stabilizer of O_x in G
        pt_stab = []
        for g in G_elements:
            if all(act(g, y) == y for y in O_x_list):
                if g not in pt_stab:
                    pt_stab.append(g)
        
        # G_x (Stabilizer of x)
        G_x = []
        for g in G_elements:
            if act(g, x) == x:
                if g not in G_x:
                    G_x.append(g)
        
        # Normal core of G_x in G: \bigcap_{g \in G} g G_x g^{-1}
        normal_core = None
        for g in G_elements:
            if isinstance(g, (int, float, complex, sympy.Integer, sympy.Rational, sympy.Float)):
                g_inv = -g
                op = '+'
            else:
                try:
                    g_inv = g**-1
                    op = '*'
                except Exception:
                    try:
                        g_inv = g.inv()
                        op = '*'
                    except Exception:
                        try:
                            g_inv = ~g
                            op = '*'
                        except Exception:
                            g_inv = -g
                            op = '+'
            
            conj = []
            for h in G_x:
                try:
                    if op == '*':
                        val = g * h * g_inv
                    else:
                        val = g + h + g_inv
                except Exception:
                    if op == '*':
                        val = g + h + g_inv
                    else:
                        val = g * h * g_inv
                        
                if val not in conj:
                    conj.append(val)
                
            if normal_core is None:
                normal_core = conj
            else:
                normal_core = [elem for elem in normal_core if elem in conj]
                
        if normal_core is None:
            normal_core = []
            
        # Check if pointwise stabilizer equals normal core
        if len(pt_stab) != len(normal_core):
            neg_q = True
        else:
            neg_q = False
            for elem in pt_stab:
                if elem not in normal_core:
                    neg_q = True
                    break
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: x is an element of X",
    "H_2: O_x is the orbit of x under G",
    "¬Q: The pointwise stabilizer of O_x in G is not the normal core of G_x in G"
]

N_HYP = 2
NEG_Q_INDEX = 2