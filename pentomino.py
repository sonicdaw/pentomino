# coding: utf-8
import numpy as np



# すべてのピース形状をPieceオブジェクトの配列に保存する
class Piece:
    def __init__(self, s, h):
        a = np.array(map(int, s)).reshape(h, -1)
        self.used = False
        self.form = []
        for i in range(2):
            for j in range(4):
                match = False
                for k in self.form:
                    piece_matrix, piece_origin = k
                    if len(a) == len(piece_matrix) and len(a[0]) == len(piece_matrix[0]):
                        if np.allclose(a, piece_matrix):
                            match = True
                if match == False:
                    self.form.append((a, a.argmax()))
                    print a
                a = np.rot90(a)
            print
            a = np.fliplr(a)

pp = [Piece('11111000', 	2),
      Piece('111100010001', 3),
      Piece('11111100', 	2),
      Piece('111101', 		3),
      Piece('100100111', 	3),
      Piece('001111',    	2),
      Piece('1011',  		2),
      Piece('0000111111', 	2)]



# パズルの解を求める
def piece_all(pp):
    for piece_i, piece in enumerate(pp):
        if not piece.used:
            for form_j, form in enumerate(piece.form):
                piece_matrix, piece_origin = form
                yield piece_i, form_j, piece_matrix, piece_origin

def chk(board, pp, x, y, lvl):
    global counter
    board_h, board_w = board.shape
    for i, j, piece_matrix, piece_origin in piece_all(pp):
        h, w = piece_matrix.shape
        ox = x - piece_origin
        # ピースが飛び出したらそこから先は見ない
        if ox < 0 or ox + w > board_w or y + h > board_h: continue
        board_section = board[y:y + h, ox:ox + w]
        # ピースがかぶったらそこから先は見ない
        if (board_section * piece_matrix).any(): continue
        # ピースを置く
        board_section += piece_matrix * (i + 1)
        pp[i].used = True
        # すべてのピースを置ききったらTrueを返す（recursiveコールの終了）
        if lvl == len(pp) - 1:
            counter += 1
            print 'No', counter
            print np.rot90(board)
            print
            # ピースを戻す
            board_section -= piece_matrix * (i + 1)
            pp[i].used = False
            return True
        # 次のピースを試す
        k = board.argmin()
        chk(board, pp, k % board_w, k // board_w, lvl + 1)
        # ピースを戻す
        board_section -= piece_matrix * (i + 1)
        pp[i].used = False
    return False

counter = 0
board = np.zeros((10, 6))
chk(board, pp, 0, 0, 0)
print '解合計', counter
