import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가하여 app 모듈을 임포트할 수 있도록 설정
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
