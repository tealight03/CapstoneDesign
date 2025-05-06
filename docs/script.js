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

        // 이모지 기준으로 보고서 내용 분할
        const sections = coreReport.split(/\n(?=📌|💣|🛠|✅)/).filter(Boolean);

        // 마크다운 렌더링 + 구역마다 <hr>로 구분
        const parsedSections = sections.map(section => marked.parse(section.trim())).join("<hr>");

        resultBox.innerHTML = `
            <h3>🛡️ <strong>${data.prediction}</strong></h3>
            <h3>🔖 <strong>라벨:</strong> ${data.label}</h3>
            <h3>📊 <strong>보안 점수:</strong> ${data.security_score}</h3>
            <h3>📄 보안 분석 리포트</h3>
            ${parsedSections}
        `;
    } catch (error) {
        resultBox.textContent = "❌ 오류: " + error.message;
    } finally {
        loading.classList.add("hidden");
    }
}