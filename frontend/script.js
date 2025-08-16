document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('submitBtn').addEventListener('click', async function () {
        const urlInput = document.getElementById('urlInput').value;
        const outputDiv = document.getElementById('output');

        outputDiv.textContent = '';
        outputDiv.className = '';

        if (!urlInput) {
            outputDiv.textContent = 'Please enter a URL!';
            outputDiv.className = 'error';
            return;
        }

        try {
            outputDiv.textContent = 'Scanning, please wait...';
            outputDiv.className = '';

            const response = await fetch('http://127.0.0.1:5000', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url: urlInput }),
            });

            if (!response.ok) {
                throw new Error('Failed to fetch from backend');
            }

            const result = await response.json();
            if (result && result.results && result.results.length > 0) {
                let message = 'Scan results:\n';
                result.results.forEach((item) => {
                    message += `${item.vulnerability}: ${item.description}\n`;
                });
                outputDiv.textContent = message;
                outputDiv.className = 'success';
            } else {
                outputDiv.textContent = 'No SQL injection vulnerabilities detected.';
                outputDiv.className = 'success';
            }
        } catch (error) {
            outputDiv.textContent = 'Error: Unable to scan the URL.';
            outputDiv.className = 'error';
        }
    });
});