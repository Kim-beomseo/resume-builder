import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가하여 app 모듈 임포트
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, VercelPathFixer

# Vercel Serverless Function WSGI entry point
app.wsgi_app = VercelPathFixer(app.wsgi_app)

