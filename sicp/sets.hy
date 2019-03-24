(defn car [x]
  (first x))

(defn cdr [x]
  (list (rest x)))

(defn cadr [x]
  (car (cdr x)))

(defn caddr [x]
  (car (cdr (cdr x))))

(defn element-of-set? [x s]
  ;; only sorted sets allowed
  (cond
    [(not s) False]
    [(= x (car s)) True]
    [(< x (car s)) False]
    [(element-of-set? x (cdr s))]))

(defn element-of-set? [x s]
  (cond
    [(not s) False]
    [(= x (car s)) True]
    [(element-of-set? x (cdr s))]))

(defn adjoin-set [x s]
  (if (element-of-set? x s)
      s
      (cons x s)))

(defn intersection-set [set1 set2]
  ;; only sorted sets allowed
  (if (or (not set1) (not set2))
      '()
      (setv x1 (car set1))
      (setv x2 (car set2))
      (cond
        [(= x1 x2) (cons x1 (intersection-set (cdr set1) (cdr set2)))]
        [(< x1 x2) (intersection-set (cdr set1) set2)]
        [(< x2 x1) (intersection-set set1 (cdr set2))])))

(defn intersection-set [set1 set2]
  (cond
    [(or (not set1) (not set2)) '()]
    [(element-of-set? (car set1) set2) (cons (car set1)
                                             (intersection-set (cdr set1) set2))]
    [(intersection-set (cdr set1) set2)]))

(print (element-of-set? 'x '(y z n h g x k l m)))
(print (adjoin-set 'x '(y z)))
(print (adjoin-set 'p '(p x y z l)))
(print (adjoin-set 1 '(1 2 3)))
(print (intersection-set '(x y z) '(a m n r u th x j u e y q a z)))


;; TREES

(defn entry [tree]
  (car tree))

(defn left-branch [tree]
  (cadr tree))

(defn right-branch [tree]
  (caddr tree))

(defn make-tree [entry left right]
  [entry left right])

(defn element-of-set? [x s]
  (cond
    [(not s) False]
    [(= x s) True]
    [(not (isinstance s list)) False]
    [(= x (entry s)) True]
    [(< x (entry s)) (element-of-set? x (left-branch s))]
    [(> x (entry s)) (element-of-set? x (right-branch s))]))

(defn adjoin-set [x s]
  (cond
    [(not s) (make-tree x [] [])]
    [(= x s) s]
    [(not (isinstance s list)) (if (< x s)
                                   (make-tree s x [])
                                   (make-tree s [] x))]
    [(= x (entry s)) s]
    [(< x (entry s)) (make-tree (entry s) (adjoin-set x (left-branch s)) (right-branch s))]
    [(> x (entry s)) (make-tree (entry s) (left-branch s) (adjoin-set x (right-branch s)))]))

(setv mytree (make-tree 3 2 (make-tree 4 None 5)))
(print (element-of-set? 5 mytree))
(print (adjoin-set 8 mytree))
(print (adjoin-set 7 (adjoin-set 8 mytree)))
