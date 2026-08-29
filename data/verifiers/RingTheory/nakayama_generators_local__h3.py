import itertools
from sympy.ntheory import factorint

CONDITION_LABELS = [
    "H_1: R is a commutative ring",
    "H_2: R is a local ring with maximal ideal m",
    "H_3: M is a finitely generated R-module",
    "H_4: m_1, ..., m_n are elements of M",
    "H_5: The images of m_1, ..., m_n in M/mM form a basis for M/mM as a vector space over k",
    "¬Q: The elements m_1, ..., m_n do not generate M as an R-module"
]

N_HYP = 5
NEG_Q_INDEX = 5

def conditions(witness):
    try:
        if not isinstance(witness, dict):
            return [False] * 6
        n = int(witness.get('n', 0))
        d = int(witness.get('d', 0))
        m_elements = witness.get('m_elements', [])
        k_size = int(witness.get('k_size', 0))
    except Exception:
        return [False] * 6

    # H_1: R = Z/nZ is a commutative ring
    try:
        h1 = (n >= 2)
    except Exception:
        h1 = False

    # H_2: R is a local ring with maximal ideal m
    p = None
    try:
        if n >= 2:
            factors = factorint(n)
            if len(factors) == 1:
                h2 = True
                p = list(factors.keys())[0]
            else:
                h2 = False
        else:
            h2 = False
    except Exception:
        h2 = False

    # H_3: M = (Z/nZ)^d is a finitely generated R-module
    try:
        h3 = (d >= 1)
    except Exception:
        h3 = False

    # H_4: m_1, ..., m_n are elements of M
    try:
        h4 = isinstance(m_elements, list) and len(m_elements) > 0
        if h4:
            for vec in m_elements:
                if not isinstance(vec, list) or len(vec) != d:
                    h4 = False
                    break
                for x in vec:
                    if not isinstance(x, int):
                        h4 = False
                        break
    except Exception:
        h4 = False

    # H_5: The images of m_1, ..., m_n in M/mM form a basis for M/mM as a vector space over k
    try:
        if p is not None and h4 and k_size >= 2 and p**d <= 100000:
            factors_k = factorint(k_size)
            if len(factors_k) == 1:
                p_k = list(factors_k.keys())[0]
                f = factors_k[p_k]
                if p_k == p:
                    c = len(m_elements)
                    if d == c * f:
                        mod_elements = [[x % p for x in vec] for vec in m_elements]
                        is_indep = True
                        for coeffs in itertools.product(range(p), repeat=c):
                            if all(coeff == 0 for coeff in coeffs):
                                continue
                            comb = [sum(coeffs[i] * mod_elements[i][j] for i in range(c)) % p for j in range(d)]
                            if all(x == 0 for x in comb):
                                is_indep = False
                                break
                        h5 = is_indep
                    else:
                        h5 = False
                else:
                    h5 = False
            else:
                h5 = False
        else:
            h5 = False
    except Exception:
        h5 = False

    # ¬Q: The elements m_1, ..., m_n do NOT generate M as an R-module
    try:
        if p is not None and h4 and p**d <= 100000:
            mod_elements = [[x % p for x in vec] for vec in m_elements]
            c = len(m_elements)
            span = set()
            for coeffs in itertools.product(range(p), repeat=c):
                comb = tuple(sum(coeffs[i] * mod_elements[i][j] for i in range(c)) % p for j in range(d))
                span.add(comb)
            neg_q = len(span) < (p ** d)
        else:
            neg_q = False
    except Exception:
        neg_q = False

    return [h1, h2, h3, h4, h5, neg_q]