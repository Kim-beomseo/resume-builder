# 🚀 AI Resume & Portfolio Builder

> Google Gemini AI가 당신의 경험을 세상에서 가장 빛나는 이력서 & 포트폴리오로 만들어드립니다.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=for-the-badge&logo=flask)
![Gemini API](https://img.shields.io/badge/Gemini-API-orange?style=for-the-badge&logo=google)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

---

## 📌 프로젝트 소개

**AI Resume & Portfolio Builder**는 사용자가 이름, 지원 직무, 경력, 프로젝트 경험, 작성 어조를 입력하면 Google Gemini AI가 즉시 완성도 높은 이력서와 포트폴리오 초안을 자동으로 작성해 주는 풀스택 웹 애플리케이션입니다.

코딩을 처음 배우는 초보자부터 개발자, 기획자, 디자이너까지 누구나 손쉽게 전문적인 취업 서류를 작성할 수 있습니다.

---

## ✨ 주요 기능

| 기능 | 설명 |
|------|------|
| 📝 정보 입력 폼 | 이름, 직무, 경력, 프로젝트, 어조(Tone) 입력 |
| 🤖 AI 자동 생성 | Google Gemini API가 맞춤형 이력서 & 포트폴리오 작성 |
| 🎨 2가지 Prompt 모드 | Prompt A (일반 멘토) / Prompt B (전문가 헤드헌터 STAR 기법) |
| 📋 원클릭 복사 | 서식(Rich Text)이 살아있는 스마트 클립보드 복사 |
| 💾 Markdown 다운로드 | `.md` 파일로 즉시 저장 |
| ✅ 이중 입력 검증 | Frontend + Backend 양쪽 검증으로 오류 원천 차단 |
| 🔒 보안 API Key 관리 | `.env` 파일로 API Key 안전하게 분리 관리 |
| 📊 백엔드 로깅 | 모든 요청/응답/오류 실시간 터미널 기록 |

---

## 📁 프로젝트 구조

```
resume-builder/
├── app.py                  # Flask 백엔드 서버 (핵심 API 로직)
├── requirements.txt        # 필요한 Python 패키지 목록
├── .env                    # 🔒 비밀 API Key 저장 (Git 미포함)
├── .env.example            # API Key 형식 견본 파일
├── .gitignore              # Git 제외 항목 설정
├── templates/
│   └── index.html          # 메인 웹 화면 (HTML)
└── static/
    ├── css/
    │   └── style.css       # 블랙 & 골드 럭셔리 스타일시트
    └── js/
        └── app.js          # 프론트엔드 동작 (Fetch API, 복사, 다운로드)
```

---

## 🛠️ 사용 기술 스택

- **Backend**: `Python 3.10+`, `Flask 3.x`
- **AI**: `Google Gemini API` (`google-genai`)
- **Frontend**: `HTML5`, `CSS3`, `Vanilla JavaScript`
- **Markdown 렌더링**: `marked.js` (CDN)
- **환경변수 관리**: `python-dotenv`

---

## ⚡ 빠른 시작 (Quick Start)

### 1. 저장소 클론
```bash
git clone https://github.com/your-username/resume-builder.git
cd resume-builder
```

### 2. 가상환경 생성 및 활성화 (Windows PowerShell)
```powershell
py -m venv venv
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
.\venv\Scripts\Activate.ps1
```

### 3. 패키지 설치
```powershell
py -m pip install -r requirements.txt
```

### 4. 환경변수 설정
`.env.example`을 복사하여 `.env` 파일을 만들고, 실제 API Key를 입력합니다.
```powershell
Copy-Item .env.example .env
notepad .env
```

```env
GEMINI_API_KEY=여기에_실제_Gemini_API_Key_입력
```

> **Gemini API Key 발급**: [Google AI Studio](https://aistudio.google.com/app/apikey) 에서 무료로 발급받을 수 있습니다.

### 5. 서버 실행
```powershell
py app.py
```

### 6. 브라우저 접속
```
http://127.0.0.1:5000
```

---

## 🎯 사용 방법

1. 브라우저에서 `http://127.0.0.1:5000`에 접속합니다.
2. 왼쪽 입력 폼에 이름, 지원 직무, 경력, 프로젝트 경험을 입력합니다.
3. 작성 어조(Tone)와 Prompt 모드(A/B)를 선택합니다.
4. **[✨ 이력서 & 포트폴리오 생성하기]** 버튼을 클릭합니다.
5. AI가 작성하는 동안(약 5~15초) 로딩 스피너가 표시됩니다.
6. 오른쪽 결과창에 완성된 이력서와 포트폴리오를 확인합니다.
7. **[📋 전체 복사]** 또는 **[💾 Markdown 다운로드]** 버튼으로 결과를 저장합니다.

---

## 💡 Prompt 모드 비교

| 구분 | Prompt A (일반 모드) | Prompt B (전문가 모드) |
|------|------------------|-------------------|
| 스타일 | 친절하고 정돈된 AI 취업 멘토 | 시니어 헤드헌터 & 글로벌 테크 리크루터 |
| 작성 방식 | 깔끔하고 읽기 쉬운 문장 | STAR 기법 + 성과 수치화 |
| 특징 | 초보자, 경력 전환자에게 적합 | 시니어, 고연봉 포지션 지원자에게 적합 |

---

## 🔒 보안 주의사항

- `.env` 파일은 절대로 GitHub에 올리지 마세요. (`.gitignore`에 의해 자동 제외됩니다.)
- Gemini API Key를 소스코드, 채팅창, 공개 저장소에 직접 노출하지 마세요.
- 공개 배포 시에는 반드시 운영 환경의 환경변수(Environment Variables)에 Key를 설정하세요.

---

## 📦 requirements.txt

```
Flask
python-dotenv
google-genai
```

---

## 🤝 기여 방법 (Contributing)

1. 이 저장소를 Fork합니다.
2. 새로운 브랜치를 생성합니다. (`git checkout -b feature/새기능`)
3. 변경사항을 커밋합니다. (`git commit -m "Add 새기능"`)
4. 브랜치에 Push합니다. (`git push origin feature/새기능`)
5. Pull Request를 생성합니다.

---

## 📄 라이선스

이 프로젝트는 [MIT 라이선스](LICENSE)를 따릅니다.

---

## 👨‍💻 만든이

**AI Resume & Portfolio Builder**는 Python, Flask, Gemini API를 학습하는 풀스택 웹 개발 실습 프로젝트입니다.

> 💬 **"당신의 첫 풀스택 AI 웹앱, 이제 세상에 공개할 준비가 되었습니다!"** 🚀
