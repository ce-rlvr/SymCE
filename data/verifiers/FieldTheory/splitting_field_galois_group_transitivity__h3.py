import sympy as sp
from sympy.combinatorics.named_groups import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup

# Top-level setup for potential witness references
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

CONDITION_LABELS = [
    "H_1: F is a field",
    "H_2: f(x) is a separable irreducible polynomial of degree n",
    "¬Q: Gal(E/F) does not act transitively on the roots of f(x) or is not isomorphic to a transitive subgroup of S_n"
]

N_HYP = 2
NEG_Q_INDEX = 2

def get_deg_E(witness):
    """Helper to extract the degree of the extension field E over F (assumed Q)."""
    if witness.get('E') == sp.QQ or witness.get('E') == 'QQ':
        return 1
    if 'E_poly' in witness and 'y' in witness:
        try:
            E_poly_obj = sp.Poly(witness['E_poly'], witness['y'], domain='QQ')
            if E_poly_obj.is_irreducible:
                return E_poly_obj.degree()
        except Exception:
            pass
    E = witness.get('E')
    if hasattr(E, 'mod'):
        try:
            return sp.Poly(E.mod).degree()
        except Exception:
            pass
    if hasattr(E, 'minpoly'):
        try:
            return sp.Poly(E.minpoly).degree()
        except Exception:
            pass
    if isinstance(E, str) and E in ['Q', 'F', 'QQ']:
        return 1
    return None

def conditions(witness) -> list[bool]:
    if not isinstance(witness, dict):
        return [False, False, False]

    try:
        f = witness['f']
        x = witness['x']
    except KeyError:
        return [False, False, False]

    # H_1: F is a field
    try:
        F = witness.get('F', sp.QQ)
        if str(F) in ['ZZ', 'Integers', 'Z']:
            h1 = False
        else:
            # Verify that f can be parsed as a polynomial over QQ (our default field)
            sp.Poly(f, x, domain='QQ')
            h1 = True
    except Exception:
        h1 = False

    # H_2: f(x) is a separable irreducible polynomial of degree n
    n = 1
    try:
        f_poly = sp.Poly(f, x, domain='QQ')
        n_val = f_poly.degree()
        
        if 'n' in witness:
            n = witness['n']
            if n != n_val:
                h2 = False
            else:
                n = n_val
        else:
            n = n_val

        is_irred = f_poly.is_irreducible
        
        f_diff = f_poly.diff()
        gcd_poly = f_poly.gcd(f_diff)
        is_sep = gcd_poly.degree() == 0
        
        if is_irred and is_sep and n >= 1:
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False

    # ¬Q: Gal(E/F) does not act transitively on the roots of f(x) or is not isomorphic to a transitive subgroup of S_n
    try:
        deg_E = get_deg_E(witness)
        if deg_E is not None:
            # Determine the minimal possible degree of the splitting field of f over Q
            sf_deg_min = n
            if n == 2:
                sf_deg_min = 2
            elif n == 3:
                disc = sp.discriminant(f_poly)
                if sp.sqrt(disc).is_rational:
                    sf_deg_min = 3
                else:
                    sf_deg_min = 6
            
            # If the degree of E is not a multiple of the splitting field's minimal degree,
            # E cannot contain the splitting field. Thus f(x) does not split completely in E,
            # and Gal(E/F) cannot act transitively on the n roots of f(x).
            if deg_E % sf_deg_min != 0:
                neg_q = True
            else:
                neg_q = False
                # Extra check for n=2: if deg_E == 2, E must be exactly the splitting field to make Q true.
                # We can verify this by checking if the discriminants' ratio is a perfect square.
                if n == 2 and deg_E == 2 and 'E_poly' in witness and 'y' in witness:
                    try:
                        disc_f = sp.discriminant(f_poly)
                        E_poly_obj = sp.Poly(witness['E_poly'], witness['y'], domain='QQ')
                        disc_E = sp.discriminant(E_poly_obj)
                        if not sp.sqrt(disc_f / disc_E).is_rational:
                            neg_q = True
                    except Exception:
                        pass
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, neg_q]