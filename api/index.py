import os
import sys
from urllib.parse import parse_qs

# 프로젝트 루트 경로를 sys.path에 추가하여 app 모듈 임포트
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

class VercelPathFixer:
    """
    Vercel Serverless Function 환경에서 vercel.json rewrite로 인해
    PATH_INFO가 '/api/index.py'로 변조되는 문제를 해결하는 WSGI 미들웨어.
    1. vercel.json의 '__path' 쿼리 파라미터 확인
    2. REQUEST_URI, RAW_URI, HTTP_X_FORWARDED_URI 헤더 확인
    3. 원래 사용자가 요청한 정확한 경로('/', '/generate' 등)로 복원
    """
    def __init__(self, wsgi_app):
        self.wsgi_app = wsgi_app

    def __call__(self, environ, start_response):
        path = environ.get('PATH_INFO', '')
        
        # 1. 쿼리스트링의 __path 파라미터 확인
        query_string = environ.get('QUERY_STRING', '')
        params = parse_qs(query_string)
        if '__path' in params and params['__path']:
            orig_path = '/' + params['__path'][0].lstrip('/')
            environ['PATH_INFO'] = orig_path
        elif path in ('/api/index.py', '/api/index', '/api', '/api/'):
            # 2. 서버 프록시 헤더 확인
            resolved = None
            for key in ('REQUEST_URI', 'RAW_URI', 'HTTP_X_FORWARDED_URI', 'HTTP_X_MATCHED_PATH', 'HTTP_X_ORIGINAL_URI'):
                val = environ.get(key)
                if val:
                    resolved = '/' + val.split('?')[0].lstrip('/')
                    break
            environ['PATH_INFO'] = resolved if resolved else '/'

        return self.wsgi_app(environ, start_response)

# WSGI 미들웨어 등록
app.wsgi_app = VercelPathFixer(app.wsgi_app)
