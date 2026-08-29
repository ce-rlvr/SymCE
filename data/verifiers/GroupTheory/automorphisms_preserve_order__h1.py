import sympy
from sympy.combinatorics import Permutation, PermutationGroup
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
V4 = PermutationGroup(Permutation(0,1)(2,3), Permutation(0,2)(1,3))
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
        G, g, phi = witness
    except Exception:
        return [False, False, False]

    # H1: g is an element of G having finite order n
    try:
        h1 = g in G
        if h1:
            if hasattr(g, 'order'):
                n = g.order()
                h1 = h1 and (n > 0) and (n != float('inf'))
            else:
                ident = g**0
                curr = g
                n = 1
                while curr != ident and n < 10000:
                    curr = curr * g
                    n += 1
                h1 = h1 and (curr == ident)
    except Exception:
        h1 = False

    # H2: phi is an automorphism of G
    try:
        if hasattr(G, 'generate'):
            elements = list(G.generate())
        elif hasattr(G, 'elements'):
            elements = list(G.elements)
        else:
            elements = list(G)
            
        h2 = True
        mapped_elements = []
        for a in elements:
            phi_a = phi[a] if isinstance(phi, dict) else phi(a)
            if phi_a not in G:
                h2 = False
                break
            mapped_elements.append(phi_a)
            
        if h2:
            if len(set(mapped_elements)) != len(elements):
                h2 = False
                
        if h2:
            for a in elements:
                for b in elements:
                    phi_a = phi[a] if isinstance(phi, dict) else phi(a)
                    phi_b = phi[b] if isinstance(phi, dict) else phi(b)
                    phi_ab = phi[a*b] if isinstance(phi, dict) else phi(a*b)
                    if phi_ab != phi_a * phi_b:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False

    # neg_Q: phi(g) does NOT have order exactly n in G
    try:
        phi_g = phi[g] if isinstance(phi, dict) else phi(g)
        
        if hasattr(g, 'order'):
            n = g.order()
        else:
            ident = g**0
            curr = g
            n = 1
            while curr != ident and n < 10000:
                curr = curr * g
                n += 1
                
        if hasattr(phi_g, 'order'):
            phi_n = phi_g.order()
        else:
            ident = phi_g**0
            curr = phi_g
            phi_n = 1
            while curr != ident and phi_n < 10000:
                curr = curr * phi_g
                phi_n += 1
                
        neg_q = (phi_n != n)
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: g is an element of G having finite order n",
    "H_2: phi is an automorphism of G",
    "¬Q: phi(g) does not have order exactly n in G"
]

N_HYP = 2
NEG_Q_INDEX = 2