import sympy
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
import math
import itertools
import functools

# Top-level setup for named groups
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
    Checks if the witness is a valid counterexample to the false conjecture.
    The witness should be a dictionary providing:
      - 'H_size': int (order of the group H)
      - 'H_mult': 2D list (Cayley table of H, elements are 0 to H_size-1)
      - 'phi': list (mapping of elements under the automorphism phi)
      - 'S_names': list of strings (names of generators for the presentation, excluding 't')
      - 'R_ab_maker': callable taking S_syms and returning a list of relations in abelianized form
      - 'phi_S_ab_maker': callable taking S_syms and returning a list of phi(s) in abelianized form
    """
    try:
        H_size = witness['H_size']
        H_mult = witness['H_mult']
        phi = witness['phi']
        
        # Check H_1: phi is an automorphism of H
        h1_ok = True
        if H_size <= 0: h1_ok = False
        if len(H_mult) != H_size: h1_ok = False
        for row in H_mult:
            if len(row) != H_size: h1_ok = False
            for x in row:
                if not (0 <= x < H_size): h1_ok = False
                
        if h1_ok:
            identity = None
            for i in range(H_size):
                if all(H_mult[i][j] == j for j in range(H_size)) and all(H_mult[j][i] == j for j in range(H_size)):
                    identity = i
                    break
            if identity is None: h1_ok = False
            
        if h1_ok:
            for i in range(H_size):
                has_inv = False
                for j in range(H_size):
                    if H_mult[i][j] == identity and H_mult[j][i] == identity:
                        has_inv = True
                        break
                if not has_inv: h1_ok = False
                
        if h1_ok:
            for i in range(H_size):
                for j in range(H_size):
                    for k in range(H_size):
                        if H_mult[H_mult[i][j]][k] != H_mult[i][H_mult[j][k]]:
                            h1_ok = False
                            
        if h1_ok:
            if len(phi) != H_size: h1_ok = False
            if set(phi) != set(range(H_size)): h1_ok = False
            for i in range(H_size):
                for j in range(H_size):
                    if phi[H_mult[i][j]] != H_mult[phi[i]][phi[j]]:
                        h1_ok = False
    except Exception:
        h1_ok = False

    try:
        # Check H_2: G is the mapping torus group of phi
        # Since G is uniquely determined by H and phi, this is satisfied by definition
        h2_ok = witness.get('G_is_mapping_torus', True) if h1_ok else False
    except Exception:
        h2_ok = False

    try:
        if not h1_ok:
            neg_q = False
        else:
            # Compute the abelianization of G = H \rtimes_\phi Z
            # G_ab = (H / K) x Z, where K is the normal closure of [H, H] and {h^-1 phi(h)}
            inv = {}
            for i in range(H_size):
                for j in range(H_size):
                    if H_mult[i][j] == identity and H_mult[j][i] == identity:
                        inv[i] = j
                        break
                        
            generators = []
            for i in range(H_size):
                for j in range(H_size):
                    c = H_mult[inv[i]][inv[j]]
                    c = H_mult[c][i]
                    c = H_mult[c][j]
                    generators.append(c)
            for i in range(H_size):
                c = H_mult[inv[i]][phi[i]]
                generators.append(c)
                
            K = set(generators)
            K.add(identity)
            while True:
                new_K = set(K)
                for x in K:
                    for y in K:
                        new_K.add(H_mult[x][y])
                        new_K.add(inv[x])
                if len(new_K) == len(K):
                    break
                K = new_K
                
            G_finite_size = H_size // len(K)
            G_Z_count = 1
            
            # Compute the abelianization of the presentation
            S_names = witness['S_names']
            S_syms = [sympy.Symbol(name) for name in S_names]
            t_sym = sympy.Symbol('t')
            
            R_ab = witness['R_ab_maker'](*S_syms)
            phi_S_ab = witness['phi_S_ab_maker'](*S_syms)
            
            relations_ab = list(R_ab)
            for s, phi_s in zip(S_syms, phi_S_ab):
                # In abelianization, t * s * t^-1 = phi(s) becomes s - phi(s) = 0
                rel = s - phi_s
                relations_ab.append(rel)
                
            vars = S_syms + [t_sym]
            matrix_rows = []
            for rel in relations_ab:
                if isinstance(rel, (int, float)) and rel == 0:
                    row = [0] * len(vars)
                else:
                    rel = sympy.sympify(rel)
                    rel = sympy.expand(rel)
                    row = [int(rel.coeff(v)) for v in vars]
                matrix_rows.append(row)
                
            M = sympy.Matrix(matrix_rows)
            
            if M.rows == 0:
                pres_Z_count = M.cols
                pres_finite_size = 1
            else:
                try:
                    SNF = M.smith_normal_form()
                    pres_finite_size = 1
                    pres_Z_count = 0
                    for i in range(min(SNF.rows, SNF.cols)):
                        val = abs(SNF[i, i])
                        if val == 0:
                            pres_Z_count += 1
                        else:
                            pres_finite_size *= val
                    if SNF.cols > SNF.rows:
                        pres_Z_count += SNF.cols - SNF.rows
                except AttributeError:
                    # Fallback if smith_normal_form is unavailable
                    pres_Z_count = M.cols - M.rank()
                    pres_finite_size = None
                    
            # neg_Q is True if the presentation does NOT present G
            # (i.e., their abelianizations are not isomorphic)
            if pres_finite_size is not None:
                neg_q = (pres_finite_size != G_finite_size) or (pres_Z_count != G_Z_count)
            else:
                neg_q = (pres_Z_count != G_Z_count)
                
    except Exception:
        neg_q = False

    return [h1_ok, h2_ok, neg_q]

CONDITION_LABELS = [
    "H_1: phi is an automorphism of H",
    "H_2: G is the mapping torus group of phi",
    "¬Q: G does not admit the presentation"
]

N_HYP = 2
NEG_Q_INDEX = 2