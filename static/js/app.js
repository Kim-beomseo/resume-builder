/**
 * AI Resume & Portfolio Builder 프론트엔드 자바스크립트
 * - 폼 제출 및 프론트엔드 유효성 검사
 * - /generate REST API 비동기(fetch) 호출
 * - 로딩 애니메이션(Spinner) 제어
 * - 오류 메시지 처리
 * - 결과 표시, 클립보드 복사, 마크다운 파일 다운로드
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. 주요 DOM 엘리먼트 가져오기
    const form = document.getElementById('resume-form');
    const nameInput = document.getElementById('name');
    const roleInput = document.getElementById('role');
    const experienceInput = document.getElementById('experience');
    const projectsInput = document.getElementById('projects');
    const toneSelect = document.getElementById('tone');
    const submitBtn = document.getElementById('submit-btn');

    const errorMessage = document.getElementById('error-message');
    const loadingSpinner = document.getElementById('loading-spinner');
    const resultPlaceholder = document.getElementById('result-placeholder');
    const resultContent = document.getElementById('result-content');
    const themeSelect = document.getElementById('theme-select');
    const copyBtn = document.getElementById('copy-btn');
    const downloadBtn = document.getElementById('download-btn');

    // 테마 실시간 변경 리스너
    if (themeSelect) {
        document.body.className = themeSelect.value;
        themeSelect.addEventListener('change', (e) => {
            document.body.className = e.target.value;
        });
    }

    // 현재 생성된 최신 텍스트 저장용 변수
    let currentGeneratedMarkdown = '';

    // 2. 오류 메시지 표시/숨김 헬퍼 함수
    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('hidden');
    }

    function clearError() {
        errorMessage.textContent = '';
        errorMessage.classList.add('hidden');
    }

    // 3. 폼 제출 이벤트 처리
    form.addEventListener('submit', async (event) => {
        // 기본 폼 제출(새로고침) 방지
        event.preventDefault();
        clearError();

        // [Frontend 입력 검증]
        const name = nameInput.value.trim();
        const role = roleInput.value.trim();
        const experience = experienceInput.value.trim();
        const projects = projectsInput.value.trim();
        const tone = toneSelect.value;
        const promptTypeRadio = document.querySelector('input[name="prompt_type"]:checked');
        const promptType = promptTypeRadio ? promptTypeRadio.value : 'A';

        if (!name) {
            showError('이름을 입력해 주세요.');
            nameInput.focus();
            return;
        }
        if (!role) {
            showError('지원 직무를 입력해 주세요.');
            roleInput.focus();
            return;
        }
        if (!experience) {
            showError('주요 경력 사항을 입력해 주세요.');
            experienceInput.focus();
            return;
        }
        if (!projects) {
            showError('프로젝트 경험을 입력해 주세요.');
            projectsInput.focus();
            return;
        }

        // [로딩 UI 활성화]
        submitBtn.disabled = true;
        submitBtn.textContent = '⏳ AI가 열심히 작성하고 있습니다...';
        copyBtn.disabled = true;
        downloadBtn.disabled = true;

        resultPlaceholder.classList.add('hidden');
        resultContent.classList.add('hidden');
        loadingSpinner.classList.remove('hidden');

        const themeSelect = document.getElementById('theme-select');
        const includeCoverCheckbox = document.getElementById('include-cover');
        const includeCover = includeCoverCheckbox ? includeCoverCheckbox.checked : true;

        try {
            // [백엔드 /generate API 호출]
            const response = await fetch('/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    role: role,
                    experience: experience,
                    projects: projects,
                    tone: tone,
                    prompt_type: promptType,
                    include_cover: includeCover
                })
            });

            const data = await response.json();

            if (!response.ok) {
                // 백엔드에서 반환한 오류 처리 (400 또는 500)
                throw new Error(data.error || '이력서 생성 중 문제가 발생했습니다.');
            }

            // [생성 성공 처리: 마크다운 렌더링]
            currentGeneratedMarkdown = data.result;
            if (typeof marked !== 'undefined') {
                resultContent.innerHTML = marked.parse(currentGeneratedMarkdown);
            } else {
                resultContent.textContent = currentGeneratedMarkdown;
            }

            // UI 상태 전환
            loadingSpinner.classList.add('hidden');
            resultContent.classList.remove('hidden');
            copyBtn.disabled = false;
            downloadBtn.disabled = false;

        } catch (error) {
            // [네트워크 또는 API 오류 처리]
            console.error('Generation Error:', error);
            loadingSpinner.classList.add('hidden');
            resultPlaceholder.classList.remove('hidden');
            showError(error.message || '서버와의 통신에 실패했습니다. 다시 시도해 주세요.');
        } finally {
            // [버튼 상태 원복]
            submitBtn.disabled = false;
            submitBtn.textContent = '✨ 이력서 & 포트폴리오 생성하기';
        }
    });

    // 4. 서식(Rich Text) 및 마크다운 동시 복사 기능
    copyBtn.addEventListener('click', async () => {
        if (!currentGeneratedMarkdown) return;

        try {
            const htmlContent = resultContent.innerHTML;
            const plainText = currentGeneratedMarkdown;

            // 서식을 지원하는 프로그램(워드, 노션, 한글, 이메일)에는 서식 그대로, 메모장에는 마크다운으로 복사
            const blobHtml = new Blob([htmlContent], { type: 'text/html' });
            const blobText = new Blob([plainText], { type: 'text/plain' });
            const dataItem = [new ClipboardItem({
                'text/html': blobHtml,
                'text/plain': blobText
            })];

            await navigator.clipboard.write(dataItem);
            const originalText = copyBtn.textContent;
            copyBtn.textContent = '✅ 서식 복사 완료!';
            setTimeout(() => {
                copyBtn.textContent = originalText;
            }, 2000);
        } catch (err) {
            // 브라우저 권한 등에 의해 실패할 경우 기본 텍스트 복사로 안전하게 fallback
            try {
                await navigator.clipboard.writeText(currentGeneratedMarkdown);
                const originalText = copyBtn.textContent;
                copyBtn.textContent = '✅ 복사 완료!';
                setTimeout(() => {
                    copyBtn.textContent = originalText;
                }, 2000);
            } catch (fallbackErr) {
                console.error('클립보드 복사 실패:', fallbackErr);
                alert('클립보드 복사에 실패했습니다.');
            }
        }
    });

    // 5. Markdown 파일 다운로드 기능
    downloadBtn.addEventListener('click', () => {
        if (!currentGeneratedMarkdown) return;

        // 마크다운 형식의 텍스트 Blob 생성
        const blob = new Blob([currentGeneratedMarkdown], { type: 'text/markdown;charset=utf-8' });
        const downloadUrl = URL.createObjectURL(blob);

        // 가상의 <a> 링크를 생성하여 다운로드 트리거
        const tempLink = document.createElement('a');
        tempLink.href = downloadUrl;
        
        // 파일 이름 지정 (예: 홍길동_이력서_포트폴리오.md)
        const applicantName = nameInput.value.trim() || 'Resume';
        tempLink.download = `${applicantName}_이력서_포트폴리오.md`;

        document.body.appendChild(tempLink);
        tempLink.click();
        document.body.removeChild(tempLink);

        // 메모리 해제
        URL.revokeObjectURL(downloadUrl);
    });

    // 6. PWA Service Worker 등록
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', () => {
            navigator.serviceWorker.register('/sw.js')
                .then((registration) => {
                    console.log('✅ PWA ServiceWorker 등록 완료, scope:', registration.scope);
                })
                .catch((err) => {
                    console.warn('⚠️ PWA ServiceWorker 등록 실패:', err);
                });
        });
    }
});

