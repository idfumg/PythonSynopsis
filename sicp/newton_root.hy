;; find function root by two points where function value is positive and negative.

(defn average [a b]
  (/ (+ a b) 2))

(defn positive? [a]
  (> a 0))

(defn negative? [a]
  (< a 0))

(defn close-enough? [a b]
  (< (abs (- a b)) 0.00000000001))

(defn search [f neg-point pos-point]
  (setv middle-point (average neg-point pos-point))
  (if (close-enough? neg-point pos-point)
      middle-point
      (do
        (setv test-value (f middle-point))
        (cond
          [(positive? test-value) (search f neg-point middle-point)]
          [(negative? test-value) (search f middle-point pos-point)]
          [middle-point]))))

(defn half-interval-method [f a b]
  (setv a-value (f a))
  (setv b-value (f b))
  (cond
    [(and (negative? a-value) (positive? b-value)) (search f a b)]
    [(and (positive? a-value) (negative? b-value)) (search f b a)]
    [None]))

(import math)

(print (half-interval-method math.sin 3.1 3.2))
