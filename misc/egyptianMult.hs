add a 0 = a
add a b = succ (add a (pred b))

dup a = add a a

half a
    | even a    = findMeAHalf a 0
    | odd a     = error "Odd numbers have no whole halfs"
    where findMeAHalf a b
                | a == 2*b  = b
                | otherwise = findMeAHalf a (succ b)

mult _ 0 = 0
mult 0 _ = 0
mult a b
    | even b    = mult (dup a) (half b)
    | odd b     = add a (mult (dup a) (half (pred b)))
