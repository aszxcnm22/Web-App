document.querySelector('.menu-button').addEventListener('click', () => {
    document.getElementById('nav-menu').classList.toggle('active');
});

const typingText = document.getElementById('typing');
if (typingText) {
    const text = "Welcome to Osteoporosis Prediction";
    let index = 0;

    function type() {
        if (index < text.length) {
            typingText.innerHTML += text.charAt(index);
            index++;
            setTimeout(type, 100);
        }
    }
    type();
}

const buttons = document.querySelectorAll('.btn');

buttons.forEach(button => {
    button.addEventListener('mouseover', () => {
        button.style.transform = 'scale(1.1)';
        button.style.transition = 'transform 0.3s ease';
    });

    button.addEventListener('mouseout', () => {
        button.style.transform = 'scale(1)'; 
    });
});

// Scroll Animation
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    sections.forEach(section => {
        const sectionTop = section.getBoundingClientRect().top;
        if (sectionTop < window.innerHeight - 100) {
            section.style.opacity = 1;
            section.style.transform = 'translateY(0)';
            section.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        }
    });
});

const navLinks = document.querySelectorAll('#nav-menu a');
const menuButton = document.querySelector('.menu-button');

navLinks.forEach(link => {
    link.addEventListener('mouseover', () => {
        link.style.transform = 'scale(1.1)';
        link.style.transition = 'transform 0.3s ease';
        link.style.color = '#ff6347';
    });

    link.addEventListener('mouseout', () => {
        link.style.transform = 'scale(1)'; 
        link.style.color = '';
    });
});

menuButton.addEventListener('mouseover', () => {
    menuButton.style.transform = 'scale(1.1)';
    menuButton.style.transition = 'transform 0.3s ease';
    menuButton.style.backgroundColor = '#ff6347';
});

menuButton.addEventListener('mouseout', () => {
    menuButton.style.transform = 'scale(1)';
    menuButton.style.backgroundColor = '';
});

// Form Submission
document.getElementById("predictionForm").addEventListener("submit", async function(event) {
    event.preventDefault();
    const formData = new FormData(event.target);
    const inputValues = Array.from(formData.values()).map(Number);

    try {
        const response = await fetch("/predict/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ input_values: inputValues }),
        });

        const result = await response.json();
        document.getElementById("result").innerHTML = `
            <h2>Prediction: ${result.prediction}</h2>
            <h2>Confidence: ${result.confidence.toFixed(2)}%</h2>
        `;
    } catch (error) {
        console.error("Error:", error);
        document.getElementById("result").innerHTML = `<h2>Error: ${error.message}</h2>`;
    }
});


