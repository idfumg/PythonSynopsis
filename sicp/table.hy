(defn lookup [key table]
  (setv record (assoc key (cdr table)))
  (if record
      (cdr record)
      False))

(defn assoc [key records]
  (cond
    [(not records) False]
    [(= key (caar records)) (car records)]
    [(assoc key (cdr records))]))
