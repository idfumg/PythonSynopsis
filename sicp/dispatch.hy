(defn cons [x y]
  (defn dispatch [m]
    (cond
      [(= m 'car) x]
      [(= m 'cdr) y]
      [(do
         (print "Error! Cons: wrong argument!")
         (exit 1))]))
  dispatch)

(defn car [z]
  (z 'car))

(defn cdr [z]
  (z 'cdr))

(setv x (cons 1 2))
(print "x =" x ",car =" (car x) ", cdr =" (cdr x))
