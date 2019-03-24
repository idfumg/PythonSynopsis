(defn factorial [n]
  (if (= n 1)
      1
      (* n (factorial (- n 1)))))

(print (factorial 6))

(defn factorial [n]
  (defn factorial-iter [product counter]
    (if (> counter n)
        product
        (factorial-iter (* product counter) (+ counter 1))))

  (factorial-iter 1 1))

(print (factorial 6))
