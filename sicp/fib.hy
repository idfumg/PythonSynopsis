(defn fib [n]
  (cond
    [(<= n 1) 1]
    [(+ (fib (- n 1))
        (fib (- n 2)))]))

(print (fib 7))

(defn fib [n]
  (defn fib-iter [a b count]
    (if (= count 0)
        a
        (fib-iter (+ a b) a (- count 1))))

  (fib-iter 1 0 n))

(print (fib 7))
