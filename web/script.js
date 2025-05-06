async function analyzeCode() {
    const code = document.getElementById("code").value.trim();
    const resultBox = document.getElementById("result");
    const loading = document.getElementById("loading");

    resultBox.textContent = "";
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

    resultBox.innerHTML = `
        🛡️ <strong>${data.prediction}</strong><br>
        🔖 <strong>라벨:</strong> ${data.label}<br>
        📊 <strong>보안 점수:</strong> ${data.security_score}<br><br>
        📄 <strong>보안 분석 리포트</strong><br><hr>
        <div>${data.report.replace(/\n/g, "<br>")}</div>`;
    } catch (error) {
        resultBox.textContent = "❌ 오류: " + error.message;
    } finally {
        loading.classList.add("hidden");
    }
}  