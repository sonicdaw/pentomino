# coding: utf-8
import numpy as np



# すべてのピース形状をPieceオブジェクトの配列に保存する
class Piece:
    def __init__(self, s, h,m,n):
        a = np.array(map(int, s)).reshape(h, -1)
        self.used = False
        self.form = []
        for i in range(m):
            for j in range(n):
                self.form.append((a, a.argmax()))
                a = np.rot90(a)
            a = np.fliplr(a)

pp = [Piece('010111010', 3,1,1),
      Piece('111101',    2,1,4),
      Piece('110011001', 3,1,4),
      Piece('110011010', 3,1,2),
      Piece('110010011', 3,2,2),
      Piece('111110',    2,2,4),
      Piece('11100011',  2,2,4),
      Piece('11110100',  2,2,4),
      Piece('111010010', 3,1,4),
      Piece('11111000',  2,2,4),
      Piece('111100100', 3,1,4),
      Piece('11111',     1,1,2)]



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
        if lvl == 11:
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
