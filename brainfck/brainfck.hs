module Brainfck where

    mem_size = 256
    
    interpret :: String -> String -> ([Int], Int, [Int], String, String)
    interpret code inp = evaluate code memLeft ptr memRight inp out
        where
            memLeft = []
            memRight = []
            ptr = 0
            out = ""

    evaluate :: String -> [Int] -> Int -> [Int] -> String -> String -> ([Int], Int, [Int], String, String)
    {- EOF reached -}
    evaluate         "" memLeft ptr memRight     inp out = (memLeft, ptr, memRight, inp, out)

    {- patterns to read input -}
    evaluate (',':code) memLeft ptr memRight      "" out = evaluate code memLeft ptr' memRight inp' out
        where
            ptr' = 0
            inp' = ""
    evaluate (',':code) memLeft ptr memRight (c:inp) out = evaluate code memLeft ptr' memRight inp out
        where ptr' = (mod (fromEnum c) mem_size)

    {- pattern to write output -}
    evaluate ('.':code) memLeft ptr memRight     inp out = evaluate code memLeft ptr memRight inp out'
        where out' = out ++ [toEnum ptr :: Char]

    {- patterns to go left on the memory tape -}
    evaluate ('<':code)      [] ptr memRight     inp out = evaluate code memLeft' ptr' memRight' inp out
        where
            memLeft' = []
            ptr' = 0
            memRight' = ptr:memRight
    evaluate ('<':code) memLeft ptr memRight     inp out = evaluate code memLeft' ptr' memRight' inp out
        where
            memLeft' = reverse (drop 1 $ reverse memLeft)
            ptr' = (head.reverse) memLeft
            memRight' = ptr:memRight

    {- patterns to go right on the memory tape -}
    evaluate ('>':code) memLeft ptr       []     inp out = evaluate code memLeft' ptr' memRight' inp out
        where
            memLeft' = memLeft ++ [ptr]
            ptr' = 0
            memRight' = []
    evaluate ('>':code) memLeft ptr memRight     inp out = evaluate code memLeft' ptr' memRight' inp out
        where
            memLeft' = memLeft ++ [ptr]
            ptr' = head memRight
            memRight' = tail memRight

    {- pattern to deal with the loops -}
    evaluate ('[':code) memLeft ptr memRight     inp out = evaluate code' memLeft' ptr' memRight' inp' out'
        where
            (memLeft', ptr', memRight', inp', out') = nest partial memLeft ptr memRight inp out
            {- use `extract` to get the code within [] -}
            extract       _         "" _ = error "Reached EOF while parsing []"
            extract partial (']':code) 1 = (partial, code)
            extract partial (']':code) n = extract (partial ++ "]") code (n-1)
            extract partial ('[':code) n = extract (partial ++ "[") code (n+1)
            extract partial   (c:code) n = extract (partial ++ [c]) code n
            (partial, code') = extract "" code 1
            {- `nest` should run the partial code while the ptr is not 0 -}
            nest partial memLeft   0 memRight inp out = (memLeft, 0, memRight, inp, out)
            nest partial memLeft ptr memRight inp out = let (nestMemLeft, nestPtr, nestMemRight, nestInp, nestOut) = evaluate partial memLeft ptr memRight inp out
                                                        in nest partial nestMemLeft nestPtr nestMemRight nestInp nestOut

    main = do
            putStr " (brainfck input) >> "
            inp <- getLine
            putStrLn $ show $ interpret ",[.,]" inp