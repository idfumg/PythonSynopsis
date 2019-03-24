(defn car[n]
  (print "car" n)
  (first n))

(defn cdr [n]
  (print "cdr" n)
  (list (rest n)))

(defn remove [item sequence]
  (print "remove" sequence)
  (cond
    [(is sequence None) []]
    [(= sequence []) []]
    [(not (isinstance sequence list)) sequence]
    [(list (filter (fn [x] (not (= item x)))
                   sequence))]))

;; (defn remove-all [items sequence]
;;   (if (= items [])
;;       sequence
;;       (remove-all (cdr items) (remove (car items) sequence))))

;; (defn permutations [s]
;;   (cond
;;     [(= s []) []]
;;     [(map (fn [x]
;;             (list (map (fn [y]
;;                          (+ [x] (flatten y) (remove-all (flatten y) (remove x s))))
;;                        (permutations (remove x s)))))
;;           s)]))

(defn accumulate [op initial sequence]
  (print "accumulate" (list sequence))
  (if (or (= sequence []))
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(defn flatmap [proc seq]
  (print "flatmap" seq)
  (cond
    [(is seq None) []]
    [(accumulate + [] (map proc seq))]
    [[]]))

(defn permutations [s]
  (print "permutations" s)
  (cond
    ;; [(not (isinstance s list)) s]
    ;; [(is s None) []]
    ;; [(= s []) []]
    [(flatmap (fn [x]
                (print x s)
                (setv p (permutations (remove x s)))
                (if (isinstance p list)
                    (list (map (fn [y] (cons x y)) p))
                    []))
              s)]))

(print (list (flatmap (fn [x] x)
                      [1,2])))

;; (print "!!!!!!" (permutations [1 2 3 4]))
;; (print (list (permutations [1 2 3 4])))
