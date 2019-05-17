{-|
https://fivethirtyeight.com/features/how-many-soldiers-do-you-need-to-beat-the-night-king/
At a pivotal moment in an epic battle between the living and the dead, the Night King, head of the army of the dead, raises all the fallen (formerly) living soldiers to join his ranks. This ability obviously presents a huge military advantage, but how big an advantage exactly?

Forget the Battle of Winterfell and model our battle as follows. Each army lines up single file, facing the other army. One soldier steps forward from each line and the pair duels — half the time the living soldier wins, half the time the dead soldier wins. If the living soldier wins, he goes to the back of his army’s line, and the dead soldier is out (the living army uses dragonglass weapons, so the dead soldier is dead forever this time). If the dead soldier wins, he goes to the back of their army’s line, but this time the (formerly) living soldier joins him there. (Reanimation is instantaneous for this Night King.) The battle continues until one army is entirely eliminated.

What starting sizes of the armies, living and dead, give each army a 50-50 chance of winning?
-}

import System.Random
import Control.Monad

battle :: Int -> Int -> IO Int
battle l d = liftM (battle' l d) rs
    where rs :: IO [Int]
          rs = liftM randoms newStdGen
          battle' 0 _ _      = 0 -- dead wins
          battle' _ 0 _      = 1 -- living wins
          battle' l d (r:rs) = if r > 0 then battle' l (d-1) rs -- living wins
                               else if r < 0 then battle' (l-1) (d+1) rs -- dead wins
                               else battle' l d rs -- skip 0s

battleSimulations :: Int -> Int -> Int -> IO ()
battleSimulations l d s =
    do lc <- liftM ((\i -> (fromIntegral i) / (fromIntegral s)) . sum) $ replicateM s (battle l d)
       putStrLn (show l ++ " living soldiers")
       putStrLn (show d ++ " dead soldiers")
       putStrLn (show s ++ " simulations:")
       putStrLn ("Living won: " ++ show (lc * 100) ++ "% of the time")
       putStrLn ("Dead won  : " ++ show ((1-lc) * 100) ++ "% of the time")

