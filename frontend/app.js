const conditions = {
  all: {
    title: "Signals differ by condition",
    count: "76 matched pairs",
    delta: "Condition-level differences vary",
    marker: 50,
    summary: "Across conditions, the median paired differences are close to zero. The NLI model’s overall median max-entailment is 0.9980, indicating ceiling saturation."
  },
  hindi: {
    title: "Hindi",
    count: "23 matched pairs",
    delta: "−0.0353 mean difference · median −0.0002",
    marker: 35.3,
    summary: "The factuality-aware prompt had a lower mean max-entailment score in this sample, while the median paired difference was nearly zero. This model score alone does not establish factuality."
  },
  synthetic: {
    title: "Synthetic p100 code-mix",
    count: "23 matched pairs",
    delta: "−0.0025 mean difference · median −0.0005",
    marker: 49.0,
    summary: "Mean and median paired differences were close to zero. The result is exploratory and applies to the selected synthetic p100 sample."
  },
  mutant: {
    title: "Authentic MUTANT Hinglish",
    count: "30 matched pairs",
    delta: "+0.0920 mean difference · median +0.0001",
    marker: 88.3,
    summary: "The mean difference was positive while the median was almost zero, consistent with a skewed, saturated score distribution. This should not be read as a prompt win."
  }
};

const tabs = document.querySelectorAll(".condition-tab");
for (const tab of tabs) {
  tab.addEventListener("click", () => {
    const result = conditions[tab.dataset.condition];
    tabs.forEach((item) => {
      const selected = item === tab;
      item.classList.toggle("active", selected);
      item.setAttribute("aria-selected", String(selected));
    });
    document.querySelector("#condition-title").textContent = result.title;
    document.querySelector("#condition-count").textContent = result.count;
    document.querySelector("#entailment-delta").textContent = result.delta;
    document.querySelector("#entailment-marker").style.left = `${result.marker}%`;
    document.querySelector("#pilot-summary").textContent = result.summary;
  });
}
