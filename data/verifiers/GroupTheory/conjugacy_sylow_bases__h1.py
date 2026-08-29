import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.ntheory import factorint
import itertools

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
A5 = AlternatingGroup(5)
S5 = SymmetricGroup(5)

def conditions(witness):
    try:
        # H1: witness is a finite group (must support Sylow subgroups and order)
        if not hasattr(witness, 'sylow_subgroup'):
            return [False, False]
        if not hasattr(witness, 'order'):
            return [False, False]
        order = witness.order()
        if order < 1:
            return [False, False]
        # Prevent timeout on excessively large groups
        if order > 5000:
            return [False, False]
        h1_ok = True
    except Exception:
        return [False, False]

    try:
        G = witness
        if order == 1:
            bases = [[G]]
        else:
            primes = list(factorint(order).keys())
            sylows_by_prime = []
            
            # Find all Sylow p-subgroups for each prime dividing the order
            for p in primes:
                P = G.sylow_subgroup(p)
                P_elements = set(P.elements)
                conjugates = []
                seen = set()
                
                for g in G.elements:
                    # Conjugate the elements to check uniqueness
                    H_elements = frozenset(~g * x * g for x in P_elements)
                    if H_elements not in seen:
                        seen.add(H_elements)
                        # Create the conjugated subgroup
                        gens = [~g * h * g for h in P.generators]
                        H = PermutationGroup(gens)
                        conjugates.append((H, H_elements))
                sylows_by_prime.append(conjugates)
                
            # A Sylow basis is a choice of one Sylow p-subgroup for each prime such that any two permute
            bases = []
            for combo in itertools.product(*sylows_by_prime):
                ok = True
                for i in range(len(combo)):
                    for j in range(i + 1, len(combo)):
                        A_elems = combo[i][1]
                        B_elems = combo[j][1]
                        # Two subgroups A and B permute iff the set AB equals the set BA
                        AB = {a * b for a in A_elems for b in B_elems}
                        BA = {b * a for a in A_elems for b in B_elems}
                        if AB != BA:
                            ok = False
                            break
                    if not ok:
                        break
                if ok:
                    bases.append([H for H, H_elems in combo])
                    
        # Check the negated conclusion:
        # The conclusion fails if there are NO Sylow bases (vacuously false in existential interpretation)
        # OR if there exist two Sylow bases that are NOT conjugate.
        if not bases:
            neg_q_ok = True
        else:
            neg_q_ok = False
            for i in range(len(bases)):
                for j in range(i + 1, len(bases)):
                    b1 = bases[i]
                    b2 = bases[j]
                    b2_elements = [set(H.elements) for H in b2]
                    
                    are_conj = False
                    for g in G.elements:
                        match = True
                        for k in range(len(b1)):
                            H_g = { ~g * x * g for x in b1[k].elements }
                            if H_g != b2_elements[k]:
                                match = False
                                break
                        if match:
                            are_conj = True
                            break
                            
                    if not are_conj:
                        neg_q_ok = True
                        break
                if neg_q_ok:
                    break
                    
    except Exception:
        neg_q_ok = False

    return [h1_ok, neg_q_ok]

CONDITION_LABELS = [
    "H_1: G is a finite group",
    "¬Q: There exist two Sylow bases of G that are not conjugate, or G has no Sylow bases"
]
N_HYP = 1
NEG_Q_INDEX = 1