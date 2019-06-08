module TruthTables where

    -- to remove duplicates from a list
    import Data.List (nub)

    data Prop =
          Const Bool
        | Var String
        | Neg Prop
        | And Prop Prop
        | Or Prop Prop
        | Equiv Prop Prop
        | Impl Prop Prop
        deriving (Eq, Show)

    type Attribution = [(String, Bool)]

    -- given a proposition, return a list with all the variables that show up
    collectVars :: Prop -> [String]
    collectVars (Const  _   ) = []
    collectVars (Var    s   ) = [s]
    collectVars (Neg    prop) = nub $collectVars prop
    -- these four patterns are rather annoying
    collectVars (And    p1 p2) = nub $ (collectVars p1) ++ (collectVars p2)
    collectVars (Or     p1 p2) = nub $ (collectVars p1) ++ (collectVars p2)
    collectVars (Equiv  p1 p2) = nub $ (collectVars p1) ++ (collectVars p2)
    collectVars (Impl   p1 p2) = nub $ (collectVars p1) ++ (collectVars p2)

    -- given a list of variables, returns a list with all possible attributions
    varAttributions :: [String] -> [Attribution]
    --varAttributions vars = map (zipWith (,) vars) tables
    varAttributions vars = map (zip vars) tables
        where
            tables = allTruthTables $ length vars

    -- generates all 2^n truth tables for n variables
    allTruthTables :: Int -> [[Bool]]
    allTruthTables 0 = [[]]
    allTruthTables n = ((True:) <$> prevTables) ++ ((False:) <$> prevTables)
        where
            prevTables = allTruthTables (n-1)

    -- given a proposition and an attribution, return its truth value
    -- (TODO) could be nice to implement the binary operators with short-circuiting logic
    truthValue :: Prop -> Attribution -> Maybe Bool
    truthValue (Const bool) _ = Just bool
    truthValue (Var   v   ) attrs = lookup v attrs
    truthValue (Neg   p   ) attrs = not <$> (truthValue p attrs)
    truthValue (And   p1 p2) attrs = (&&) <$> (truthValue p1 attrs) <*> (truthValue p2 attrs)
    truthValue (Or    p1 p2) attrs = (||) <$> (truthValue p1 attrs) <*> (truthValue p2 attrs)
    truthValue (Equiv p1 p2) attrs = (==) <$> (truthValue p1 attrs) <*> (truthValue p2 attrs)
    -- maybe it is cheating, but b1 <= b2 as "less than or equal to" evaluates to the same thing
    -- as "b1 implies b2"!
    truthValue (Impl  p1 p2) attrs = (<=) <$> (truthValue p1 attrs) <*> (truthValue p2 attrs)

    -- given a proposition, evaluate it at all of its attributions
    extensiveEvaluation :: Prop -> [Bool]
    extensiveEvaluation prop = unwrap values
        where
            vars = collectVars prop
            attributions = varAttributions vars
            -- use sequence to make this [Maybe Bool] a Maybe [Bool]
            values = sequence $ map (truthValue prop) attributions
            unwrap (Just j) = j
            -- if "attributions" is calculated with my varAttributions then "truthValue"
            -- will never return a Nothing, so that "map (truthValue prop) attributions" is
            -- a list of a lot of (Just bool) and no Nothing shows up
            unwrap Nothing = error "everything just crashed!"

    -- checks if a given proposition is a tautology
    tautology :: Prop -> Bool
    tautology = and . extensiveEvaluation

    -- attempts to find an attribution that sets the proposition to false
    falsify :: Prop -> Maybe Attribution
    falsify prop = lookup (Just False) valuesWithAttrs
        where
            vars = collectVars prop
            attributions = varAttributions vars
            values = map (truthValue prop) attributions
            valuesWithAttrs = zip values attributions

    -- attemps to find an attribution that sets the proposition to true
    truthify :: Prop -> Maybe Attribution
    truthify prop = lookup (Just True) valuesWithAttrs
        where
            vars = collectVars prop
            attributions = varAttributions vars
            values = map (truthValue prop) attributions
            valuesWithAttrs = zip values attributions

    {- Show that the "and", "or" and "equivalence"
        operators can be built with negations and implications;
        The only "Equiv" propositions allowed are the middle one
        that actually check if the two sides are equal -}
    -- P v Q <=> (~P => Q)
    prop1 = Equiv
                (Or (Var "P") (Var "Q"))
                (Impl (Neg (Var "P")) (Var "Q"))
    -- P ^ Q <=> ~(P => ~Q)
    prop2 = Equiv
                (And (Var "P") (Var "Q"))
                (Neg (Impl (Var "P") (Neg (Var "Q"))))
    -- (P <=> Q) <=> ~((P => Q) => ~(Q => P))
    prop3 = Equiv
                (Equiv (Var "P") (Var "Q"))
                (Neg (Impl
                        (Impl (Var "P") (Var "Q"))
                        (Neg (Impl (Var "Q") (Var "P")))
                    ))
    -- (P => Q) => [(Q => R) => (P => R)]
    prop4 = Impl
                (Impl (Var "P") (Var "Q"))
                (Impl
                    (Impl (Var "Q") (Var "R"))
                    (Impl (Var "P") (Var "R"))
                )
    -- this should be falsifiable
    -- [P => (Q => (P => Q))] => (P => Q)
    prop5 = Impl
                (Impl (Var "P") (Impl (Var "Q") (Impl (Var "P") (Var "Q"))))
                (Impl (Var "P") (Var "Q"))

    main = do
        print $ tautology prop1
        print $ tautology prop2
        print $ tautology prop3
        print $ tautology prop4
        print $ falsify prop5