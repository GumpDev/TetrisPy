from ursina import *
from classes.Piece import Piece
from consts.PieceType import PieceTypes

class Board(Entity):
    def __init__(self):
        super().__init__(
            parent= camera.ui,
            model= "quad",
            scale= (.5,1),
            origin= (-.5, .4),
            position= (-.25,.4),
            texture= 'white_cube',
            texture_scale= (10, 20),
            color= color.dark_gray
        )
        
        self.pieces = []
        self.item_parent = Entity(parent=self, scale=(1/10,1/20))
        self.createPiece(type=self.newPiece())
        self.nextPiece = self.newPiece()
        
    def newPiece(self):
        return PieceTypes[random.randint(0, len(PieceTypes) -1)]
    
    def generatePiece(self):
        self.createPiece(self.nextPiece)
        self.nextPiece = self.newPiece()
        
    def createPiece(self, type):
        self.pieces.append(
            Piece(board=self, type=type)
        )