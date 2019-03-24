;; O(n) + O(n) memory
(defn expt [b n]
  (if (= n 0)
      1
      (* b (expt b (- n 1)))))

;; O(n) + O(1) memory
(defn expt [b n]
  (defn expt_iter [counter product]
    (if (= counter 0)
        product
        (expt-iter (- counter 1) (* product b))))

  (expt-iter n 1))

(print (expt 2 5))

;; O(log(n)) + O(1) memory
(defn fast-expt [b n]
  (defn square [x]
    (* x x))

  (defn even? [n]
    (= (% n 2) 0))

  (cond
    [(= n 0) 1]
    [(even? n) (square (fast-expt b (/ n 2)))]
    [(* b (fast-expt b (- n 1)))]))

(print (fast-expt 2 100))

