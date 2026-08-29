import sympy
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup, AbelianGroup
)
from sympy.matrices import eye, zeros

# Top-level setup: named object bindings
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
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def is_torsion_free(G):
    """Helper to determine if a group or object is torsion-free."""
    # 1. Check for explicit attribute/method (useful for mock witnesses)
    if hasattr(G, 'is_torsion_free'):
        val = G.is_torsion_free
        return val() if callable(val) else bool(val)
        
    # 2. If it's a tuple, treat it as a direct product
    if isinstance(G, tuple):
        return all(is_torsion_free(g) for g in G)
        
    # 3. Check if it's a SymPy PermutationGroup (or similar finite group)
    if hasattr(G, 'elements') and hasattr(G, 'identity'):
        for g in G.elements:
            if g != G.identity:
                o = g.order() if callable(g.order) else g.order
                if o != float('inf'):
                    return False
        return True
        
    # 4. Check if it's a SymPy FreeGroup (always torsion-free)
    from sympy.combinatorics.free_groups import FreeGroup
    if isinstance(G, FreeGroup):
        return True
        
    # 5. Check if it's a SymPy FpGroup
    from sympy.combinatorics.fp_groups import FpGroup
    if isinstance(G, FpGroup):
        if len(G.relators) == 0:
            return True
            
    # 6. Integer representation (0 is Z, 1 is trivial, >1 is Z_n)
    if isinstance(G, int):
        return G == 0 or G == 1
        
    # 7. Fallback to checking group order
    if hasattr(G, 'order'):
        o = G.order() if callable(G.order) else G.order
        if o == 1:
            return True
        elif o != float('inf'):
            return False
            
    raise ValueError(f"Cannot determine if {G} is torsion-free")

def direct_product(G, H):
    """Helper to compute the direct product of two groups."""
    from sympy.combinatorics import PermutationGroup
    if isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup):
        return G * H
        
    if hasattr(G, 'direct_product'):
        return G.direct_product(H)
        
    if hasattr(G, '__mul__') and not isinstance(G, (int, float, str, tuple, list)):
        try:
            return G * H
        except Exception:
            pass
            
    # Fallback representation of direct product
    return (G, H)

def conditions(witness) -> list[bool]:
    try:
        if len(witness) != 2:
            return [False, False, False]
        G, H = witness
    except Exception:
        return [False, False, False]
        
    try:
        h1_ok = is_torsion_free(G)
    except Exception:
        h1_ok = False
        
    try:
        h2_ok = is_torsion_free(H)
    except Exception:
        h2_ok = False
        
    try:
        GxH = direct_product(G, H)
        neg_q_ok = not is_torsion_free(GxH)
    except Exception:
        neg_q_ok = False
        
    return [h1_ok, h2_ok, neg_q_ok]

CONDITION_LABELS: list[str] = [
    "H_1: G is torsion-free",
    "H_2: H is torsion-free",
    "¬Q: G x H is not a torsion-free group"
]

N_HYP: int = 2
NEG_Q_INDEX: int = 2