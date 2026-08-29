import sympy
import math
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.homomorphisms import GroupHomomorphism
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
    """
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a tuple (G, H, phi).
    """
    try:
        G, H, phi = witness
    except Exception:
        return [False, False, False, False]
        
    # H_1: H is a finite group
    try:
        # In SymPy, PermutationGroup instances are finite groups.
        h_finite = isinstance(H, PermutationGroup)
    except Exception:
        h_finite = False
        
    # H_2: The orders of G and H are coprime, meaning \gcd(|G|, |H|) = 1
    try:
        if hasattr(G, 'order'):
            g_order = G.order()
        elif hasattr(G, 'generate'):
            g_order = len(list(G.generate()))
        elif hasattr(G, 'elements'):
            g_order = len(G.elements)
        else:
            g_order = len(G)
            
        h_order = H.order()
        coprime = math.gcd(int(g_order), int(h_order)) == 1
    except Exception:
        coprime = False
        
    # H_3: \phi: G \to H is a group homomorphism
    try:
        is_hom = True
        if isinstance(phi, GroupHomomorphism):
            if phi.domain != G or phi.codomain != H:
                is_hom = False
        else:
            if hasattr(G, 'generate'):
                elements = list(G.generate())
            elif hasattr(G, 'elements'):
                elements = G.elements
            else:
                elements = list(G)
                
            if hasattr(G, 'op'):
                op_G = G.op
            elif hasattr(G, 'mul'):
                op_G = G.mul
            else:
                op_G = lambda x, y: x * y
                
            if isinstance(phi, dict):
                def phi_func(x): return phi[x]
            else:
                phi_func = phi
                
            for x in elements:
                if phi_func(x) not in H:
                    is_hom = False
                    break
                for y in elements:
                    xy = op_G(x, y)
                    if xy not in elements:
                        is_hom = False
                        break
                    if phi_func(xy) != phi_func(x) * phi_func(y):
                        is_hom = False
                        break
                if not is_hom:
                    break
    except Exception:
        is_hom = False
        
    # ¬Q: \phi is not the trivial homomorphism
    try:
        if isinstance(phi, GroupHomomorphism):
            is_trivial = phi.is_trivial()
        else:
            is_trivial = True
            id_H = H.identity
            
            if hasattr(G, 'generate'):
                elements = list(G.generate())
            elif hasattr(G, 'elements'):
                elements = G.elements
            else:
                elements = list(G)
                
            if isinstance(phi, dict):
                def phi_func(x): return phi[x]
            else:
                phi_func = phi
                
            for x in elements:
                if phi_func(x) != id_H:
                    is_trivial = False
                    break
    except Exception:
        is_trivial = False
        
    return [bool(h_finite), bool(coprime), bool(is_hom), not bool(is_trivial)]

CONDITION_LABELS = [
    "H_1: H is a finite group",
    "H_2: The orders of G and H are coprime",
    "H_3: phi is a group homomorphism",
    "¬Q: phi is not the trivial homomorphism"
]

N_HYP = 3
NEG_Q_INDEX = 3