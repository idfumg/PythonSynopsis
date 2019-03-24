;; (import sys)
;; (sys.setrecursionlimit 15000)

(defn count-change [amount]
  (defn get-denomination [kind]
    (cond
      [(= kind 1) 1]
      [(= kind 2) 5]
      [(= kind 3) 10]
      [(= kind 4) 25]
      [(= kind 5) 50]))

  (defn count-change-iter [amount kinds-of-coins]
    (cond
      [(= amount 0) 1]
      [(or (< amount 0) (= kinds-of-coins 0)) 0]
      [(+ (count-change-iter amount (- kinds-of-coins 1))
          (count-change-iter (- amount (get-denomination kinds-of-coins)) kinds-of-coins))]))

  (count-change-iter amount 5))

(print (count-change 100))
