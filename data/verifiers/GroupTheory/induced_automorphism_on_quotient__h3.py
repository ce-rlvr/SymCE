import sympy
from sympy.combinatorics import PermutationGroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros

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
O2 = zeros(2,2)
O3 = zeros(3,3)

def conditions(witness):
    try:
        G, N, phi = witness
    except Exception:
        return [False, False, False, False]
        
    # H1: G is a group
    try:
        h1 = isinstance(G, PermutationGroup)
    except Exception:
        h1 = False
        
    # H2: N is a normal subgroup of G
    try:
        h2 = isinstance(N, PermutationGroup) and N.is_subgroup(G) and N.is_normal(G)
    except Exception:
        h2 = False
        
    # H3: \phi(N) = N
    try:
        try:
            N_set = set(N.elements)
        except AttributeError:
            N_set = set(N.generate())
        phi_N = set()
        for n in N_set:
            pn = phi(n) if callable(phi) else phi[n]
            phi_N.add(pn)
        h3 = (phi_N == N_set)
    except Exception:
        h3 = False
        
    # neg_Q: \bar{\phi} is NOT a well-defined automorphism of G/N
    try:
        try:
            G_set = set(G.elements)
        except AttributeError:
            G_set = set(G.generate())
            
        try:
            N_set = set(N.elements)
        except AttributeError:
            N_set = set(N.generate())
            
        is_well_defined = True
        is_homomorphism = True
        is_injective = True
        is_surjective = True
        
        for g in G_set:
            try:
                pg = phi(g) if callable(phi) else phi[g]
                if pg not in G_set:
                    is_well_defined = False
            except Exception:
                is_well_defined = False
                
            if not is_well_defined:
                break
                
            # Check well-defined
            for n in N_set:
                try:
                    gn = g * n
                    pgn = phi(gn) if callable(phi) else phi[gn]
                    if (~pg * pgn) not in N_set:
                        is_well_defined = False
                        break
                except Exception:
                    is_well_defined = False
                    break
            if not is_well_defined:
                break
                
            # Check homomorphism
            for g2 in G_set:
                try:
                    pg2 = phi(g2) if callable(phi) else phi[g2]
                    gg2 = g * g2
                    pgg2 = phi(gg2) if callable(phi) else phi[gg2]
                    if (~(pg * pg2) * pgg2) not in N_set:
                        is_homomorphism = False
                        break
                except Exception:
                    is_homomorphism = False
                    break
            if not is_homomorphism:
                break
                
            # Check injective
            try:
                if pg in N_set and g not in N_set:
                    is_injective = False
            except Exception:
                is_injective = False
            if not is_injective:
                break
                
        # Check surjective
        if is_well_defined and is_homomorphism and is_injective:
            for g in G_set:
                found = False
                for h in G_set:
                    try:
                        ph = phi(h) if callable(phi) else phi[h]
                        if (~g * ph) in N_set:
                            found = True
                            break
                    except Exception:
                        pass
                if not found:
                    is_surjective = False
                    break
                    
        neg_q = not (is_well_defined and is_homomorphism and is_injective and is_surjective)
    except Exception:
        neg_q = False
        
    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group",
    "H_2: N is a normal subgroup of G",
    "H_3: phi(N) = N",
    "¬Q: bar{phi} is not a well-defined automorphism of G/N"
]

N_HYP = 3
NEG_Q_INDEX = 3