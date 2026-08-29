import sympy
from sympy.combinatorics import PermutationGroup, Permutation
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, CyclicGroup, DihedralGroup

# Top-level setup for standard algebra objects
S3 = SymmetricGroup(3)
S4 = SymmetricGroup(4)
A4 = AlternatingGroup(4)
D4 = DihedralGroup(4)
C4 = CyclicGroup(4)
V4 = PermutationGroup(Permutation([[0, 1], [2, 3]]), Permutation([[0, 2], [1, 3]]))
Z2 = CyclicGroup(2)
Z3 = CyclicGroup(3)
Z4 = CyclicGroup(4)
Z6 = CyclicGroup(6)
trivial = CyclicGroup(1)

def conditions(witness):
    """
    Checks whether the witness is a valid counterexample to the false conjecture.
    Witness is expected to be a tuple: (N, H, phi, n, h, m)
    """
    try:
        if len(witness) != 6:
            return [False] * 5
        N, H, phi, n, h, m = witness
    except Exception:
        return [False] * 5

    # H1: N and H are groups
    try:
        h1 = isinstance(N, PermutationGroup) and isinstance(H, PermutationGroup)
    except Exception:
        h1 = False

    # H2: phi is a group homomorphism from H to Aut(N)
    try:
        h2 = True
        phi_dict = {}
        # Normalize phi to a dictionary for robust access
        for hx in H.elements:
            phi_dict[hx] = {}
            for nx in N.elements:
                val = None
                if callable(phi):
                    try:
                        val = phi(hx, nx)
                    except Exception:
                        try:
                            val = phi(hx)(nx)
                        except Exception:
                            pass
                elif isinstance(phi, dict):
                    if hx in phi:
                        if callable(phi[hx]):
                            try:
                                val = phi[hx](nx)
                            except Exception:
                                pass
                        elif isinstance(phi[hx], dict):
                            val = phi[hx].get(nx)
                    elif (hx, nx) in phi:
                        val = phi.get((hx, nx))
                
                if val is None or val not in N.elements:
                    h2 = False
                    break
                phi_dict[hx][nx] = val
            if not h2: 
                break
                
        if h2:
            # Check that each phi[h] is an automorphism of N
            for hx in H.elements:
                mapping = phi_dict[hx]
                if set(mapping.keys()) != set(N.elements) or set(mapping.values()) != set(N.elements):
                    h2 = False
                    break
                for n1 in N.elements:
                    for n2 in N.elements:
                        if mapping[n1 * n2] != mapping[n1] * mapping[n2]:
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
                
        if h2:
            # Check that phi is a homomorphism H -> Aut(N)
            for h1_el in H.elements:
                for h2_el in H.elements:
                    h12 = h1_el * h2_el
                    for nx in N.elements:
                        if phi_dict[h12][nx] != phi_dict[h1_el][phi_dict[h2_el][nx]]:
                            h2 = False
                            break
                    if not h2: break
                if not h2: break
    except Exception:
        h2 = False

    # H3: G is the external semidirect product of N and H
    # This is definitional given that N, H are groups and phi is a valid homomorphism
    try:
        h3 = h1 and h2
    except Exception:
        h3 = False

    # H4: (n, h) is an element of G
    try:
        h4 = (n in N.elements) and (h in H.elements)
    except Exception:
        h4 = False

    # ¬Q: The m-th power formula fails for (n, h)^m
    try:
        if not (isinstance(m, int) or isinstance(m, sympy.Integer)):
            neg_q = False
        else:
            m = int(m)
            
            # Find identities
            n_id = None
            for nx in N.elements:
                if nx * nx == nx:
                    n_id = nx
                    break
            h_id = None
            for hx in H.elements:
                if hx * hx == hx:
                    h_id = hx
                    break
                    
            def sdp_mult(e1, e2):
                n1, h1_el = e1
                n2, h2_el = e2
                return (n1 * phi_dict[h1_el][n2], h1_el * h2_el)
                
            def sdp_inv(e):
                nx, hx = e
                hx_inv = ~hx
                nx_inv = ~nx
                return (phi_dict[hx_inv][nx_inv], hx_inv)
                
            def power(base, exp, identity):
                if exp == 0:
                    return identity
                if exp < 0:
                    base = ~base
                    exp = -exp
                res = identity
                b = base
                while exp > 0:
                    if exp % 2 == 1:
                        res = res * b
                    b = b * b
                    exp //= 2
                return res
                
            def sdp_pow(elem, exp):
                if exp == 0:
                    return (n_id, h_id)
                if exp < 0:
                    elem = sdp_inv(elem)
                    exp = -exp
                res = (n_id, h_id)
                base = elem
                while exp > 0:
                    if exp % 2 == 1:
                        res = sdp_mult(res, base)
                    base = sdp_mult(base, base)
                    exp //= 2
                return res
                
            # Compute LHS: (n, h)^m in the semidirect product
            lhs = sdp_pow((n, h), m)
            
            # Compute RHS: (n * phi_h(n) * ... * phi_{h^{m-1}}(n), h^m)
            if m > 0:
                rhs_n = n_id
                for i in range(m):
                    h_pow = power(h, i, h_id)
                    rhs_n = rhs_n * phi_dict[h_pow][n]
                rhs = (rhs_n, power(h, m, h_id))
            else:
                # For m <= 0, the explicit product notation is empty/ill-defined
                rhs = (n_id, power(h, m, h_id))
                
            neg_q = (lhs != rhs)
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, neg_q]

CONDITION_LABELS = [
    "H_1: N and H are groups",
    "H_2: phi is a group homomorphism from H to Aut(N)",
    "H_3: G is the external semidirect product of N and H",
    "H_4: (n, h) is an element of G",
    "¬Q: The m-th power formula fails for (n, h)^m"
]

N_HYP = 4
NEG_Q_INDEX = 4