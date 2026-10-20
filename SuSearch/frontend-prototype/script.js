const projects = [
  {
    id: 1,
    title: "Matsvinn",
    theme: "Mat och konsumtion",
    summary: "Minska matsvinn i skolor och offentliga kök.",
    tags: ["Mat", "Matsvinn"],
    methods: ["Workshop", "Pilotstudie"],
    activities: ["Workshop med kökspersonal", "Mätning av matsvinn"],
    partners: ["Kommuner", "Skolor"],
    result: "Arbetssätt för att mäta och minska matsvinn.",
    reason: "Passar sökningar om mat, konsumtion och matsvinn."
  },
  {
    id: 2,
    title: "Cirkulär ekonomi",
    theme: "Cirkulär ekonomi",
    summary: "Återbruk, delning och hur material kan användas längre.",
    tags: ["Återbruk", "Resurser"],
    methods: ["Workshop", "Co-design"],
    activities: ["Workshop om återbruk", "Gemensam idéutveckling"],
    partners: ["Kommuner", "Lokala verksamheter"],
    result: "Idéer för återbruk och delning.",
    reason: "Passar sökningar om cirkulär ekonomi, återbruk och resurser."
  },
  {
    id: 3,
    title: "Klimatanpassning",
    theme: "Klimatanpassning",
    summary: "Skyfall, värme och grönare bostadsområden.",
    tags: ["Klimat", "Stadsutveckling"],
    methods: ["Dialogmöten", "Pilotstudie"],
    activities: ["Dialogmöte", "Test av en lokal lösning"],
    partners: ["Kommuner", "Fastighetsägare"],
    result: "Lokala lösningar för regn och värme.",
    reason: "Passar sökningar om klimat, skyfall och grön stadsutveckling."
  },
  {
    id: 4,
    title: "Hållbara transporter",
    theme: "Transporter",
    summary: "Cykling, kollektivtrafik och nya resvanor.",
    tags: ["Resor", "Transporter"],
    methods: ["Dialogmöten", "Pilotstudie"],
    activities: ["Resvaneundersökning", "Test av en transportlösning"],
    partners: ["Kommuner", "Arbetsplatser"],
    result: "Hur hållbara resor kan testas i liten skala.",
    reason: "Passar sökningar om resvanor, cykling och kollektivtrafik."
  },
  {
    id: 5,
    title: "Energi",
    theme: "Energi",
    summary: "Använda mindre energi i lokaler och verksamheter.",
    tags: ["Energi", "Rådgivning"],
    methods: ["Utbildning", "Workshop"],
    activities: ["Energivandring", "Kort utbildning"],
    partners: ["Föreningar", "Kommuner"],
    result: "En enkel plan för minskad energianvändning.",
    reason: "Passar sökningar om energi, lokaler och rådgivning."
  },
  {
    id: 6,
    title: "Biologisk mångfald",
    theme: "Biodiversitet",
    summary: "Natur, pollinatörer och gröna miljöer nära människor.",
    tags: ["Natur", "Biodiversitet"],
    methods: ["Dialogmöten", "Utbildning"],
    activities: ["Naturvandring", "Samtal med lokala aktörer"],
    partners: ["Föreningar", "Skolor"],
    result: "Små åtgärder som kan gynna den lokala naturen.",
    reason: "Passar sökningar om natur, pollinatörer och biologisk mångfald."
  }
];

const searchInput = document.querySelector("#searchInput");
const searchButton = document.querySelector("#searchButton");
const resultList = document.querySelector("#resultList");
const resultCount = document.querySelector("#resultCount");
const loadingState = document.querySelector("#loadingState");
const loadingText = document.querySelector("#loadingText");
const emptyState = document.querySelector("#emptyState");
const fileInput = document.querySelector("#fileInput");
const chosenFile = document.querySelector("#chosenFile");
const drawer = document.querySelector("#projectDrawer");
const drawerBackdrop = document.querySelector("#drawerBackdrop");
const drawerContent = document.querySelector("#drawerContent");

const filterIds = ["themeFilter", "methodFilter"];

let selectedFile = null;
let lastFocusedButton = null;

function getFilteredProjects() {
  const query = searchInput.value.trim().toLocaleLowerCase("sv");

  const ignored = [
    "och",
    "med",
    "som",
    "för",
    "ett",
    "att",
    "om",
    "projekt"
  ];

  const words = query
    .split(/\s+/)
    .filter(word => word.length > 2 && !ignored.includes(word));

  const filters = Object.fromEntries(
    filterIds.map(id => [
      id,
      document.querySelector("#" + id).value
    ])
  );

  return projects
    .map(project => {
      const searchable = [
        project.title,
        project.summary,
        project.theme,
        ...project.tags,
        ...project.methods,
        ...project.activities,
        ...project.partners
      ]
        .join(" ")
        .toLocaleLowerCase("sv");

      const wordHits = words.filter(word =>
        searchable.includes(word)
      ).length;

      return {
        ...project,
        wordHits
      };
    })
    .filter(project => {
      const matchesQuery =
        words.length === 0 || project.wordHits > 0;

      return (
        matchesQuery &&
        (!filters.themeFilter ||
          project.theme === filters.themeFilter) &&
        (!filters.methodFilter ||
          project.methods.includes(filters.methodFilter))
      );
    })
    .sort((a, b) => b.wordHits - a.wordHits);
}

function renderProjects(list) {
  loadingState.hidden = true;
  emptyState.hidden = list.length > 0;
  resultList.hidden = list.length === 0;

  resultCount.textContent =
    list.length === 1
      ? "1 exempel"
      : `${list.length} exempel`;

  // I might add matching to the project cards later.

  resultList.innerHTML = list
    .map(
      project => `
        <article class="project-card">
          <div class="card-top">
            <span class="meta">${project.theme}</span>
          </div>

          <h3>${project.title}</h3>

          <p>${project.summary}</p>

          <div class="card-footer">
            <div class="tags">
              ${project.tags
                .slice(0, 2)
                .map(tag => `<span class="tag">${tag}</span>`)
                .join("")}
            </div>

            <button
              class="view-button"
              type="button"
              data-project-id="${project.id}"
            >
              Visa exempel
            </button>
          </div>
        </article>
      `
    )
    .join("");
}

function runSearch(documentSearch = false) {
  loadingState.hidden = false;
  emptyState.hidden = true;
  resultList.hidden = true;
  resultCount.textContent = "";

  loadingText.textContent = documentSearch
    ? "Simulerar dokumentanalys..."
    : "Letar bland exemplen...";

  window.setTimeout(() => {
    const list = getFilteredProjects();

    renderProjects(list);

    document
      .querySelector("#results-title")
      .scrollIntoView({
        behavior: "smooth",
        block: "start"
      });
  }, documentSearch ? 1100 : 500);
}

function updateFilterLabel() {
  const active = filterIds
    .map(id => document.querySelector("#" + id))
    .filter(select => select.value);

  document.querySelector("#activeFilters").textContent =
    active.length === 1
      ? "1 filter valt"
      : active.length > 1
        ? `${active.length} filter valda`
        : "Inga filter valda";
}

function openProject(id, trigger) {
  const project = projects.find(
    item => item.id === Number(id)
  );

  if (!project) return;

  lastFocusedButton = trigger || document.activeElement;

  drawerContent.innerHTML = `
    <p class="detail-period">${project.theme}</p>

    <h2 id="detailTitle">${project.title}</h2>

    <p class="detail-summary">${project.summary}</p>

    <div class="detail-relevance">
      <strong>Därför passar exemplet</strong>
      <span>${project.reason}</span>
    </div>

    <div class="detail-grid">
      <section class="detail-block">
        <h3>Aktiviteter</h3>
        <ul>
          ${project.activities
            .map(item => `<li>${item}</li>`)
            .join("")}
        </ul>
      </section>

      <section class="detail-block">
        <h3>Arbetssätt</h3>
        <ul>
          ${project.methods
            .map(item => `<li>${item}</li>`)
            .join("")}
        </ul>
      </section>

      <section class="detail-block">
        <h3>Kan kopplas till</h3>
        <ul>
          ${project.partners
            .map(item => `<li>${item}</li>`)
            .join("")}
        </ul>
      </section>

      <section class="detail-block">
        <h3>Exempelresultat</h3>
        <p>${project.result}</p>
      </section>

      <section class="detail-block detail-wide">
        <h3>Dokument och material</h3>
        <p>Exempel på rapport och metodmaterial.</p>
      </section>
    </div>

    <a
      class="sharepoint-link"
      href="#"
      id="sharepointLink"
    >
      Exempel: öppna i SharePoint
    </a>
  `;

  drawer.classList.add("open");
  drawerBackdrop.classList.add("open");

  drawer.setAttribute("aria-hidden", "false");

  document.body.classList.add("drawer-open");

  document.querySelector("#closeDrawer").focus();
}

function closeProject() {
  drawer.classList.remove("open");
  drawerBackdrop.classList.remove("open");

  drawer.setAttribute("aria-hidden", "true");

  document.body.classList.remove("drawer-open");

  if (lastFocusedButton) {
    lastFocusedButton.focus();
  }
}

searchButton.addEventListener("click", () => {
  runSearch(false);
});

searchInput.addEventListener("keydown", event => {
  if (event.key === "Enter") {
    runSearch(false);
  }
});

document
  .querySelector("#fileButton")
  .addEventListener("click", () => {
    fileInput.click();
  });

fileInput.addEventListener("change", () => {
  selectedFile = fileInput.files[0] || null;

  if (!selectedFile) return;

  document.querySelector("#fileName").textContent =
    selectedFile.name;

  chosenFile.classList.add("visible");

  runSearch(true);
});

document
  .querySelector("#removeFile")
  .addEventListener("click", () => {
    selectedFile = null;

    fileInput.value = "";

    chosenFile.classList.remove("visible");

    renderProjects(getFilteredProjects());
  });

document
  .querySelector("#filterButton")
  .addEventListener("click", event => {
    const panel =
      document.querySelector("#filterPanel");

    const isOpen =
      panel.classList.toggle("open");

    event.currentTarget.setAttribute(
      "aria-expanded",
      String(isOpen)
    );
  });

filterIds.forEach(id => {
  document
    .querySelector("#" + id)
    .addEventListener("change", () => {
      updateFilterLabel();

      renderProjects(getFilteredProjects());
    });
});

document
  .querySelector("#clearFilters")
  .addEventListener("click", () => {
    filterIds.forEach(id => {
      document.querySelector("#" + id).value = "";
    });

    updateFilterLabel();

    renderProjects(getFilteredProjects());
  });

resultList.addEventListener("click", event => {
  const button =
    event.target.closest("[data-project-id]");

  if (button) {
    openProject(
      button.dataset.projectId,
      button
    );
  }
});

document
  .querySelector("#closeDrawer")
  .addEventListener("click", closeProject);

drawerBackdrop.addEventListener(
  "click",
  closeProject
);

document.addEventListener("keydown", event => {
  if (
    event.key === "Escape" &&
    drawer.classList.contains("open")
  ) {
    closeProject();
  }
});

drawerContent.addEventListener("click", event => {
  if (
    !event.target.closest("#sharepointLink")
  ) {
    return;
  }

  event.preventDefault();

  const toast =
    document.querySelector("#toast");

  toast.classList.add("show");

  window.setTimeout(() => {
    toast.classList.remove("show");
  }, 2300);
});

renderProjects(getFilteredProjects());

// Dark theme
const themeToggle = document.querySelector("#themeToggle");
const themeLabel = document.querySelector("#themeLabel");
const themeIcon = document.querySelector("#themeIcon");

function updateTheme() {
  const isDark = document.body.classList.contains("dark-mode");

  themeLabel.textContent = isDark ? "Ljust läge" : "Mörkt läge";
  themeIcon.textContent = isDark ? "☀" : "☾";

  themeToggle.setAttribute(
    "aria-label",
    isDark ? "Byt till ljust tema" : "Byt till mörkt tema"
  );
}

// localstorage for theme mode 
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark-mode");
}

updateTheme();

themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark-mode");

  localStorage.setItem(
    "theme",
    document.body.classList.contains("dark-mode") ? "dark" : "light"
  );

  updateTheme();
});