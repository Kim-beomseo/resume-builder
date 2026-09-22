import os
import logging
from flask import Flask, render_template, request, jsonify, send_from_directory, make_response
from dotenv import load_dotenv
from google import genai

# .env 파일에서 환경변수 로드
load_dotenv()

# 프로젝트 루트 디렉토리 기준 절대 경로 설정
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask 애플리케이션 생성 (Vercel 환경에서도 경로 보장)
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, 'templates'),
    static_folder=os.path.join(BASE_DIR, 'static')
)

# Backend 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

@app.route('/')
@app.route('/api/index.py')
@app.route('/api/index')
def index():
    """메인 입력 및 결과 페이지 렌더링"""
    return render_template('index.html')

@app.route('/manifest.json')
@app.route('/api/manifest.json')
def manifest():
    """PWA 매니페스트 서빙"""
    return send_from_directory(app.static_folder, 'manifest.json', mimetype='application/manifest+json')

@app.route('/sw.js')
@app.route('/api/sw.js')
def service_worker():
    """PWA Service Worker 서빙 (루트 스코프 허용 헤더 포함)"""
    response = make_response(send_from_directory(app.static_folder, 'sw.js', mimetype='application/javascript'))
    response.headers['Service-Worker-Allowed'] = '/'
    return response

@app.route('/generate', methods=['POST'])
@app.route('/api/generate', methods=['POST'])
def generate():
    """Gemini API를 호출하여 이력서 및 포트폴리오 생성"""
    # 1. 요청 데이터 확인
    data = request.get_json()
    if not data:
        app.logger.warning("Empty request body received")
        return jsonify({"error": "요청 데이터가 올바르지 않습니다."}), 400

    # 2. 백엔드 입력값 검증 (Validation)
    name = data.get('name', '').strip()
    role = data.get('role', '').strip()
    experience = data.get('experience', '').strip()
    projects = data.get('projects', '').strip()
    tone = data.get('tone', '전문적이고 신뢰감 있는').strip()
    prompt_type = data.get('prompt_type', 'A').strip().upper()

    if not name:
        return jsonify({"error": "이름을 입력해 주세요."}), 400
    if not role:
        return jsonify({"error": "지원 직무를 입력해 주세요."}), 400
    if not experience:
        return jsonify({"error": "경력 사항을 입력해 주세요."}), 400
    if not projects:
        return jsonify({"error": "프로젝트 경험을 입력해 주세요."}), 400

    app.logger.info(f"Generation request: Name={name}, Role={role}, PromptType={prompt_type}, Tone={tone}")

    # 3. API Key 로드 및 확인
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        app.logger.error("GEMINI_API_KEY is missing or invalid in .env")
        return jsonify({"error": ".env 파일에 유효한 GEMINI_API_KEY가 설정되지 않았습니다. .env 파일을 확인해 주세요."}), 500

    include_cover = data.get('include_cover', True)

    # 4. 프롬프트 엔지니어링 (스타일리시하고 전문적인 마크다운 템플릿 + 표지 옵션)
    cover_instruction_B = """
# 📘 PROFESSIONAL PORTFOLIO & RESUME
> ### 👤 {name} | Senior {role}
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> 🎯 **Core Identity**: "데이터와 실력으로 비즈니스 임팩트를 증명하는 {role}"  
> 📅 **Submission**: 2026 Confidential Portfolio  
> ✉️ **Contact**: user@career-path.io | 📱 010-XXXX-XXXX  
> 🔗 **Repository**: https://github.com/{name}

---
""".format(name=name, role=role) if include_cover else ""

    cover_instruction_A = """
# 📘 이력서 & 포트폴리오 (Cover Page)
> ### 👤 {name} 지원자
> **지원 분야: {role}**  
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> 🎯 **직무 모토**: "끊임없이 성장하고 기여하는 {role} 인재"  
> 📅 **작성 일자**: 2026년  
> ✉️ **연락처**: candidate@career.net | 📱 010-XXXX-XXXX  

---
""".format(name=name, role=role) if include_cover else ""

    if prompt_type == 'B':
        # Prompt B: 전문가 모드 (시니어 헤드헌터 & 테크 리크루터 관점, STAR 기법 & 수치 성과 중심)
        prompt = f"""
당신은 실리콘밸리 글로벌 기업의 수석 테크 리크루터이자 시니어 커리어 컨설턴트입니다.
아래 지원자의 정보를 바탕으로 인사담당자가 10초 만에 합격을 결정할 수 있을 만큼 **매우 세련되고 전문적인 프리미엄 [이력서 & 포트폴리오]**를 마크다운으로 작성하세요.

[지원자 프로필]
- 이름: {name}
- 지원 직무: {role}
- 경력 사항: {experience}
- 프로젝트 경험: {projects}
- 희망 어조(Tone): {tone}

[출력 서식 가이드라인 - 반드시 이 마크다운 구조를 지켜주세요]
{cover_instruction_B}
# 👤 {name} | {role} Professional Resume & Portfolio

> 💡 **핵심 역량 요약 (Executive Summary)**
> 지원자의 핵심 강점 2~3줄 요약. 비즈니스 임팩트와 차별화된 역량을 압축 제시.

---

## 📋 전문 이력서 (Resume)

### 💼 주요 경력 및 성과 (Professional Experience)
- 경력 사항을 STAR 기법(상황-과제-행동-성과)으로 재구성하여 불릿 포인트로 작성
- 기여한 성과는 반드시 구체적 수치(%, 건수, 시간 단축 등)로 임팩트 있게 강조
- 관련 기술 스택 및 키워드는 `Python`, `FastAPI` 처럼 백틱(`)으로 감싸서 강조

### 🛠️ 핵심 직무 역량 (Core Competencies)
- 주요 직무 스킬 및 도구를 카테고리별로 나누어 백틱(`) 태그로 정리

---

## 💼 포트폴리오 요약 (Portfolio Summary)

### 🚀 [프로젝트명]
- **프로젝트 개요**: 무엇을 해결하기 위해 만든 프로젝트인지 한 줄 설명
- **담당 역할 및 기여도**: 구체적으로 어떤 모듈/문제를 해결했는지 명시
- **핵심 기술 스택**: `기술1`, `기술2`, `기술3`
- **주요 성과 및 정량적 결과**: 수치화된 성과 지표 제시

---
문체는 요청된 '{tone}' 어조를 철저하게 유지하세요.
"""
    else:
        # Prompt A: 일반 모드 (친절하고 신뢰감 높은 AI 취업 멘토 관점)
        prompt = f"""
당신은 친절하고 꼼꼼한 AI 취업 멘토입니다.
아래 지원자의 경험을 바탕으로 인사담당자에게 신뢰감을 주는 **깔끔하고 완성도 높은 [이력서 & 포트폴리오]**를 마크다운으로 작성하세요.

[지원자 프로필]
- 이름: {name}
- 지원 직무: {role}
- 경력 사항: {experience}
- 프로젝트 경험: {projects}
- 희망 어조(Tone): {tone}

[출력 서식 가이드라인 - 반드시 이 마크다운 구조를 지켜주세요]
{cover_instruction_A}
# 👤 {name} | {role} 이력서 & 포트폴리오

> 💡 **한 줄 소개 및 커리어 목표**
> 지원자의 강점과 직무에 대한 열정을 담은 2~3줄 요약 소개글

---

## 📋 이력서 (Resume)

### 💼 경력 사항 (Experience)
- 담당 업무와 기여한 내용을 명확하고 단정한 불릿 포인트로 작성
- 사용한 주요 기술 및 도구는 `Python`, `Excel` 처럼 백틱(`)으로 감싸서 돋보이게 표현

### 🛠️ 보유 기술 및 역량 (Skills)
- 직무 관련 역량과 도구를 정돈하여 제시

---

## 💼 포트폴리오 (Portfolio)

### 🚀 [프로젝트명]
- **소개**: 프로젝트 목적 및 진행 배경
- **담당 업무**: 맡았던 구체적인 역할
- **사용 기술**: `도구1`, `도구2`
- **배운 점 및 성과**: 프로젝트를 통해 이끌어낸 변화와 배운 점

---
문체는 요청된 '{tone}' 어조에 맞추어 따뜻하고 자신감 있게 작성하세요.
"""

    # 5. Gemini API 호출
    try:
        client = genai.Client(api_key=api_key)
        candidate_models = ['gemini-3.6-flash', 'gemini-3.5-flash-lite', 'gemini-3.5-flash']
        response = None
        last_err = None

        for model_name in candidate_models:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                app.logger.info(f"Generated successfully using model: {model_name}")
                break
            except Exception as model_err:
                app.logger.warning(f"모델 {model_name} 호출 실패: {model_err}")
                last_err = model_err

        if not response:
            raise last_err or Exception("사용 가능한 Gemini 모델을 호출할 수 없습니다.")

        result_text = response.text
        app.logger.info("AI generation completed successfully.")
        return jsonify({"result": result_text})

    except Exception as e:
        app.logger.error(f"Gemini API 호출 중 예외 발생: {str(e)}")
        return jsonify({"error": f"AI 생성 중 오류가 발생했습니다: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
