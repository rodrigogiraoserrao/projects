module EgyptianMult2 where

    -- | Non-recursive egyptian multiplication algorithm (https://mathspp.com/blog/egyptian-multiplication),
    -- following up on the discussion in the comment section.

    double :: Int -> Int
    double = (2*)

    half :: Int -> Int
    half = flip div 2

    halves :: Int -> [Int]
    halves n = takeWhile (>0) (iterate half n)

    binary :: Int -> [Int]
    binary n = (flip mod 2) <$> halves n

    egyptMult :: Int -> Int -> Int
    egyptMult a n = foldl (\s p -> s + ((fst p)*(snd p))) 0 pairs
        where
            pairs = zip (iterate double a) (binary n)
