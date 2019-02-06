{- three-deck monte
https://fivethirtyeight.com/features/can-you-escape-a-maze-without-walls/

You meet someone on a street corner who’s standing at a table on which there
are three decks of playing cards. He tells you his name is “Three Deck Monte.”
Knowing this will surely end well, you inspect the decks. Each deck contains
12 cards:
-- Red Deck: four aces, four 9s, four 7s
-- Blue Deck: four kings, four jacks, four 6s
-- Black Deck: four queens, four 10s, four 8s

The man offers you a bet: You pick one of the decks, he then picks a different
one. You both shuffle your decks, and you compete in a short game similar to
War. You each turn over cards one at a time, the one with a higher card wins
that turn (aces are high), and the first to win five turns wins the bet. (There
can’t be ties, as no deck contains any of the same cards as any other deck.)

Should you take the bet? After all, you can pick any of the decks, which seems
like it should give you an advantage against the dealer. If you take the bet,
and the dealer picks the best possible counter deck each time, how often will
you win?
-}

import Control.Monad
import Control.Monad.Random.Class
import System.Random.Shuffle

data Card = Six | Seven | Eight | Nine | Ten | Jack | Queen | King | Ace
          deriving (Eq, Show, Ord)

red_deck :: [Card]
red_deck = concat $ (replicate 4) <$> [Seven, Nine, Ace]

blue_deck :: [Card]
blue_deck = concat $ (replicate 4) <$> [Six, Jack, King]

black_deck :: [Card]
black_deck = concat $ (replicate 4) <$> [Eight, Ten, Queen]

score :: Ord a => [a] -> [a] -> (Int, Int)
score a b =
    foldl
        (\(a_score, b_score) (a, b) ->
            if a > b then (a_score + 1, b_score)
            else (a_score, b_score + 1))
        (0, 0)
        (zip (take 9 a) (take 9 b))

count_win :: Int -> ([Card], [Card]) -> Int
count_win acc (a, b) =
    let (a_score, b_score) = score a b in
    if a_score > b_score then acc + 1 else acc

win_probability :: Fractional a => [[Card]] -> [[Card]] -> a
win_probability as bs =
    let num_a_wins = foldl
                        (\acc (a, b) -> count_win acc (a, b))
                        0
                        (zip as bs)
    in
    (fromIntegral num_a_wins / fromIntegral (length as))

decks :: MonadRandom m => Int -> [Card] -> m [[Card]]
decks n deck = sequence $ map shuffleM (replicate n deck)

deck_vs :: (MonadRandom m, Fractional a) => [Card] -> [Card] -> Int -> m a
deck_vs a b n = liftM2 win_probability (decks n a) (decks n b)

red_vs_blue :: (MonadRandom m, Fractional a) => Int -> m a
red_vs_blue = deck_vs red_deck blue_deck

red_vs_black :: (MonadRandom m, Fractional a) => Int -> m a
red_vs_black = deck_vs red_deck black_deck

blue_vs_black :: (MonadRandom m, Fractional a) => Int -> m a
blue_vs_black = deck_vs blue_deck black_deck
