const form = document.getElementById("predict-form");
const button = document.getElementById("submit-btn");
const resultBox = document.getElementById("result");
const errorBox = document.getElementById("error");
const marksEl = document.getElementById("marks");
const gradeEl = document.getElementById("grade");
const barFill = document.getElementById("bar-fill");

// Show the live value next to each slider
document.querySelectorAll("input[type='range']").forEach((input) => {
  const output = document.querySelector(`output[data-for='${input.id}']`);
  input.addEventListener("input", () => {
    output.textContent = input.value;
  });
});

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  errorBox.classList.add("hidden");
  button.disabled = true;
  button.textContent = "Predicting...";

  const payload = Object.fromEntries(new FormData(form).entries());

  try {
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || "Something went wrong.");
    }

    marksEl.textContent = data.predicted_marks;
    gradeEl.textContent = data.grade;
    resultBox.classList.remove("hidden");
    // Reset then set width so the bar animates every time
    barFill.style.width = "0";
    requestAnimationFrame(() => {
      barFill.style.width = `${data.predicted_marks}%`;
    });
  } catch (err) {
    resultBox.classList.add("hidden");
    errorBox.textContent = err.message;
    errorBox.classList.remove("hidden");
  } finally {
    button.disabled = false;
    button.textContent = "Predict marks";
  }
});
