(defn sqrt [x]
  (defn square [x]
    (* x x))

  (defn average [x y]
    (/ (+ x y) 2))

  (defn improve [guess]
    (average guess (/ x guess)))

  (defn good-enough? [guess]
    (< (abs (- (square guess) x)) 0.00000000000001))

  (defn sqrt-iter [guess]
    (if (good-enough? guess)
        guess
        (sqrt-iter (improve guess))))

  (sqrt-iter 1))

(print (sqrt 3))
