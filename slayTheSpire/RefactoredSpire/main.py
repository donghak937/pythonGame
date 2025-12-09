# -*- coding: utf-8 -*-
"""
Slay the Spire - 게임 실행 파일

실행 방법: python main.py
"""

import sys
import io

# 인코딩 설정 (Windows 콘솔 한글 출력용)
sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

from game import Game


def main():
    """게임 시작"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
