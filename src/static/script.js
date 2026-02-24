function parseDateTime(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return null;
  }
  return date;
}

function calculateDateDifference() {
  const startInput = document.getElementById("start-datetime");
  const endInput = document.getElementById("end-datetime");
  const result = document.getElementById("diff-result");
  const startDate = parseDateTime(startInput.value);
  const endDate = parseDateTime(endInput.value);

  if (!startDate || !endDate) {
    result.textContent = "無効な日時です";
    return;
  }

  const diffMs = endDate.getTime() - startDate.getTime();
  const diffDays = Math.round(diffMs / (24 * 60 * 60 * 1000));
  result.textContent = `差分: ${diffDays} 日`;
}

function calculateOffsetDate() {
  const baseInput = document.getElementById("base-datetime");
  const dayOffsetInput = document.getElementById("day-offset");
  const result = document.getElementById("offset-result");
  const baseDate = parseDateTime(baseInput.value);
  const offset = Number(dayOffsetInput.value);

  if (!baseDate || !Number.isFinite(offset)) {
    result.textContent = "無効な入力です";
    return;
  }

  const newDate = new Date(baseDate.getTime() + offset * 24 * 60 * 60 * 1000);
  result.textContent = `計算結果: ${newDate.toLocaleString("ja-JP")}`;
}

function toggleDarkMode() {
  document.body.classList.toggle("dark-mode");
}

document.getElementById("calculate-diff").addEventListener("click", calculateDateDifference);
document.getElementById("calculate-offset").addEventListener("click", calculateOffsetDate);
document.getElementById("dark-mode-toggle").addEventListener("change", toggleDarkMode);

function updateClock() {
  const now = new Date();
  const seconds = now.getSeconds();
  const minutes = now.getMinutes();
  const hours = now.getHours();

  const secondDegrees = ((seconds / 60) * 360) + 90;
  const minuteDegrees = ((minutes / 60) * 360) + ((seconds/60)*6) + 90;
  const hourDegrees = ((hours / 12) * 360) + ((minutes/60)*30) + 90;

  const secondHand = document.querySelector('.hand.second');
  const minuteHand = document.querySelector('.hand.minute');
  const hourHand = document.querySelector('.hand.hour');

  if(secondHand) secondHand.style.transform = `rotate(${secondDegrees}deg)`;
  if(minuteHand) minuteHand.style.transform = `rotate(${minuteDegrees}deg)`;
  if(hourHand) hourHand.style.transform = `rotate(${hourDegrees}deg)`;
}

setInterval(updateClock, 1000);
updateClock();
