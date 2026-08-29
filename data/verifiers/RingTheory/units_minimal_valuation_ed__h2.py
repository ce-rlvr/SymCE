import sympy

QQ = sympy.QQ
ZZ = sympy.ZZ

CONDITION_LABELS = [
    "H_1: R is a Euclidean domain",
    "H_2: u is a non-zero element of R",
    "¬Q: u is a unit in R and v(u) != v(1), or u is not a unit and v(u) == v(1)"
]

N_HYP = 2
NEG_Q_INDEX = 2

def conditions(witness):
    try:
        is_finite_ring = False
        if isinstance(witness, dict) and 'elements' in witness:
            elements = witness['elements']
            add = witness['add']
            mul = witness['mul']
            zero = witness['zero']
            one = witness['one']
            v = witness['v']
            u = witness['u']
            is_finite_ring = True
        elif hasattr(witness, 'elements') and hasattr(witness, 'add'):
            elements = witness.elements
            add = witness.add
            mul = witness.mul
            zero = witness.zero
            one = witness.one
            v = witness.v
            u = witness.u
            is_finite_ring = True

        if is_finite_ring:
            if isinstance(v, dict):
                v_func = lambda x: v[x]
            else:
                v_func = v

            # H1: R is a Euclidean domain
            is_domain = True
            if zero == one:
                is_domain = False
                
            for a in elements:
                if add(a, zero) != a: is_domain = False
                if mul(a, one) != a: is_domain = False
                for b in elements:
                    if mul(a, b) != mul(b, a): is_domain = False
                    if add(a, b) != add(b, a): is_domain = False
                    if a != zero and b != zero and mul(a, b) == zero: is_domain = False
            
            is_euclidean = is_domain
            if is_euclidean:
                for a in elements:
                    if a != zero:
                        try:
                            val = v_func(a)
                            if not isinstance(val, int) or val < 0:
                                is_euclidean = False
                                break
                        except Exception:
                            is_euclidean = False
                            break
                
                if is_euclidean:
                    for a in elements:
                        for b in elements:
                            if b == zero: continue
                            found = False
                            for q in elements:
                                for r in elements:
                                    if add(mul(b, q), r) == a:
                                        if r == zero or v_func(r) < v_func(b):
                                            found = True
                                            break
                                if found: break
                            if not found:
                                is_euclidean = False
                                break
                        if not is_euclidean: break

            h1 = is_euclidean
            h2 = (u in elements) and (u != zero)

            if h2:
                is_unit = False
                for a in elements:
                    if mul(u, a) == one:
                        is_unit = True
                        break
                
                try:
                    v_cond = (v_func(u) == v_func(one))
                    neg_q = (is_unit != v_cond)
                except Exception:
                    neg_q = False
            else:
                neg_q = False

            return [bool(h1), bool(h2), bool(neg_q)]

        else:
            # Try sympy domain interface
            if isinstance(witness, tuple) and len(witness) == 3:
                domain, v, u = witness
            elif isinstance(witness, dict):
                domain = witness['domain']
                v = witness['v']
                u = witness['u']
            else:
                domain = witness.domain
                v = witness.v
                u = witness.u

            h1 = False
            if hasattr(domain, 'is_Field') and domain.is_Field:
                h1 = True
                for elem in [domain.one, u]:
                    try:
                        val = v(elem) if callable(v) else v[elem]
                        if not isinstance(val, int) or val < 0:
                            h1 = False
                            break
                    except Exception:
                        h1 = False
                        break
            
            h2 = False
            if u != domain.zero:
                try:
                    domain.convert(u)
                    h2 = True
                except Exception:
                    pass
            
            if h2:
                is_unit = domain.is_Field
                try:
                    val_u = v(u) if callable(v) else v[u]
                    val_one = v(domain.one) if callable(v) else v[domain.one]
                    v_cond = (val_u == val_one)
                    neg_q = (is_unit != v_cond)
                except Exception:
                    neg_q = False
            else:
                neg_q = False
            
            return [bool(h1), bool(h2), bool(neg_q)]

    except Exception:
        return [False, False, False]