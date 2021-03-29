from ursina import *
from consts.PieceType import PieceType

class Piece(Entity):
    def __init__(self, board, type):
        super().__init__(
            parent=board.item_parent,
            origin= (-.5, .5),
            position= (5,-0+3),
            color= color.random_color(),
            z=-.1
        )
        
        self.board = board
        self.pieces = []
        self.pieceType = type
        self.rotatePiece = 0
        self.renderType()
        
        self.freezed = False
        self.fallingY = self.position[1]+1
        self.fallingSpeed = 1
        self.moveX = self.position[0]
    
    def clearPieces(self):
        for x in self.pieces:
            x.disable()
        self.pieces = []
    
    def renderType(self):
        self.clearPieces()
        typeMap = PieceType[self.pieceType][self.rotatePiece]
        self.x_offset = len(typeMap[0]) -1
        self.y_offset = len(typeMap) - 1
        for y in range(len(typeMap)):
            for x in range(len(typeMap[y])):
                if typeMap[y][x] == 1:
                    self.pieces.append(
                        Entity(
                            parent= self,
                            model = 'quad',
                            origin= (-.5, .5),
                            texture= 'white_cube',
                            color= self.color,
                            position= (x,-y)
                        )
                    )

    def update(self):
        if not self.freezed:
            self.fall()
            self.move()
    
    def input(self,key):
        if not self.freezed:
            self.rotate(key)
        
    def rotate(self,key):
        if key == 'q up':
            self.rotatePiece -= 1
        if key == 'e up':
            self.rotatePiece += 1
            
        if self.rotatePiece >= len(PieceType[self.pieceType]):
            self.rotatePiece = 0
        elif self.rotatePiece < 0:
            self.rotatePiece = len(PieceType[self.pieceType]) - 1
            
        self.renderType()
        
    def move(self):
        if held_keys['s']:
            self.fallingSpeed = 10
        else:
            self.fallingSpeed = 1
    
        self.moveX += held_keys['d'] * time.dt * 5
        self.moveX -= held_keys['a'] * time.dt * 5
        
        if self.moveX + self.x_offset >= 10:
            self.moveX = 9 - self.x_offset
        if self.moveX + self.x_offset + 1 <= -1:
            self.moveX = 0
    
        if self.moveX - self.x_offset <= 9 and self.moveX + self.x_offset + 1 >= 0:
            self.x = int(self.moveX)
        
    def freeze(self):
        if not self.freezed:
            self.freezed = True
            self.board.generatePiece()
    
    def fall(self):
        if self.y - self.y_offset <= -17:
            self.freeze()
        self.fallingY -= time.dt * self.fallingSpeed
        self.y = int(self.fallingY)