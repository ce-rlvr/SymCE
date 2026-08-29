import sympy

CONDITION_LABELS = [
    "H_1: (X, d_X) and (Y, d_Y) are metric spaces",
    "H_2: Y is a complete metric space",
    "H_3: f: A -> Y is uniformly continuous",
    "¬Q: f does not have a unique uniformly continuous extension to X"
]

N_HYP = 3
NEG_Q_INDEX = 3

def conditions(witness):
    x = sympy.Symbol('x', real=True)
    
    X = witness.get("X", sympy.S.EmptySet)
    Y = witness.get("Y", sympy.S.EmptySet)
    A = witness.get("A", sympy.S.EmptySet)
    f = witness.get("f", None)
    exts = witness.get("extensions", [])
    
    if f is not None:
        try:
            f = sympy.sympify(f)
        except Exception:
            pass
    
    try:
        exts = [sympy.sympify(ext) for ext in exts]
    except Exception:
        pass

    # H1: X and Y are metric spaces (subsets of Reals)
    try:
        h1 = X.is_subset(sympy.S.Reals) and Y.is_subset(sympy.S.Reals) and X != sympy.S.EmptySet and Y != sympy.S.EmptySet
    except Exception:
        h1 = False
        
    # H2: Y is complete (closed in Reals)
    try:
        if Y == sympy.S.Reals:
            h2 = True
        elif isinstance(Y, sympy.Interval):
            h2 = (not Y.left_open) and (not Y.right_open)
        elif isinstance(Y, sympy.FiniteSet):
            h2 = True
        else:
            h2 = False
    except Exception:
        h2 = False
        
    # H3: f: A -> Y is uniformly continuous
    try:
        h3 = False
        if f is not None and A.is_subset(X) and A != sympy.S.EmptySet:
            from sympy.calculus.util import continuous_domain
            cd = continuous_domain(f, x, A)
            if A.is_subset(cd):
                # Check uniform continuity
                is_unif = False
                if isinstance(A, sympy.Interval) and not A.left_open and not A.right_open and A.measure < sympy.S.Infinity:
                    is_unif = True
                elif isinstance(A, sympy.FiniteSet):
                    is_unif = True
                else:
                    deriv = sympy.diff(f, x)
                    try:
                        is_unif = True
                        if isinstance(A, sympy.Interval):
                            start = float(A.start) if A.start != -sympy.S.Infinity else -100.0
                            end = float(A.end) if A.end != sympy.S.Infinity else 100.0
                        else:
                            start, end = -100.0, 100.0
                        
                        step = (end - start) / 50.0
                        pts = [start + i*step for i in range(51)]
                        max_deriv = 0.0
                        for p in pts:
                            try:
                                val = abs(float(deriv.subs(x, p)))
                                if val > max_deriv:
                                    max_deriv = val
                            except Exception:
                                pass
                        if max_deriv > 1000.0:
                            is_unif = False
                    except Exception:
                        is_unif = False
                
                if is_unif:
                    # Check maps to Y
                    if Y == sympy.S.Reals:
                        h3 = True
                    else:
                        pts = []
                        if isinstance(A, sympy.Interval):
                            start = float(A.start) if A.start != -sympy.S.Infinity else -10.0
                            end = float(A.end) if A.end != sympy.S.Infinity else 10.0
                            pts = [start + (end - start)*0.1, start + (end - start)*0.5, start + (end - start)*0.9]
                        elif isinstance(A, sympy.FiniteSet):
                            pts = list(A)
                        
                        maps_to_y = True
                        for p in pts:
                            try:
                                val = float(f.subs(x, p))
                                if isinstance(Y, sympy.Interval):
                                    in_y = False
                                    y_start = float(Y.start)
                                    y_end = float(Y.end)
                                    if y_start <= val <= y_end:
                                        if val == y_start and Y.left_open:
                                            pass
                                        elif val == y_end and Y.right_open:
                                            pass
                                        else:
                                            in_y = True
                                    if not in_y:
                                        maps_to_y = False
                                        break
                                elif isinstance(Y, sympy.FiniteSet):
                                    if not any(abs(val - float(y)) < 1e-7 for y in Y):
                                        maps_to_y = False
                                        break
                            except Exception:
                                maps_to_y = False
                                break
                        if maps_to_y:
                            h3 = True
    except Exception:
        h3 = False
        
    # neg_Q: f does not have a unique uniformly continuous extension
    try:
        neg_q = False
        if len(exts) >= 2:
            valid_exts = []
            for ext in exts:
                # Check continuity on X
                from sympy.calculus.util import continuous_domain
                cd = continuous_domain(ext, x, X)
                if not X.is_subset(cd):
                    continue
                
                # Check uniform continuity on X
                is_unif = False
                if isinstance(X, sympy.Interval) and not X.left_open and not X.right_open and X.measure < sympy.S.Infinity:
                    is_unif = True
                elif isinstance(X, sympy.FiniteSet):
                    is_unif = True
                else:
                    deriv = sympy.diff(ext, x)
                    try:
                        is_unif = True
                        if isinstance(X, sympy.Interval):
                            start = float(X.start) if X.start != -sympy.S.Infinity else -100.0
                            end = float(X.end) if X.end != sympy.S.Infinity else 100.0
                        else:
                            start, end = -100.0, 100.0
                        
                        step = (end - start) / 50.0
                        pts = [start + i*step for i in range(51)]
                        max_deriv = 0.0
                        for p in pts:
                            try:
                                val = abs(float(deriv.subs(x, p)))
                                if val > max_deriv:
                                    max_deriv = val
                            except Exception:
                                pass
                        if max_deriv > 1000.0:
                            is_unif = False
                    except Exception:
                        is_unif = False
                
                if not is_unif:
                    continue
                    
                # Check maps to Y
                maps_to_y = True
                if Y != sympy.S.Reals:
                    pts = []
                    if isinstance(X, sympy.Interval):
                        start = float(X.start) if X.start != -sympy.S.Infinity else -10.0
                        end = float(X.end) if X.end != sympy.S.Infinity else 10.0
                        pts = [start + (end - start)*0.1, start + (end - start)*0.5, start + (end - start)*0.9]
                    elif isinstance(X, sympy.FiniteSet):
                        pts = list(X)
                    
                    for p in pts:
                        try:
                            val = float(ext.subs(x, p))
                            if isinstance(Y, sympy.Interval):
                                in_y = False
                                y_start = float(Y.start)
                                y_end = float(Y.end)
                                if y_start <= val <= y_end:
                                    if val == y_start and Y.left_open:
                                        pass
                                    elif val == y_end and Y.right_open:
                                        pass
                                    else:
                                        in_y = True
                                if not in_y:
                                    maps_to_y = False
                                    break
                            elif isinstance(Y, sympy.FiniteSet):
                                if not any(abs(val - float(y)) < 1e-7 for y in Y):
                                    maps_to_y = False
                                    break
                        except Exception:
                            maps_to_y = False
                            break
                if not maps_to_y:
                    continue
                        
                # Check agrees with f on A
                agrees = True
                if isinstance(A, sympy.Interval):
                    start = float(A.start) if A.start != -sympy.S.Infinity else -10.0
                    end = float(A.end) if A.end != sympy.S.Infinity else 10.0
                    test_pts = [start + (end - start)*0.1, start + (end - start)*0.5, start + (end - start)*0.9]
                elif isinstance(A, sympy.FiniteSet):
                    test_pts = list(A)
                else:
                    test_pts = []
                
                for p in test_pts:
                    try:
                        if abs(float(ext.subs(x, p)) - float(f.subs(x, p))) > 1e-7:
                            agrees = False
                            break
                    except Exception:
                        agrees = False
                        break
                
                if agrees:
                    valid_exts.append(ext)
            
            if len(valid_exts) >= 2:
                # Check if they are distinct on X
                diff_set = X - A
                test_pts = []
                if isinstance(diff_set, sympy.Interval):
                    start = float(diff_set.start) if diff_set.start != -sympy.S.Infinity else -10.0
                    end = float(diff_set.end) if diff_set.end != sympy.S.Infinity else 10.0
                    test_pts.append((start + end)/2)
                elif isinstance(diff_set, sympy.Union):
                    for arg in diff_set.args:
                        if isinstance(arg, sympy.Interval):
                            start = float(arg.start) if arg.start != -sympy.S.Infinity else -10.0
                            end = float(arg.end) if arg.end != sympy.S.Infinity else 10.0
                            test_pts.append((start + end)/2)
                elif isinstance(diff_set, sympy.FiniteSet):
                    test_pts.extend(list(diff_set))
                else:
                    if isinstance(X, sympy.Interval):
                        start = float(X.start) if X.start != -sympy.S.Infinity else -10.0
                        end = float(X.end) if X.end != sympy.S.Infinity else 10.0
                        test_pts = [start + (end - start)*0.1, start + (end - start)*0.9]
                
                distinct = False
                for p in test_pts:
                    try:
                        v1 = float(valid_exts[0].subs(x, p))
                        v2 = float(valid_exts[1].subs(x, p))
                        if abs(v1 - v2) > 1e-7:
                            distinct = True
                            break
                    except Exception:
                        pass
                
                if distinct:
                    neg_q = True

        if not neg_q:
            # Check if A is dense in X
            try:
                if isinstance(A, sympy.Interval):
                    closure_A = sympy.Interval(A.start, A.end, False, False)
                elif isinstance(A, sympy.FiniteSet):
                    closure_A = A
                elif isinstance(A, sympy.Union):
                    args = []
                    for arg in A.args:
                        if isinstance(arg, sympy.Interval):
                            args.append(sympy.Interval(arg.start, arg.end, False, False))
                        else:
                            args.append(arg)
                    closure_A = sympy.Union(*args)
                else:
                    closure_A = A
                
                if not X.is_subset(closure_A):
                    if Y == sympy.S.Reals or (isinstance(Y, sympy.Interval) and Y.measure > 0):
                        neg_q = True
            except Exception:
                pass

    except Exception:
        neg_q = False
        
    return [bool(h1), bool(h2), bool(h3), bool(neg_q)]