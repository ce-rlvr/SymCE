import sympy
import sympy.combinatorics
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup
import math
import itertools
import functools

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = DihedralGroup(2)  # Isomorphic to the Klein four-group
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    """
    Check if the witness satisfies the remaining hypotheses and falsifies the conclusion.
    The witness should be a dictionary containing:
      'G': PermutationGroup
      'H': PermutationGroup
      'N': PermutationGroup
      'g': dict or callable mapping G elements to H elements
      's': dict or callable mapping H elements to G elements
    """
    # H_1: There exists a group homomorphism s: H -> G such that g o s = id_H
    # (This implicitly requires g to be a homomorphism from G to H as well)
    try:
        G = witness['G']
        H = witness['H']
        g = witness['g']
        s = witness['s']
        
        G_elements = set(G.elements)
        H_elements = set(H.elements)
        
        h1_ok = True
        
        # Check if s is a homomorphism H -> G
        for h1 in H_elements:
            for h2 in H_elements:
                sh1 = s[h1] if isinstance(s, dict) else s(h1)
                sh2 = s[h2] if isinstance(s, dict) else s(h2)
                sh12 = s[h1*h2] if isinstance(s, dict) else s(h1*h2)
                if sh12 != sh1 * sh2:
                    h1_ok = False
                    break
                if sh1 not in G_elements:
                    h1_ok = False
                    break
            if not h1_ok:
                break
                
        if h1_ok:
            # Check if g is a homomorphism G -> H
            for g1 in G_elements:
                for g2 in G_elements:
                    gg1 = g[g1] if isinstance(g, dict) else g(g1)
                    gg2 = g[g2] if isinstance(g, dict) else g(g2)
                    gg12 = g[g1*g2] if isinstance(g, dict) else g(g1*g2)
                    if gg12 != gg1 * gg2:
                        h1_ok = False
                        break
                    if gg1 not in H_elements:
                        h1_ok = False
                        break
                if not h1_ok:
                    break
                    
        if h1_ok:
            # Check g(s(h)) == h for all h in H
            for h in H_elements:
                sh = s[h] if isinstance(s, dict) else s(h)
                gsh = g[sh] if isinstance(g, dict) else g(sh)
                if gsh != h:
                    h1_ok = False
                    break
    except Exception:
        h1_ok = False

    # ¬Q: G is not isomorphic to a semidirect product of N and H
    try:
        G = witness['G']
        H = witness['H']
        N = witness['N']
        
        order_G = G.order() if callable(getattr(G, 'order', None)) else len(list(G.elements))
        order_N = N.order() if callable(getattr(N, 'order', None)) else len(list(N.elements))
        order_H = H.order() if callable(getattr(H, 'order', None)) else len(list(H.elements))
        
        # If the orders do not match, G cannot be isomorphic to any semidirect product of N and H.
        # This is a safe and fast check. If orders match, we conservatively return False to avoid false positives.
        if order_G != order_N * order_H:
            neg_q_ok = True
        else:
            neg_q_ok = False
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: There exists a group homomorphism s: H -> G such that g o s = id_H",
    "¬Q: G is not isomorphic to a semidirect product of N and H"
]

N_HYP = 1
NEG_Q_INDEX = 1