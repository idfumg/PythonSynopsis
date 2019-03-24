(defn add-rat [x y]
  (make-rat (+ (* (numer x) (denom y))
               (* (denom y) (numer x)))
            (* (denom x) (denom y))))

(defn sub-rat [x y]
  (make-rat (- (* (numer x) (denom y))
               (* (numer y) (denom x)))
            (* (denom x) (denom y))))

(defn mul-rat [x y]
  (make-rat (* (numer x) (numer y))
            (* (denom x) (denom y))))

(defn div-rat [x y]
  (make-rat (* (numer x) (denom y))
            (* (denom x) (numer y))))

(defn equal-rat? [x y]
  (= (* (numer x) (denom y))
     (* (denom x) (numer y))))

(defn make-rat [n d]
  (setv g (gcd n d))
  (cons (/ n g) (/ d g)))

(defn numer [x]
  (first x))

(defn denom [x]
  (first (rest x)))

(defn gcd [a b]
  (if (= b 0)
      a
      (gcd b (% a b))))

(defn print-rat [x]
  (print (numer x) "/" (denom x)))

(setv one-half (make-rat 1 2))
(print-rat one-half)
(setv six-nine (mul-rat (make-rat 2 3) (make-rat 3 3)))
(print-rat six-nine)
