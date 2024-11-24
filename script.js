document.getElementById("resumeForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // Prevent default form submission behavior

    const fileInput = document.getElementById("resumeUpload");
    const resultsDiv = document.getElementById("results");
    const formData = new FormData();

    // Ensure a file is selected
    if (fileInput.files.length === 0) {
        alert("Please upload a resume file.");
        return;
    }

    formData.append("resume", fileInput.files[0]);

    try {
        const response = await fetch("http://127.0.0.1:5000/analyze", {
            method: "POST",
            body: formData,
        });
        console.log(response, 'response')
        if (!response.ok) {
            const errorData = await response.json();
            // throw new Error(errorData.error || `HTTP error! Status: ${response.status}`);
        }

        const result = await response.json();

        // Update the UI with analysis results
        resultsDiv.innerHTML = `
            <h2>Analysis Results:</h2>
            <p><strong>Skills Found:</strong> ${result.skills.length > 0 ? result.skills.join(", ") : "None"}</p>
            <p><strong>Resume Length:</strong> ${result.word_count} words</p>
        `;
    } catch (error) {
        console.log("Error fetching data:", error);
        console.error("Error fetching data:", error);
        // alert(`Failed to analyze the resume: ${error.message}`);
        // resultsDiv.innerHTML = `<p class="error">Error: ${error.message}</p>`;
    }
});
