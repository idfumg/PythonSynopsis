;; fixed point is point that f(x) = x.
;; to find fixed point we must apply f multiply times: f(x), f(f(x)), f(f(f(x))).

(defn fixed-point [f first-guess]
  (defn close-enough? [x y]
    (< (abs (- x y)) 0.0000001))

  (defn try-next [guess]
    (setv next (f guess))
    (if (close-enough? next guess)
        next
        (try-next next)))

  (try-next first-guess))

(import math)
(print (fixed-point math.cos 1.0))
(print (fixed-point (fn [y] (+ (math.sin y) (math.cos y))) 1.0))

;; by using fixed point algorithm we can find root of x
;; y = sqrt(x)
;; y^2 = x
;; y = x / y           ;; it doesn't work, need a smaller step
;; 2y = y + x / y
;; торможение усреднением. возвращается функция, значение которое в точке x есть
;; среднее арифметическое между x и f(x)
;; y = (y + x / y) / 2
(defn sqrt [x]
  (defn average [a b]
    (/ (+ a b) 2))

  (defn average-damp [f]
    (fn [x] (average x (f x))))

  (fixed-point (average-damp (fn [y] (/ x y))) 1.0))

(print (sqrt 3))

(defn cube-root [x]
  (defn average [a b]
    (/ (+ a b) 2))

  (defn average-damp [f]
    (fn [x] (average x (f x))))

  (fixed-point (average-damp (fn [y] (/ x (* y y)))) 1.0))

(print (cube-root 27))
