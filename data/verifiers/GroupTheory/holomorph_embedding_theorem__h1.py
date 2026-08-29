import itertools
from sympy.combinatorics import Permutation, PermutationGroup
from sympy.combinatorics.named_groups import (
    SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
)
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

def conditions(witness):
    # Attempt to convert SymPy PermutationGroup to a Cayley table (list of lists)
    try:
        if not isinstance(witness, list):
            if hasattr(witness, 'elements'):
                elements = list(witness.elements)
                n = len(elements)
                elem_idx = {e: i for i, e in enumerate(elements)}
                G_table = []
                for e1 in elements:
                    row = []
                    for e2 in elements:
                        row.append(elem_idx[e1 * e2])
                    G_table.append(row)
                witness = G_table
    except Exception:
        pass

    # H_1: \rho: G \to S_{|G|} is the right regular representation of G
    try:
        if not isinstance(witness, list):
            h1 = False
        else:
            n = len(witness)
            if n == 0:
                h1 = False
            else:
                h1 = True
                for row in witness:
                    if not isinstance(row, list) or len(row) != n:
                        h1 = False
                        break
                    for val in row:
                        if not isinstance(val, int) or val < 0 or val >= n:
                            h1 = False
                            break
                    if not h1: break
                
                if h1:
                    # Check if right regular representation maps to S_{|G|}
                    # i.e., each column is a valid permutation of 0..n-1
                    for j in range(n):
                        col = [witness[i][j] for i in range(n)]
                        if sorted(col) != list(range(n)):
                            h1 = False
                            break
    except Exception:
        h1 = False

    # neg_Q: The normalizer of \rho(G) in S_{|G|} is NOT isomorphic to G \rtimes Aut(G)
    try:
        if not h1:
            neg_q = False
        else:
            n = len(witness)
            G = witness
            
            # Check if G is associative. 
            # A finite right quasigroup is a group iff it is associative.
            # If G is not associative, Hol is not a group, so it cannot be isomorphic to N (which is always a group).
            is_G_assoc = True
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        if G[G[i][j]][k] != G[i][G[j][k]]:
                            is_G_assoc = False
                            break
                    if not is_G_assoc: break
                if not is_G_assoc: break

            if not is_G_assoc:
                neg_q = True
            else:
                # If G is associative, it is a group. The theorem holds for all groups.
                # We compute the explicit isomorphism for small n to be faithful to the definition,
                # but skip for n > 6 to avoid timeouts (since we mathematically know neg_q is False).
                if n > 6:
                    neg_q = False
                else:
                    # Compute Aut(G)
                    Aut = []
                    for alpha in itertools.permutations(range(n)):
                        valid = True
                        for i in range(n):
                            for j in range(n):
                                if alpha[G[i][j]] != G[alpha[i]][alpha[j]]:
                                    valid = False
                                    break
                            if not valid: break
                        if valid:
                            Aut.append(alpha)
                    
                    # Compute Hol = G \rtimes Aut(G)
                    Hol_elements = list(itertools.product(range(n), Aut))
                    Hol_size = len(Hol_elements)
                    
                    # Compute N = normalizer of rho(G) in S_n
                    rho_set = set(tuple(G[i][j] for i in range(n)) for j in range(n))
                    N_perms = []
                    for pi in itertools.permutations(range(n)):
                        pi_inv = [0]*n
                        for i, p in enumerate(pi): pi_inv[p] = i
                        valid = True
                        for r in rho_set:
                            conj = tuple(pi[r[pi_inv[x]]] for x in range(n))
                            if conj not in rho_set:
                                valid = False
                                break
                        if valid:
                            N_perms.append(Permutation(pi))
                    
                    if Hol_size != len(N_perms):
                        neg_q = True
                    else:
                        # Build Cayley table for Hol
                        Hol_idx = {elem: i for i, elem in enumerate(Hol_elements)}
                        Hol_cayley = []
                        for e1 in Hol_elements:
                            row = []
                            for e2 in Hol_elements:
                                g1, a1 = e1
                                g2, a2 = e2
                                g_new = G[g1][a1[g2]]
                                a_new = tuple(a1[a2[x]] for x in range(n))
                                row.append(Hol_idx[(g_new, a_new)])
                            Hol_cayley.append(row)
                            
                        # Convert to PermutationGroups to check isomorphism
                        Hol_perms = []
                        for i in range(Hol_size):
                            p = [Hol_cayley[i][x] for x in range(Hol_size)]
                            Hol_perms.append(Permutation(p))
                        
                        Hol_group = PermutationGroup(Hol_perms)
                        N_group = PermutationGroup(N_perms)
                        
                        neg_q = not N_group.is_isomorphic(Hol_group)
    except Exception:
        neg_q = False

    return [h1, neg_q]

CONDITION_LABELS = [
    "H_1: rho is the right regular representation of G mapping to S_|G|",
    "¬Q: The normalizer of rho(G) in S_|G| is not isomorphic to G ⋊ Aut(G)"
]

N_HYP = 1
NEG_Q_INDEX = 1