
const API_URL = "http://127.0.0.1:5000/predict";

const SYMPTOMS = [
  { key: "bodypain", label: "Body pain" },
  { key: "hollow", label: "Hollow" },
  { key: "cold_and_cough", label: "Cold and cough" },
  { key: "cough", label: "Cough" },
  { key: "chest_pain", label: "Chest pain" },
  { key: "breathing_problem", label: "Breathing problem" },
  { key: "throat_pain", label: "Throat pain" },
  { key: "head_pain", label: "Head pain" },
  { key: "stomach_pain", label: "Stomach pain" },
  { key: "diarrhea", label: "Diarrhea" },
  { key: "omitting", label: "Vomiting" },
  { key: "back_pain", label: "Back pain" },
  { key: "swollen_feet", label: "Swollen feet" },
];


const form = document.getElementById("form");
const ageInput = document.getElementById("age");
const genderInput = document.getElementById("gender");
const feverInput = document.getElementById("fever");
const feverValue = document.getElementById("fever-value");
const thermo = document.getElementById("thermo");
const symptomsBox = document.getElementById("symptoms");
const countText = document.getElementById("count");
const predictButton = document.getElementById("predict");
const resetButton = document.getElementById("reset");


const states = {
  empty: document.getElementById("state-empty"),
  loading: document.getElementById("state-loading"),
  error: document.getElementById("state-error"),
  result: document.getElementById("state-result"),
};


function showState(name) {

  Object.entries(states).forEach(([key, node]) => {
    node.hidden = key !== name;
  });

}


function buildSymptomChips() {

  SYMPTOMS.forEach((symptom) => {

    const chip = document.createElement("button");

    chip.type = "button";
    chip.className = "chip";
    chip.textContent = symptom.label;
    chip.dataset.key = symptom.key;
    chip.setAttribute("aria-pressed", "false");


    chip.addEventListener("click", () => {

      const pressed =
        chip.getAttribute("aria-pressed") === "true";

      chip.setAttribute(
        "aria-pressed",
        String(!pressed)
      );

      updateCount();

    });


    symptomsBox.appendChild(chip);

  });

}


function updateCount() {

  const selected =
    symptomsBox.querySelectorAll(
      '[aria-pressed="true"]'
    ).length;


  countText.textContent =
    selected === 0
      ? "None selected."
      : `${selected} selected.`;

}


function updateThermometer() {

  const value = Number(feverInput.value);
  const min = Number(feverInput.min);
  const max = Number(feverInput.max);


  const percent =
    ((value - min) / (max - min)) * 100;


  feverValue.textContent = value;

  thermo.style.setProperty(
    "--pct",
    `${percent}%`
  );


  thermo.classList.toggle(
    "warm",
    value >= 100 && value <= 102
  );


  thermo.classList.toggle(
    "hot",
    value >= 103
  );

}


function buildPayload() {

  const payload = {

    age: Number(ageInput.value),

    gender: Number(genderInput.value),

    fever: Number(feverInput.value),

  };


  symptomsBox
    .querySelectorAll(".chip")
    .forEach((chip) => {

      payload[chip.dataset.key] =
        chip.getAttribute("aria-pressed") === "true"
          ? 1
          : 2;

    });


  return payload;

}


function showError(message) {

  document.getElementById(
    "error-text"
  ).textContent = message;

  showState("error");

}


function percent(value) {

  return `${(value * 100).toFixed(1)}%`;

}
function getConfidenceColor(value) {
  const confidence = value * 100;

  if (confidence < 40) {
    return "linear-gradient(90deg, #ef4444, #f87171)";
  }

  else if (confidence <= 70 && confidence >= 40) {
    return "linear-gradient(90deg, #f59e0b, #fbbf24)";
  }

  return "linear-gradient(90deg, #22c55e, #86efac)";
}

function showResult(data) {

  const results = Array.isArray(data.top)
    ? data.top
    : [];


  if (results.length === 0) {

    showError(
      "No prediction was returned by the server."
    );

    return;

  }


  const priorityResults = results
    .filter(
      (item) =>
        item &&
        item.condition &&
        typeof item.probability === "number"
    )
    .sort(
      (a, b) =>
        b.probability - a.probability
    )
    .slice(0, 3);


  if (priorityResults.length === 0) {

    showError(
      "No valid prediction was returned by the server."
    );

    return;

  }


  const first = priorityResults[0];


  document.getElementById(
    "condition"
  ).textContent = first.condition;


  document.getElementById(
    "confidence-value"
  ).textContent =
    percent(first.probability);


  const mainBar =
    document.getElementById(
      "confidence-bar"
    );


  mainBar.style.width = "0";


  requestAnimationFrame(() => {

    mainBar.style.width =
      `${Math.max(
        first.probability * 100,
        1
      )}%`;

  });


  const othersSection =
    document.getElementById(
      "others-section"
    );


  const others =
    document.getElementById(
      "others"
    );


  others.replaceChildren();


  const alternatives =
    priorityResults.slice(1);


  othersSection.hidden =
    alternatives.length === 0;


  alternatives.forEach(
    (item, index) => {

      const li =
        document.createElement("li");


      const row =
        document.createElement("div");


      row.className = "row";


      const name =
        document.createElement("span");


      name.textContent =
        `Priority ${index + 2}: ${item.condition}`;


      const value =
        document.createElement("span");


      value.textContent =
        percent(item.probability);


      row.append(
        name,
        value
      );


      const bar =
        document.createElement("div");


      bar.className = "bar";


      const fill =
        document.createElement("span");
      fill.style.background = getConfidenceColor( item.probability );


      bar.appendChild(fill);


      li.append(
        row,
        bar
      );


      others.appendChild(li);


      requestAnimationFrame(() => {

        fill.style.width =
          `${Math.max(
            item.probability * 100,
            1
          )}%`;

      });

    }
  );


  showState("result");

}


async function handleSubmit(event) {

  event.preventDefault();


  const age =
    Number(ageInput.value);


  if (
    !Number.isInteger(age) ||
    age < 15 ||
    age > 95
  ) {

    ageInput.classList.add(
      "invalid"
    );

    ageInput.focus();

    showError(
      "Enter an age between 15 and 95."
    );

    return;

  }


  ageInput.classList.remove(
    "invalid"
  );


  predictButton.disabled = true;


  showState("loading");


  try {

    const response =
      await fetch(API_URL, {

        method: "POST",

        headers: {
          "Content-Type":
            "application/json",
        },

        body:
          JSON.stringify(
            buildPayload()
          ),

      });


    const data =
      await response.json();


    if (!response.ok) {

      showError(
        data.error ||
        "The server rejected the request."
      );

      return;

    }


    showResult(data);


  } catch (error) {

    showError(
      "Cannot reach the server. Start the backend with: python app.py"
    );

  } finally {

    predictButton.disabled = false;

  }

}


function handleReset() {

  ageInput.value = 35;

  ageInput.classList.remove(
    "invalid"
  );

  genderInput.value = "1";

  feverInput.value = 101;


  symptomsBox
    .querySelectorAll(".chip")
    .forEach((chip) => {

      chip.setAttribute(
        "aria-pressed",
        "false"
      );

    });


  updateThermometer();

  updateCount();

  showState("empty");

}


buildSymptomChips();

updateThermometer();

updateCount();


feverInput.addEventListener(
  "input",
  updateThermometer
);


form.addEventListener(
  "submit",
  handleSubmit
);


resetButton.addEventListener(
  "click",
  handleReset
);

