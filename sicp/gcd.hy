;; greatest common delimiter
;; GCD(a, b) = GCD(b, r), r - reminder of a/b.
;; O(log n)

(defn gcd [a b]
  (if (= b 0)
      a
      (gcd b (% a b))))

(print (gcd 206, 40))
