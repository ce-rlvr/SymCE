import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import itertools
from math import gcd
from functools import reduce

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
I2 = eye(2)
I3 = eye(3)
O2 = zeros(2, 2)
O3 = zeros(3, 3)

def conditions(witness) -> list[bool]:
    def get_snf_diagonal(gens, rels):
        n = len(gens)
        if not rels:
            return [0] * n
        matrix = [[int(rel.get(g, 0)) for g in gens] for rel in rels]
        M = sympy.Matrix(matrix)
        
        diag = []
        prev_gcd = 1
        for k in range(1, min(M.rows, M.cols) + 1):
            minors = []
            for rows in itertools.combinations(range(M.rows), k):
                for cols in itertools.combinations(range(M.cols), k):
                    subM = M[list(rows), list(cols)]
                    minors.append(abs(int(subM.det())))
            k_gcd = reduce(gcd, minors)
            if k_gcd == 0:
                diag.extend([0] * (min(M.rows, M.cols) - k + 1))
                break
            diag.append(k_gcd // prev_gcd)
            prev_gcd = k_gcd
            
        while len(diag) < n:
            diag.append(0)
        return diag

    def group_size(gens, rels):
        snf = get_snf_diagonal(gens, rels)
        if 0 in snf:
            return 0
        size = 1
        for x in snf:
            size *= x
        return size

    def is_zero(element, gens, rels):
        snf_orig = get_snf_diagonal(gens, rels)
        snf_new = get_snf_diagonal(gens, rels + [element])
        return snf_orig == snf_new

    def is_injective(phi, A_gens, A_rels, G_gens, G_rels):
        size_A = group_size(A_gens, A_rels)
        if size_A == 0:
            return False
        
        size_G = group_size(G_gens, G_rels)
        if size_G == 0:
            return False
            
        for rel in A_rels:
            image = {}
            for a, exp in rel.items():
                if a in phi:
                    for g, exp2 in phi[a].items():
                        image[g] = image.get(g, 0) + exp * exp2
            if not is_zero(image, G_gens, G_rels):
                return False
                
        im_gens_rels = list(G_rels)
        for a in A_gens:
            if a in phi:
                im_gens_rels.append(phi[a])
                
        size_G_mod_im = group_size(G_gens, im_gens_rels)
        if size_G_mod_im == 0:
            return False
            
        size_im = size_G // size_G_mod_im
        return size_im == size_A

    def check_well_formed(group):
        gens = set(group['gens'])
        for rel in group['rels']:
            if not set(rel.keys()).issubset(gens):
                return False
        return True

    def check_phi_well_formed(phi, A_gens, G_gens):
        G_gens_set = set(G_gens)
        for a, image in phi.items():
            if a not in A_gens:
                return False
            if not set(image.keys()).issubset(G_gens_set):
                return False
        return True

    try:
        G1 = witness['G1']
        G2 = witness['G2']
        A = witness['A']
        phi1 = witness['phi1']
        phi2 = witness['phi2']
        
        h1 = isinstance(G1, dict) and 'gens' in G1 and 'rels' in G1 and check_well_formed(G1) and \
             isinstance(G2, dict) and 'gens' in G2 and 'rels' in G2 and check_well_formed(G2)
    except Exception:
        h1 = False

    try:
        h2 = isinstance(A, dict) and 'gens' in A and 'rels' in A and check_well_formed(A)
    except Exception:
        h2 = False

    try:
        h3_1 = check_phi_well_formed(phi1, A['gens'], G1['gens']) and is_injective(phi1, A['gens'], A['rels'], G1['gens'], G1['rels'])
        h3_2 = check_phi_well_formed(phi2, A['gens'], G2['gens']) and is_injective(phi2, A['gens'], A['rels'], G2['gens'], G2['rels'])
        h3 = h3_1 and h3_2
    except Exception:
        h3 = False

    try:
        # Compute abelianization of the presentation given in the conclusion
        gens_conc = sorted(list(set(G1['gens'] + G2['gens'])))
        rels_conc = list(G1['rels']) + list(G2['rels'])
        for a in A['gens']:
            rel = {}
            for g, exp in phi1.get(a, {}).items():
                rel[g] = rel.get(g, 0) + exp
            for g, exp in phi2.get(a, {}).items():
                rel[g] = rel.get(g, 0) - exp
            rels_conc.append(rel)
            
        snf_conc = get_snf_diagonal(gens_conc, rels_conc)
        
        # Compute abelianization of the ACTUAL amalgamated free product
        gens_actual = [f"{g}_1" for g in G1['gens']] + [f"{g}_2" for g in G2['gens']]
        rels_actual = []
        for rel in G1['rels']:
            rels_actual.append({f"{g}_1": exp for g, exp in rel.items()})
        for rel in G2['rels']:
            rels_actual.append({f"{g}_2": exp for g, exp in rel.items()})
            
        for a in A['gens']:
            rel = {}
            for g, exp in phi1.get(a, {}).items():
                rel[f"{g}_1"] = rel.get(f"{g}_1", 0) + exp
            for g, exp in phi2.get(a, {}).items():
                rel[f"{g}_2"] = rel.get(f"{g}_2", 0) - exp
            rels_actual.append(rel)
            
        snf_actual = get_snf_diagonal(gens_actual, rels_actual)
        
        # Filter out 1s (trivial factors) and sort to compare isomorphism classes of abelianizations
        snf_conc_filtered = sorted([x for x in snf_conc if x != 1])
        snf_actual_filtered = sorted([x for x in snf_actual if x != 1])
        
        # If the abelianizations are not isomorphic, the groups are not isomorphic.
        neg_q = (snf_conc_filtered != snf_actual_filtered)
        
    except Exception:
        neg_q = False

    return [h1, h2, h3, neg_q]

CONDITION_LABELS = [
    "H_1: G1 and G2 are groups with presentations <X1|R1> and <X2|R2>",
    "H_2: A is a group",
    "H_3: phi1 and phi2 are injective group homomorphisms",
    "¬Q: The presentation <X1 U X2 | R1 U R2 U {phi1(a)phi2(a)^-1=1}> does not present the amalgamated free product"
]

N_HYP = 3
NEG_Q_INDEX = 3