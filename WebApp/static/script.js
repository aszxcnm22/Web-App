const form = document.getElementById('predictionForm');
form.onsubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const values = [...formData.getAll('input_values')].map(v => parseFloat(v));
    const response = await fetch('/predict/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ input_values: values })
    });
    const result = await response.json();
    document.getElementById('predictionResult').textContent = result.prediction;
}