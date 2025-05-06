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

        // 이모지 기준으로 구역 분할
        const sections = coreReport.split(/\n(?=💣|🛠|✅)/).filter(Boolean);

        // 맨 앞 섹션에만 📌 이모지를 수동으로 붙임
        if (sections.length > 0) {
            sections[0] = "📌 " + sections[0].trim();
        }

        // 섹션을 카드 형식으로 예쁘게 표현
        const parsedSections = sections.map(section => `
            <div class="section-card">
                ${marked.parse(section.trim())}
            </div>
        `).join("");

        // 전체 결과 출력
        resultBox.innerHTML = `
            <div class="summary">
                <strong>🛡️ 예측 결과:</strong> ${data.prediction}<br>
                <strong>🔖 라벨:</strong> ${data.label}<br>
                <strong>📊 보안 점수:</strong> ${data.security_score}<br>
                <strong>📄 보안 분석 리포트:</strong>
            </div>
            ${parsedSections}
        `;
    } catch (error) {
        resultBox.textContent = "❌ 오류: " + error.message;
    } finally {
        loading.classList.add("hidden");
    }
}