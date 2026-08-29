import sympy
from sympy.combinatorics.free_groups import free_group, FreeGroupElement
from sympy.combinatorics.fp_groups import FpGroup, FpSubgroup
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for standard groups
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
    """
    witness is expected to be a tuple: (G, H_gens, T)
    where:
      - G is an FpGroup
      - H_gens is a list of FreeGroupElement (generators for subgroup H)
      - T is a list of FreeGroupElement (the right Schreier transversal)
    """
    try:
        G, H_gens, T = witness
    except Exception:
        return [False, False, False]
        
    # H_1: G is a group with presentation < X | R >
    try:
        h1 = isinstance(G, FpGroup)
    except Exception:
        h1 = False
        
    # H_2: T is a right Schreier transversal for H in G
    try:
        h2 = True
        H = FpSubgroup(G, H_gens)
        
        # T must contain the identity
        if G.free_group.identity not in T:
            h2 = False
            
        # T must be prefix-closed (Schreier property)
        if h2:
            for t in T:
                prefixes = [G.free_group.identity]
                current = G.free_group.identity
                for gen, exp in t.array_form:
                    step = 1 if exp > 0 else -1
                    for _ in range(abs(exp)):
                        current = current * (gen**step)
                        prefixes.append(current)
                
                for p in prefixes:
                    if p not in T:
                        h2 = False
                        break
                if not h2:
                    break
                    
        # Elements of T must be in distinct right cosets of H
        if h2:
            for i in range(len(T)):
                for j in range(i+1, len(T)):
                    if T[i] * T[j]**-1 in H:
                        h2 = False
                        break
                if not h2:
                    break
                    
        # T must cover all right cosets of H
        if h2:
            for t in T:
                for x in G.free_group.generators:
                    tx = t * x
                    found = False
                    for tp in T:
                        if tx * tp**-1 in H:
                            found = True
                            break
                    if not found:
                        h2 = False
                        break
                if not h2:
                    break
    except Exception:
        h2 = False
        
    # neg_Q: The conclusion fails at the witness
    try:
        neg_q = False
        if h1 and h2:
            X = G.free_group.generators
            R = G.relators
            
            # Construct the Schreier generating set S
            S = set()
            for t in T:
                for x in X:
                    tx = t * x
                    rep = None
                    for tp in T:
                        if tx * tp**-1 in H:
                            rep = tp
                            break
                    if rep is not None:
                        s = t * x * rep**-1
                        if len(s) > 0:  # exclude identity
                            S.add(s)
                            
            # Construct the relation set R_H as given in the false conjecture
            R_H = set()
            for t in T:
                for r in R:
                    rel = t * r * t**-1
                    if len(rel) > 0:
                        R_H.add(rel)
                        
            # The conjecture omits the Reidemeister rewriting process (\tau).
            # Without \tau, R_H consists of words over the original alphabet X.
            # For < S | R_H > to be a valid presentation, R_H must be words over the alphabet S.
            # We check if R_H contains any symbols from X that are not in S.
            invalid = False
            for rel in R_H:
                for gen, exp in rel.array_form:
                    if gen not in S and gen**-1 not in S:
                        invalid = True
                        break
                if invalid:
                    break
                    
            if invalid:
                neg_q = True
            else:
                neg_q = False
    except Exception:
        neg_q = False
        
    return [h1, h2, neg_q]

CONDITION_LABELS = [
    "H_1: G is a group with presentation < X | R >",
    "H_2: T is a right Schreier transversal for H in G",
    "¬Q: The relation set R_H is not a valid set of words over S (missing Reidemeister rewriting)"
]

N_HYP = 2
NEG_Q_INDEX = 2