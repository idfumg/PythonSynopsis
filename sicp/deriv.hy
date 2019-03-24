(defn car [x]
  (first x))

(defn cdr [x]
  (list (rest x)))

(defn cadr [x]
  (car (cdr x)))

(defn caddr [x]
  (car (cdr (cdr x))))

(defn number? [x]
  (isinstance x int))

(defn =number? [x value]
  (and (number? x) (= x value)))

(defn variable? [x]
  (symbol? x))

(defn same-variable? [v1 v2]
  (and (variable? v1) (variable? v2) (= v1 v2)))

(defn make-sum [a1 a2]
  (cond
    [(=number? a1 0) a2]
    [(=number? a2 0) a1]
    [(and (number? a1) (number? a2)) (+ a1 a2)]
    [['+ a1 a2]]))

(defn make-product [a1 a2]
  (cond
    [(or (=number? a1 0) (=number? a2 0)) 0]
    [(=number? a1 1) a2]
    [(=number? a2 1) a1]
    [(and (number? a1) (number? a2)) (* a1 a2)]
    [['* a1 a2]]))

(defn sum? [x]
  (and (isinstance x list) (= (car x) '+)))

(defn addend [x]
  (cadr x))

(defn augend [x]
  (caddr x))

(defn product? [x]
  (and (isinstance x list) (= (car x) '*)))

(defn multiplier [x]
  (cadr x))

(defn multiplicand [x]
  (caddr x))

(defn deriv [exp var]
  (cond
    [(number? exp) 0]
    [(variable? exp) (if (same-variable? exp var) 1 0)]
    [(sum? exp) (make-sum (deriv (addend exp) var)
                          (deriv (augend exp) var))]
    [(product? exp) (make-sum (make-product (multiplier exp)
                                            (deriv (multiplicand exp) var))
                              (make-product (deriv (multiplier exp) var)
                                            (multiplicand exp)))]
    [(print "Wrong expression type!")
     (exit 1)]))

(print (deriv '(+ x 3) 'x))
(print (deriv '(* x y) 'x))
(print (deriv '(* (* x y) (+ x 3)) 'x))
