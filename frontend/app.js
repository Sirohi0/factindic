const conditions = {
  all: {
    title: "Prior Devanagari-based pilot",
    count: "76 matched pairs",
    delta: "Not target-style evidence",
    marker: 50,
    summary: "This earlier screening run used Devanagari-based sources. Its median paired differences are close to zero and its NLI scores are ceiling-saturated. Do not read it as a Roman-script Hinglish result."
  },
  hindi: {
    title: "Prior Hindi-script condition",
    count: "23 matched pairs",
    delta: "−0.0353 mean difference · median −0.0002",
    marker: 35.3,
    summary: "This prior condition used Devanagari Hindi. It is included only to document the earlier pilot and does not represent the corrected Roman-script Hinglish target."
  },
  synthetic: {
    title: "Prior synthetic p100 condition",
    count: "23 matched pairs",
    delta: "−0.0025 mean difference · median −0.0005",
    marker: 49.0,
    summary: "This prior synthetic condition used Devanagari-based sources with inserted English tokens. It does not test Hindi written in Latin characters."
  },
  mutant: {
    title: "Prior MUTANT sample",
    count: "30 matched pairs",
    delta: "+0.0920 mean difference · median +0.0001",
    marker: 88.3,
    summary: "The 30-source local sample was Devanagari-dominant. The original dataset is retained for provenance and background, but this sample does not evaluate the target Roman-script style."
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
