import sympy
from sympy.combinatorics import PermutationGroup, SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
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

N_HYP = 4
NEG_Q_INDEX = 4

CONDITION_LABELS = [
    "H_1: K is a finite Galois extension of F",
    "H_2: G is the Galois group Gal(K/F)",
    "H_3: G' is the commutator subgroup of G",
    "H_4: E is the fixed field of G' in K",
    "¬Q: E is not a normal extension of F, or some intermediate abelian extension L is not contained in E"
]

def conditions(witness):
    try:
        if not isinstance(witness, PermutationGroup):
            return [False, False, False, False, False]
        
        # The witness is the Galois group G. 
        # The hypotheses establish the standard Galois correspondence setup.
        h1 = True
        h2 = True
        h3 = True
        h4 = True
        
        G = witness
        G_prime = G.derived_subgroup()
        
        # Check if E is a normal extension of F, which corresponds to G' being a normal subgroup of G.
        E_is_normal = True
        for g in G.generators:
            for h in G_prime.generators:
                if (g**-1 * h * g) not in G_prime:
                    E_is_normal = False
                    break
            if not E_is_normal:
                break
                
        # Check if any intermediate field L that is an abelian extension of F is contained in E.
        # This corresponds to checking if for every normal subgroup H of G such that G/H is abelian, G' is a subgroup of H.
        all_contained = True
        for H in G.normal_subgroups():
            is_abelian_quotient = True
            for g1 in G.generators:
                for g2 in G.generators:
                    comm = g1**-1 * g2**-1 * g1 * g2
                    if comm not in H:
                        is_abelian_quotient = False
                        break
                if not is_abelian_quotient:
                    break
            
            if is_abelian_quotient:
                for gen in G_prime.generators:
                    if gen not in H:
                        all_contained = False
                        break
            if not all_contained:
                break
                
        Q = E_is_normal and all_contained
        neg_Q = not Q
        
        return [h1, h2, h3, h4, neg_Q]
    except Exception:
        return [False, False, False, False, False]