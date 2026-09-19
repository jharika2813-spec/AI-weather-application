const form = document.querySelector("#weather-form");
const status = document.querySelector("#status");
const card = document.querySelector("#weather-card");
const advice = document.querySelector("#advice");
let currentWeather;

function showError(message) {
  status.textContent = message;
  card.hidden = true;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  status.textContent = "Getting weather…";
  card.hidden = true;
  try {
    const city = new FormData(form).get("city");
    const response = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    currentWeather = data;
    document.querySelector("#place").textContent = `${data.city}, ${data.country}`;
    document.querySelector("#temperature").textContent = data.temperature;
    document.querySelector("#condition").textContent = data.condition;
    document.querySelector("#feels-like").textContent = `${data.feels_like}°C`;
    document.querySelector("#humidity").textContent = `${data.humidity}%`;
    document.querySelector("#wind").textContent = `${data.wind_speed} m/s`;
    const icon = document.querySelector("#icon");
    icon.src = `https://openweathermap.org/img/wn/${data.icon}@2x.png`;
    icon.alt = data.condition;
    advice.textContent = "";
    status.textContent = "";
    card.hidden = false;
  } catch (error) { showError(error.message || "Something went wrong."); }
});

document.querySelector("#advice-button").addEventListener("click", async () => {
  if (!currentWeather) return;
  advice.textContent = "Thinking…";
  try {
    const response = await fetch("/api/advice", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ weather: currentWeather }) });
    const data = await response.json();
    if (!response.ok) throw new Error(data.error);
    advice.textContent = data.advice;
  } catch (error) { advice.textContent = error.message || "Advice is unavailable."; }
});
