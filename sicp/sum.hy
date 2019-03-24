(defn sum [term a next b]
  (if (> a b)
      0
      (+ (term a)
         (sum term (next a) next b))))

(defn sum-cubes [a b]
  (sum (fn [x] (* x x x)) a inc b))

(print (sum-cubes 1 10))

(defn sum-integers [a b]
  (sum identity a inc b))

(print (sum-integers 1 100))

