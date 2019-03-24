;; if not prime, the number has divisor less or equal than sqrt(n)

(defn prime? [n]
  (defn smallest-divisor [n]
    (find-divisor 2))

  (defn divides? [x y]
    (= (% y x) 0))

  (defn square [x]
    (* x x))

  (defn find-divisor [test-divisor]
    (cond
      [(> (square test-divisor) n) n]
      [(divides? test-divisor n) test-divisor]
      [(find-divisor (+ test-divisor 1))]))

  (= n (smallest-divisor n)))

(print (prime? 11123822342111))
