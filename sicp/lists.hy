(defn fib [n]
  (cond
    [(<= n 1) 1]
    [(+ (fib (- n 1))
        (fib (- n 2)))]))

(defn car [x]
  (first x))

(defn cdr [x]
  (list (rest x)))

(defn list-ref [items n]
  (if (= n 0)
      (car items)
      (list-ref (cdr items) (- n 1))))

;; LISTS

(setv squares [1 4 9 16 25])
(print (list-ref squares 4))

(defn length [items]
  (if (= items [])
      0
      (+ 1 (length (cdr items)))))

(defn length [items]
  (defn length-iter [x counter]
    (if (= x [])
        counter
        (length-iter (cdr x) (+ 1 counter))))
  (length-iter items 0))

(setv odds [1 3 5 7])
(print (length odds))

(defn scale-list [items factor]
  (if (= items [])
      None
      (cons (* (car items) factor) (scale-list (cdr items) factor))))

(print (scale-list [1 2 3 4 5] 10))

(print (map (fn [x] (* x 10)) [1 2 3 4 5]))

(defn map [proc items]
  (if (= items [])
      None
      (cons (proc (car items)) (map proc (cdr items)))))

(print (map (fn [x] (* x 10)) [1 2 3 4 5]))
(print (map abs [-1 0 1 -3 -40 -8.1]))

(defn scale-list [items factor]
  (map (fn [x] (* x factor)) items))

(print (scale-list [1 2 3 4 5] 10))


;; TREES

(setv x (cons '(1 2) '(3 4)))
(print (length x))


(defn count-leaves [x]
  (cond
    [(= x []) 0]
    [(not (isinstance x list)) 1]
    [(+ (count-leaves (car x)) (count-leaves (cdr x)))]))

(print (count-leaves x))

(defn scale-tree [tree factor]
  (cond
    [(= tree []) None]
    [(not (isinstance tree list)) (* tree factor)]
    [(cons (scale-tree (car tree) factor)
           (scale-tree (cdr tree) factor))]))

(print (scale-tree '(1 2 (3 (4 5))) 10))

(defn scale-tree [tree factor]
  (map (fn [sub-tree]
         (if (not (isinstance sub-tree list))
             (* sub-tree factor)
             (scale-tree sub-tree factor)))
       tree))

(print (scale-tree '(1 2 (3 (4 5))) 10))

(defn tree-map [proc tree]
  (map (fn [sub-tree]
         (if (not (isinstance sub-tree list))
             (proc sub-tree)
             (tree-map proc sub-tree)))
       tree))

(print (tree-map (fn [x] (* x 10)) '(1 2 (3 (4 5)))))

;; SEQUENCES

(defn filter [predicate sequence]
  (cond
    [(= sequence []) None]
    [(predicate (car sequence))
     (cons (car sequence) (filter predicate (cdr sequence)))]
    [(filter predicate (cdr sequence))]))

(defn accumulate [op initial sequence]
  (if (= sequence [])
      initial
      (op (car sequence)
          (accumulate op initial (cdr sequence)))))

(defn enumerate-interval [low high]
  (if (> low high)
      None
      (cons low (enumerate-interval (+ low 1) high))))

(print (enumerate-interval 2 7))

(defn enumerate-tree [tree]
  (cond
    [(= tree []) []]
    [(not (isinstance tree list)) [tree]]
    [(+ (enumerate-tree (car tree))
        (enumerate-tree (cdr tree)))]))

(print (enumerate-tree '(1 (2 (3 4)) 5)))

(defn sum-odd-squares [tree]
  (accumulate +
              0
              (map (fn [x] (* x x))
                   (filter odd?
                           (enumerate-tree tree)))))

(print (sum-odd-squares '(1 (2 (3 4)) 5)))

(defn even-fibs [n]
  (accumulate cons
              None
              (filter even?
                      (map fib
                           (enumerate-interval 0 n)))))

(print (even-fibs 10))

(defn length [seq]
  (accumulate (fn [a b] (+ 1 b))
              0
              seq))

(print (length [1 2 3 4 5 10]))
