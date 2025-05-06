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
    <p>🛡️ <strong>${data.prediction}</strong></p>
    <p>🔖 <strong>라벨:</strong> ${data.label}</p>
    <p>📊 <strong>보안 점수:</strong> ${data.security_score}</p>
    <br>
    <h3>📄 보안 분석 리포트</h3>
    <hr>
    <div>${marked.parse(data.report)}</div>`;

    } catch (error) {
        resultBox.textContent = "❌ 오류: " + error.message;
    } finally {
        loading.classList.add("hidden");
    }
}  