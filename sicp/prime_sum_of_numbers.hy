(defn car[n]
  (first n))

(defn cdr [n]
  (list (rest n)))

(defn cadr [n]
  (first (cdr n)))

(defn accumulate [op initial sequence]
  (if (= sequence [])
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(defn enumerate-interval [low high]
  (if (> low high)
      []
      (cons low (enumerate-interval (+ low 1) high))))

(defn flatmap [proc seq]
  (accumulate + [] (proc seq)))

(defn prime-sum? [pair]
  (import prime)
  (prime.prime? (+ (car pair) (cadr pair))))

(defn make-pair-sum [pair]
  [(car pair) (cadr pair) (+ (car pair) (cadr pair))])

(defn prime-sum-pairs [n]
  (map make-pair-sum
       (filter prime-sum?
               (flatmap
                 identity
                 (list (map (fn [i] (list (map (fn [j] [i j])
                                               (enumerate-interval 1 (- i 1)))))
                            (enumerate-interval 1 n)))))))


(print (list (prime-sum-pairs 6)))
