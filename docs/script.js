async function analyzeCode() {
    const code = document.getElementById("code").value.trim();
    const resultBox = document.getElementById("result");
    const loading = document.getElementById("loading");

    resultBox.innerHTML = "";
    loading.classList.remove("hidden");

    try {
        const response = await fetch("https://ai-powered-code-security-analyzer.onrender.com/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code })
        });

        if (!response.ok) {
            throw new Error("서버 오류가 발생했습니다.");
        }

        const data = await response.json();

        // 📌 이후 내용만 남기고 앞부분 제거
        const coreReport = data.report.split("📌")[1] || "";

        // 보고서 구역을 이모지 기준으로 분할 (📌는 제외)
        const sections = coreReport.split(/\n(?=💣|🛠|✅)/).filter(Boolean);

        // 맨 앞에만 📌 붙이기
        if (sections.length > 0) {
            sections[0] = "📌 " + sections[0].trim();
        }

        // 분석 정보 요약(예측 결과/라벨/보안 점수)
        const headerSection = `
            <div class="section-card">
                <h3>🛡️ 예측 결과: ${data.prediction}</h3>
                <h3>🔖 라벨: ${data.label}</h3>
                <h3>📊 보안 점수: ${data.security_score}</h3>
            </div>
        `;

        // 카드 섹션으로 내용 구성
        const parsedSections = sections.map(section => `
            <div class="section-card">
                ${marked.parse(section.trim())}
            </div>
        `).join("");

        // 전체 결과 출력
        resultBox.innerHTML = `
            ${headerSection}
            ${parsedSections}
        `;
    } catch (error) {
        resultBox.textContent = "❌ 오류: " + error.message;
    } finally {
        loading.classList.add("hidden");
    }
}