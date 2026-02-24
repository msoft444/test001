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
  const diffDays = diffMs / (24 * 60 * 60 * 1000);
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
