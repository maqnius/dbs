main :: IO ()
main = do
    putStrLn "Wie heißt du, Fremder? "
    name <- getLine
    putStrLn $ greet name

greet :: String -> String
greet name = "Hallo " ++ name ++ "!"