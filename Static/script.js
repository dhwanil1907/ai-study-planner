document.getElementById('study-form').addEventListener('submit', async (e) => {
    e.preventDefault();

    const subjects = document.getElementById('subjects').value;
    const deadline = document.getElementById('deadline').value;
    const hours = document.getElementById('hours').value;

    try {
        const response = await fetch('/generate-plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                subjects: subjects,
                deadline: deadline,
                hours_per_day: hours
            })
        });

        const data = await response.json();
        
        if (data.success) {
            displayStudyPlan(data.plan);
            window.location.reload();  // Reload to show saved plans
        } else {
            displayError(data.message);
        }
    } catch (error) {
        displayError('Error generating study plan. Please try again.');
    }
});

function displayStudyPlan(plan) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <div class="bg-white p-6 rounded-lg shadow-md">
            <h2 class="text-2xl font-bold mb-4">Your Study Plan</h2>
            ${plan.map(day => `
                <div class="mb-4">
                    <h3 class="text-lg font-semibold">${day.date}</h3>
                    <ul>
                        ${day.schedule.map(item => `
                            <li class="py-2">${item.time}: ${item.subject} (${item.duration} hours)</li>
                        `).join('')}
                    </ul>
                </div>
            `).join('')}
        </div>
    `;
}

function displayError(message) {
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = `
        <div class="bg-red-100 border-l-4 border-red-500 text-red-700 p-4">
            <p>${message}</p>
        </div>
    `;
}