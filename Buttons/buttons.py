import pygame
from Buttons.PromotionButton import PromotionButton

DIMENSION = 8  #8X8 board
HEIGHT = 512
SQ_SIZE = HEIGHT // DIMENSION


whiteQueen = PromotionButton(95,50,80,80)
whiteRock = PromotionButton(175,50,80,80)
whiteBishop = PromotionButton(255,50,80,80)
whiteKnight = PromotionButton(335,50,80,80)

blackQueen = PromotionButton(95,385,80,80)
blackRock = PromotionButton(175,385,80,80)
blackBishop = PromotionButton(255,385,80,80)
blackKnight = PromotionButton(335,385,80,80)
