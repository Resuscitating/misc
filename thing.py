
(
    (cvp_fa := (cvp := (c := ((i := __import__)((ct := "ctypes")))).c_voidp).from_address),
    (gv := (lambda o: o.value)),
    (sv := (lambda o, v: o.__setattr__("value", v))),
    (gfmd := (lambda f: (cvp_fa(id(f) + 16)))),
    (gfvc := (lambda f: (cvp_fa(id(f) + 48)))),
    (st := (lambda f, *a, s={}: (s_si := s.__setitem__, a and (f in s or s_si(f, a)), s.get(f, 0) or (s_si(f, (gv(gfmd(f)), gv(gfvc(f)))), s[f])[~0])[~0])),
    (sw := (lambda f, F: (st(f, gv(gfmd(f)), gv(gfvc(f))), sv(gfmd(f), st(F)[0]), sv(gfvc(f), st(F)[1]), None)[~0]))
)
