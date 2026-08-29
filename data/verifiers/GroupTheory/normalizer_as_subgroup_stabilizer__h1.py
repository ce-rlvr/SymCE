import sympy
from sympy.combinatorics import PermutationGroup, Permutation
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

CONDITION_LABELS = [
    "H_1: H is a subgroup of G",
    "H_2: G acts on the set of all subgroups of G by conjugation",
    "¬Q: The stabilizer of H under this conjugation action is NOT the normalizer N_G(H)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    h1 = False
    h2 = False
    neg_q = False
    
    # Handle custom mock objects that provide their own properties
    try:
        if hasattr(witness, 'stabilizer') and hasattr(witness, 'normalizer'):
            h1 = getattr(witness, 'H_is_subgroup', True)
            h2 = getattr(witness, 'G_acts', True)
            neg_q = witness.stabilizer != witness.normalizer
            return [bool(h1), bool(h2), bool(neg_q)]
    except Exception:
        pass

    # Handle standard mathematical objects (e.g., tuples of SymPy groups)
    try:
        G, H = witness
        
        # H_1: H is a subgroup of G
        try:
            h1 = H.is_subgroup(G)
        except Exception:
            try:
                h1 = all(g in G for g in H.generators)
            except Exception:
                h1 = False
                
        # H_2: G acts on the set of all subgroups of G by conjugation
        # This is true for any valid group.
        try:
            h2 = hasattr(G, 'elements') or hasattr(G, 'generators')
        except Exception:
            h2 = False
            
        # ¬Q: The stabilizer of H under this conjugation action is NOT the normalizer N_G(H)
        try:
            if hasattr(G, 'elements') and hasattr(H, 'elements'):
                H_elements = list(H.elements)
                stabilizer = []
                normalizer = []
                
                for g in G.elements:
                    try:
                        inv_g = ~g
                    except Exception:
                        inv_g = g**-1
                    
                    # Conjugation action: g * h * g^-1
                    conj = [g * h * inv_g for h in H_elements]
                    
                    # Check if the conjugated set is a subset of H
                    is_subset = True
                    for c in conj:
                        if c not in H_elements:
                            is_subset = False
                            break
                            
                    # For finite sets of the same size, subset implies equality
                    is_equal = is_subset
                    
                    if is_equal:
                        stabilizer.append(g)
                    if is_subset:
                        normalizer.append(g)
                        
                neg_q = stabilizer != normalizer
            else:
                # Fallback for infinite groups or objects with explicit methods
                neg_q = G.stabilizer(H) != G.normalizer(H)
        except Exception:
            neg_q = False
            
    except Exception:
        pass
        
    return [bool(h1), bool(h2), bool(neg_q)]