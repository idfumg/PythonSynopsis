(defn car [x]
  (first x))

(defn cdr [x]
  (list (rest x)))

(defn memq [item x]
  (cond
    [(not x) None]
    [(= item (car x)) x]
    [(memq item (cdr x))]))

(print (memq 'apple '(pear banana prune)))
(print (memq 'apple '(x (apple sauce) y apple pear)))
