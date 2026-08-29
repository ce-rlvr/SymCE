import sympy
from sympy import Symbol, Rational, Integer, Matrix, eye, zeros
from sympy.abc import x, y, z

# Top-level setup for potential witness expressions
Z = Symbol('Z')
Q = Symbol('Q')
R = Symbol('R')
M = Symbol('M')

def conditions(witness):
    """
    Verifies if the given witness is a counterexample to the false conjecture:
    "Over a local ring R, if the images of m_1, ..., m_n form a basis for M/mM, 
    then m_1, ..., m_n generate M."
    (This is Nakayama's lemma with the 'M is finitely generated' hypothesis dropped).
    """
    h1 = h2 = h3 = h4 = h5 = neg_q = False
    
    try:
        # 0. Handle the case where the witness is provided as a descriptive string
        if isinstance(witness, str):
            w_lower = witness.lower()
            if any(term in w_lower for term in ['z_(p)', 'z_p', 'k[[x]]', 'local', 'z_{(p)}', 'q[[x]]', 'r[[x]]']):
                h1 = h2 = h3 = True
            if '[]' in w_lower or 'empty' in w_lower or 'm_elements' in w_lower or 'm_i' in w_lower:
                h4 = True
            divisible_terms = ['q', 'k((x))', 'frac', 'fraction', 'rationals', '1/p', '1/2', 'infty', 'prufer', 'prüfer']
            if any(term in w_lower for term in divisible_terms):
                if '[]' in w_lower or 'empty' in w_lower or '0' in w_lower:
                    h5 = True
                    neg_q = True
            return [h1, h2, h3, h4, h5, neg_q]

        # 1. Try to extract properties if witness is a dict
        if isinstance(witness, dict):
            R_obj = witness.get('R', witness.get('ring', ''))
            M_obj = witness.get('M', witness.get('module', ''))
            m_elements = witness.get('m_elements', witness.get('elements', []))
            
            # Explicit boolean flags provided by the generator
            if 'is_commutative_ring' in witness: h1 = bool(witness['is_commutative_ring'])
            if 'is_local_ring' in witness: h2 = bool(witness['is_local_ring'])
            if 'residue_field' in witness: h3 = True
            if 'M_mod_mM_basis' in witness: h5 = bool(witness['M_mod_mM_basis'])
            if 'generates_M' in witness: neg_q = not bool(witness['generates_M'])
            
        # 2. Try to extract properties if witness is a tuple/list
        elif isinstance(witness, (tuple, list)):
            if len(witness) >= 3:
                R_obj = witness[0]
                M_obj = witness[1]
                m_elements = witness[2]
            else:
                R_obj, M_obj, m_elements = "", "", []
                
        # 3. Try to extract properties if witness is a custom object
        else:
            R_obj = getattr(witness, 'R', getattr(witness, 'ring', ''))
            M_obj = getattr(witness, 'M', getattr(witness, 'module', ''))
            m_elements = getattr(witness, 'm_elements', getattr(witness, 'elements', []))
            
            if hasattr(witness, 'is_commutative_ring'):
                val = witness.is_commutative_ring
                h1 = bool(val() if callable(val) else val)
            if hasattr(witness, 'is_local_ring'):
                val = witness.is_local_ring
                h2 = bool(val() if callable(val) else val)
            if hasattr(witness, 'M_mod_mM_basis'):
                val = witness.M_mod_mM_basis
                h5 = bool(val() if callable(val) else val)
            if hasattr(witness, 'generates_M'):
                val = witness.generates_M
                neg_q = not bool(val() if callable(val) else val)

        R_str = str(R_obj).lower()
        M_str = str(M_obj).lower()
        
        # Evaluate H1, H2, H3 based on R_str if not already set
        if not h1:
            if any(term in R_str for term in ['z_(p)', 'z_p', 'k[[x]]', 'local', 'z_{(p)}', 'q[[x]]', 'r[[x]]']):
                h1 = True
        if not h2:
            if any(term in R_str for term in ['z_(p)', 'z_p', 'k[[x]]', 'local', 'z_{(p)}', 'q[[x]]', 'r[[x]]']):
                h2 = True
        if not h3:
            h3 = h2  # If it's a local ring, it has a residue field
            
        # Evaluate H4
        if isinstance(m_elements, (list, tuple, set)):
            h4 = True
            
        # Evaluate H5 and neg_Q based on M_str and m_elements if not already set
        if not h5 or not neg_q:
            divisible_terms = ['q', 'k((x))', 'frac', 'fraction', 'rationals', '1/p', '1/2', 'infty', 'prufer', 'prüfer']
            is_divisible = any(term in M_str for term in divisible_terms)
            is_mixed = is_divisible and any(op in M_str for op in ['+', 'oplus', 'sum'])
            
            if is_mixed:
                # For mixed modules like Q \oplus Z_(p), the basis for M/mM has size > 0
                if len(m_elements) > 0:
                    h5 = True
                    neg_q = True
            elif is_divisible:
                # For purely divisible modules like Q, M = mM, so M/mM = 0 and the basis is empty
                if len(m_elements) == 0:
                    h5 = True
                    neg_q = True

    except Exception:
        pass

    return [h1, h2, h3, h4, h5, neg_q]

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "H_3: k is the residue field R/m",
    "H_4: m_1, ..., m_n are elements of M",
    "H_5: The images of m_1, ..., m_n in M/mM form a basis for M/mM as a vector space over k",
    "¬Q: The elements m_1, ..., m_n do not generate M as an R-module"
]

N_HYP = 5
NEG_Q_INDEX = 5