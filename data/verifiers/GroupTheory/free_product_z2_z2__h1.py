import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup
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

def conditions(witness):
    try:
        if isinstance(witness, dict):
            G1 = witness.get('G1', witness.get('G_1'))
            G2 = witness.get('G2', witness.get('G_2'))
            G = witness.get('G')
        elif isinstance(witness, (list, tuple)) and len(witness) == 3:
            G1, G2, G = witness
        else:
            return [False, False, False]
            
        if G1 is None or G2 is None or G is None:
            return [False, False, False]
    except Exception:
        return [False, False, False]

    def check_H1():
        try:
            # Fast path for FpGroup C2 to avoid hanging on infinite groups
            if hasattr(G2, 'generators') and hasattr(G2, 'relators'):
                if len(G2.generators) == 1 and len(G2.relators) == 1:
                    if len(G2.relators[0]) == 2:
                        return True
            
            # Check abelian invariants first as a safe necessary condition
            if hasattr(G2, 'abelian_invariants'):
                inv = list(G2.abelian_invariants())
                if inv != [2]:
                    return False
                    
            if hasattr(G2, 'order'):
                return G2.order() == 2
            elif hasattr(G2, 'elements'):
                return len(list(G2.elements)) == 2
            return False
        except Exception:
            return False

    def check_H2():
        try:
            # Syntactic check for FpGroup construction
            if hasattr(G1, 'generators') and hasattr(G2, 'generators') and hasattr(G, 'generators'):
                if hasattr(G1, 'relators') and hasattr(G2, 'relators') and hasattr(G, 'relators'):
                    if len(G.generators) == len(G1.generators) + len(G2.generators):
                        if len(G.relators) == len(G1.relators) + len(G2.relators):
                            return True
                            
            # Semantic check for trivial G1 (e.g., using PermutationGroups)
            def get_order(grp):
                if hasattr(grp, 'generators') and hasattr(grp, 'relators'):
                    return None # Avoid calling order() on FpGroup to prevent hanging
                if hasattr(grp, 'order'):
                    return grp.order()
                if hasattr(grp, 'elements'):
                    return len(list(grp.elements))
                return None
                
            o1 = get_order(G1)
            o2 = get_order(G2)
            og = get_order(G)
            if o1 == 1 and o2 == 2 and og == 2:
                return True
                
            return False
        except Exception:
            return False

    def check_neg_Q():
        try:
            # If G is not an FpGroup, we can safely check its order
            if not (hasattr(G, 'generators') and hasattr(G, 'relators')):
                if hasattr(G, 'order'):
                    o = G.order()
                    if o != sympy.oo:
                        return True
                elif hasattr(G, 'elements'):
                    return True
                    
            # For FpGroups (and others), abelian invariants are safe and fast to compute.
            # The infinite dihedral group has abelian invariants [2, 2].
            if hasattr(G, 'abelian_invariants'):
                inv = list(G.abelian_invariants())
                if inv != [2, 2]:
                    return True
                return False
                
            return False
        except Exception:
            return False

    return [check_H1(), check_H2(), check_neg_Q()]

CONDITION_LABELS = [
    "H_1: G_2 is a cyclic group of order 2",
    "H_2: G is the free product G_1 * G_2",
    "¬Q: G is not isomorphic to the infinite dihedral group"
]

N_HYP = 2
NEG_Q_INDEX = 2