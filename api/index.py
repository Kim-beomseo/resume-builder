import os
import sys

# 프로젝트 루트 경로를 sys.path에 추가하여 app 모듈 임포트
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class VercelPathFixer:
    """
    Vercel Serverless Function 환경에서 vercel.json rewrite로 인해
    PATH_INFO가 '/api/index.py'로 변조되는 문제를 해결하는 WSGI 미들웨어.
    Vercel이 전달하는 X-Forwarded-Uri 또는 X-Matched-Path 헤더를 읽어
    사용자가 요청한 실제 경로('/', '/generate', '/manifest.json' 등)로 복원합니다.
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        x_forwarded_uri = environ.get('HTTP_X_FORWARDED_URI')
        x_matched_path = environ.get('HTTP_X_MATCHED_PATH')

        if path in ('/api/index.py', '/api/index', '/api', '/api/'):
            if x_forwarded_uri:
                environ['PATH_INFO'] = x_forwarded_uri.split('?')[0]
            elif x_matched_path:
                environ['PATH_INFO'] = x_matched_path.split('?')[0]
            else:
                environ['PATH_INFO'] = '/'

        return self.wsgi_app(environ, start_response)

# WSGI 미들웨어 등록
app.wsgi_app = VercelPathFixer(app.wsgi_app)
