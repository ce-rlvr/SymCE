import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup: named object bindings
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness) -> list[bool]:
    # Unpack witness
    try:
        if isinstance(witness, dict):
            G = witness['G']
            H = witness['H']
            A = witness['A']
            B = witness['B']
            phi = witness['phi']
        else:
            G, H, A, B, phi = witness
    except Exception:
        return [False, False, False, False]

    # Convert callable phi to dict if necessary
    try:
        if callable(phi) and hasattr(G, 'generate'):
            phi = {g: phi(g) for g in list(G.generate())}
    except Exception:
        pass

    # H_1: G and H are groups
    try:
        h1 = isinstance(G, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H_2: A and B are subgroups of G
    try:
        def is_subgroup(sub, grp):
            if hasattr(sub, 'generate'):
                elements = list(sub.generate())
            else:
                elements = list(sub)
            
            grp_elements = list(grp.generate())
            
            # Check subset
            if not all(e in grp_elements for e in elements):
                return False
            if not elements:
                return False
            
            # Check identity
            if grp.identity not in elements:
                return False
                
            # Check closure
            for x in elements:
                for y in elements:
                    if x * y not in elements:
                        return False
                        
            # Check inverse
            for x in elements:
                if x**-1 not in elements:
                    return False
                    
            return True
        
        h2 = is_subgroup(A, G) and is_subgroup(B, G)
    except Exception:
        h2 = False

    # H_3: phi is a function from G to H
    try:
        if isinstance(phi, dict):
            g_elements = list(G.generate())
            h_elements = list(H.generate())
            h3 = all(g in phi for g in g_elements) and all(phi[g] in h_elements for g in g_elements)
        else:
            h3 = False
    except Exception:
        h3 = False

    # ¬Q: phi(AB) != phi(A)phi(B)
    try:
        if hasattr(A, 'generate'):
            A_elems = list(A.generate())
        else:
            A_elems = list(A)
            
        if hasattr(B, 'generate'):
            B_elems = list(B.generate())
        else:
            B_elems = list(B)
            
        # Compute AB
        AB = set()
        for a in A_elems:
            for b in B_elems:
                AB.add(a * b)
                
        # Compute phi(AB)
        phi_AB = set(phi[x] for x in AB)
        
        # Compute phi(A) and phi(B)
        phi_A = set(phi[a] for a in A_elems)
        phi_B = set(phi[b] for b in B_elems)
        
        # Compute phi(A)phi(B)
        phi_A_phi_B = set()
        for pa in phi_A:
            for pb in phi_B:
                phi_A_phi_B.add(pa * pb)
                
        neg_q = phi_AB != phi_A_phi_B
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G and H are groups",
    "H_2: A and B are subgroups of G",
    "H_3: phi is a function from G to H",
    "¬Q: phi(AB) != phi(A)phi(B)"
]

N_HYP = 3
NEG_Q_INDEX = 3