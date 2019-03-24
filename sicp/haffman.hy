(defn car [param]
  (first param))

(defn cdr [param]
  (list (rest param)))

(defn cddr [param]
  (cdr (cdr param)))

(defn cadr [param]
  (car (cdr param)))

(defn caddr [param]
  (car (cdr (cdr param))))

(defn cadddr [param]
  (car (cdr (cdr (cdr param)))))

(defn make-leaf [symbol weight]
  ['leaf symbol weight])

(defn leaf? [param]
  (= (car param) 'leaf))

(defn symbol-leaf [param]
  (cadr param))

(defn weight-leaf [param]
  (caddr param))

(defn make-code-tree [left right]
  [left
   right
   (+ (symbols left) (symbols right))
   (+ (weight left) (weight right))])

(defn left-branch [tree]
  (car tree))

(defn right-branch [tree]
  (cadr tree))

(defn symbols [tree]
  (cond
    [(leaf? tree) (symbol-leaf tree)]
    [(not (isinstance tree list)) []]
    [(caddr tree)]))

(defn weight [tree]
  (if (leaf? tree)
      (weight-leaf tree)
      (cadddr tree)))

(defn decode [bits tree]
  (defn choose-branch [bit branch]
    (cond
      [(= bit 0) (left-branch branch)]
      [(= bit 1) (right-branch branch)]
      [(print "Wrong bit in sequence:" bit)
       (exit 1)]))

  (defn decode-helper [bits current-branch]
    (if (or (not current-branch) (not bits))
        '()
        (do
          (setv next-branch (choose-branch (car bits) current-branch))
          (if (leaf? next-branch)
              (cons (symbol-leaf next-branch) (decode-helper (cdr bits) tree))
              (decode-helper (cdr bits) next-branch)))))
  (decode-helper bits tree))

(defn encode [data tree]
  (defn find-bitcode-for-symbol [value]
    (defn go-left? [branch]
      (in value (symbols (left-branch branch))))

    (defn find-bitcode-helper [current-branch result]
      (cond
        [(and (leaf? current-branch) (= value (symbol-leaf current-branch))) result]
        [(do
           (setv next-branch (if (go-left? current-branch)
                                 (left-branch current-branch)
                                 (right-branch current-branch)))
           (setv bitcode [(if (go-left? current-branch)
                              0
                              1)])
           (find-bitcode-helper next-branch (+ result bitcode)))]))

    (find-bitcode-helper tree []))

  (defn encode-helper [bits data]
    (cond
      [(not data) bits]
      [(encode-helper (+ bits (find-bitcode-for-symbol (car data))) (cdr data))]))

  (encode-helper [] data))

(defn create-haffman-tree [initial-data]
  (defn generate-leafs-weights [leafs]
    (setv weights {})
    (for [leaf leafs]
      (.__setitem__ weights (car leaf) (+ 1 (.get weights (car leaf) 0))))
    weights)

  (defn generate-leafs [leafs]
    (setv result [])
    (for [leaf-weight (.items (generate-leafs-weights leafs))]
      (.append result (make-leaf (car leaf-weight) (cadr leaf-weight))))
    result)

  (defn create-haffman [leafs]
    (.sort leafs :key (fn [leaf] (weight leaf)))
    (while (> (len leafs) 1)
      (setv merged-leafs (make-code-tree (.pop leafs) (.pop leafs)))
      (.append leafs merged-leafs)
      (.sort leafs :key (fn [leaf] (weight leaf))))
    leafs)

  (create-haffman (generate-leafs initial-data)))


(setv haffman-tree (create-haffman-tree ['A 'A 'A 'A 'A 'A 'A 'A 'B 'B 'B 'C 'D 'E 'F 'G 'H]))
(setv data ['A 'B 'C 'D 'D 'A 'A 'A])
(setv encoded (encode data haffman-tree))
(setv decoded (decode encoded haffman-tree))

(print data "->" decoded) ;; ['A', 'B', 'C', 'D', 'D', 'A', 'A', 'A'] -> ('A' 'B' 'C' 'D' 'D' 'A' 'A' 'A')
(assert (= data decoded))
