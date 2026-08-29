import sympy
from sympy.combinatorics import SymmetricGroup, AlternatingGroup, DihedralGroup, CyclicGroup
from sympy.matrices import eye, zeros
import math
import itertools
import functools
import z3

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

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "H_3: k is the residue field R/m",
    "H_4: M is a finitely generated R-module",
    "H_5: The images of m_1, ..., m_n in M/mM form a basis for M/mM as a vector space over k",
    "¬Q: The elements m_1, ..., m_n do not generate M as an R-module"
]

N_HYP = 5
NEG_Q_INDEX = 5

def evaluate_finite_structure(R_add, R_mul, M_add, M_smul, m_elements):
    def get_zero(add_table):
        n = len(add_table)
        for i in range(n):
            if all(add_table[i][j] == j for j in range(n)) and all(add_table[j][i] == j for j in range(n)):
                return i
        return None

    def get_one(mul_table):
        n = len(mul_table)
        for i in range(n):
            if all(mul_table[i][j] == j for j in range(n)) and all(mul_table[j][i] == j for j in range(n)):
                return i
        return None

    def is_commutative_ring():
        n = len(R_add)
        zero = get_zero(R_add)
        if zero is None: return False
        one = get_one(R_mul)
        if one is None: return False
        if zero == one and n > 1: return False
        for i in range(n):
            for j in range(n):
                if R_add[i][j] != R_add[j][i]: return False
                if R_mul[i][j] != R_mul[j][i]: return False
                for k in range(n):
                    if R_add[R_add[i][j]][k] != R_add[i][R_add[j][k]]: return False
                    if R_mul[R_mul[i][j]][k] != R_mul[i][R_mul[j][k]]: return False
                    if R_mul[i][R_add[j][k]] != R_add[R_mul[i][j]][R_mul[i][k]]: return False
        return True

    h1 = is_commutative_ring()
    
    n = len(R_add)
    m_ideal = set()
    h2 = False
    if h1:
        one = get_one(R_mul)
        units = set()
        for i in range(n):
            for j in range(n):
                if R_mul[i][j] == one:
                    units.add(i)
                    break
        non_units = set(range(n)) - units
        is_ideal = True
        for x in non_units:
            for y in non_units:
                if R_add[x][y] not in non_units:
                    is_ideal = False
            for r in range(n):
                if R_mul[r][x] not in non_units:
                    is_ideal = False
        h2 = is_ideal and len(non_units) > 0
        if h2:
            m_ideal = non_units

    h3 = h2

    def is_module():
        r_n = len(R_add)
        m_n = len(M_add)
        m_zero = get_zero(M_add)
        if m_zero is None: return False
        r_one = get_one(R_mul)
        if r_one is None: return False
        for i in range(m_n):
            for j in range(m_n):
                if M_add[i][j] != M_add[j][i]: return False
                for k in range(m_n):
                    if M_add[M_add[i][j]][k] != M_add[i][M_add[j][k]]: return False
        for r in range(r_n):
            for s in range(r_n):
                for x in range(m_n):
                    if M_smul[R_add[r][s]][x] != M_add[M_smul[r][x]][M_smul[s][x]]: return False
                    if M_smul[R_mul[r][s]][x] != M_smul[r][M_smul[s][x]]: return False
        for r in range(r_n):
            for x in range(m_n):
                for y in range(m_n):
                    if M_smul[r][M_add[x][y]] != M_add[M_smul[r][x]][M_smul[r][y]]: return False
        for x in range(m_n):
            if M_smul[r_one][x] != x: return False
        return True

    h4 = is_module()

    def get_submodule(gens):
        r_n = len(R_add)
        elements = set([get_zero(M_add)])
        for g in gens:
            elements.add(g)
        changed = True
        while changed:
            changed = False
            new_elements = set(elements)
            for x in elements:
                for y in elements:
                    s = M_add[x][y]
                    if s not in new_elements:
                        new_elements.add(s)
                        changed = True
                for r in range(r_n):
                    s = M_smul[r][x]
                    if s not in new_elements:
                        new_elements.add(s)
                        changed = True
            elements = new_elements
        return elements

    h5 = False
    if h1 and h2 and h4:
        r_n = len(R_add)
        m_n = len(M_add)
        mM_gens = []
        for r in m_ideal:
            for x in range(m_n):
                mM_gens.append(M_smul[r][x])
        mM = get_submodule(mM_gens)
        
        span_gens = list(m_elements) + list(mM)
        span = get_submodule(span_gens)
        if len(span) == m_n:
            k_reps = []
            k_cosets = set()
            for r in range(r_n):
                coset = frozenset(R_add[r][x] for x in m_ideal)
                if coset not in k_cosets:
                    k_cosets.add(coset)
                    k_reps.append(r)
            
            indep = True
            for coeffs in itertools.product(k_reps, repeat=len(m_elements)):
                s = get_zero(M_add)
                for i, c in enumerate(coeffs):
                    term = M_smul[c][m_elements[i]]
                    s = M_add[s][term]
                if s in mM:
                    if not all(c in m_ideal for c in coeffs):
                        indep = False
                        break
            h5 = indep

    neg_q = False
    if h4:
        span = get_submodule(m_elements)
        neg_q = len(span) != len(M_add)

    return [h1, h2, h3, h4, h5, neg_q]

def conditions(witness):
    if isinstance(witness, tuple) and len(witness) == 5:
        try:
            return evaluate_finite_structure(*witness)
        except Exception:
            pass
            
    if isinstance(witness, dict) and 'R_add' in witness:
        try:
            return evaluate_finite_structure(
                witness['R_add'], witness['R_mul'],
                witness['M_add'], witness['M_smul'],
                witness['m_elements']
            )
        except Exception:
            pass

    def check(*names):
        if isinstance(witness, dict):
            for name in names:
                if name in witness:
                    v = witness[name]
                    return bool(v() if callable(v) else v)
        else:
            for name in names:
                if hasattr(witness, name):
                    v = getattr(witness, name)
                    return bool(v() if callable(v) else v)
        return False

    try:
        h1 = check('is_commutative_ring', 'H1', 'commutative')
    except Exception:
        h1 = False

    try:
        h2 = check('is_local_ring', 'H2', 'local')
    except Exception:
        h2 = False

    try:
        h3 = check('is_residue_field', 'H3', 'residue_field')
    except Exception:
        h3 = False

    try:
        h4 = check('is_finitely_generated_module', 'H4', 'finitely_generated')
    except Exception:
        h4 = False

    try:
        h5 = check('images_form_basis', 'H5', 'basis')
    except Exception:
        h5 = False

    try:
        if isinstance(witness, dict) and 'neg_Q' in witness:
            v = witness['neg_Q']
            neg_q = bool(v() if callable(v) else v)
        elif hasattr(witness, 'neg_Q'):
            v = getattr(witness, 'neg_Q')
            neg_q = bool(v() if callable(v) else v)
        else:
            q = check('elements_generate_module', 'Q', 'generates')
            neg_q = not q
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]