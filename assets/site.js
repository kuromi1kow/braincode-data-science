"use strict";

if (document.body.dataset.page === "home") {
  function followOldBookmark() {
    const destination = document.getElementById(location.hash.slice(1))?.dataset.movedTo;
    if (destination) location.replace(destination);
  }
  followOldBookmark();
  window.addEventListener("hashchange", followOldBookmark);
}

const tools = document.querySelector("#catalog-tools");
if (tools) {
  const field = tools.querySelector("input");
  const filters = [...tools.querySelectorAll("[data-module]")];
  const modules = [...document.querySelectorAll(".module")];
  const reset = document.querySelector("#reset-search");
  const status = document.querySelector("#found");
  const normalize = text => text.toLocaleLowerCase("ru").replaceAll("ё", "е").trim();
  let selected = "";

  function applyFilters() {
    const query = normalize(field.value);
    const terms = query.split(/\s+/).filter(Boolean);
    let total = 0;
    for (const module of modules) {
      let matches = 0;
      for (const item of module.querySelectorAll("[data-lesson]")) {
        const text = normalize([module.querySelector("h2").textContent, item.textContent, item.dataset.lesson].join(" "));
        const visible = (!selected || selected === module.id) && terms.every(term => text.includes(term));
        item.hidden = !visible;
        if (visible) matches++;
      }
      module.hidden = matches === 0;
      total += matches;
    }
    for (const button of filters) button.setAttribute("aria-pressed", String(button.dataset.module === selected));
    reset.hidden = !query && !selected;
    status.textContent = total ? "Занятий: " + total : "Ничего не найдено. Измените запрос или сбросьте фильтры.";
  }
  field.addEventListener("input", applyFilters);
  for (const button of filters) button.addEventListener("click", () => {
    selected = button.dataset.module;
    applyFilters();
  });
  reset.addEventListener("click", () => {
    selected = "";
    field.value = "";
    applyFilters();
    field.focus();
  });
  tools.hidden = false;
  applyFilters();
}

const sectionMenu = document.querySelector(".section-menu");
if (sectionMenu) {
  const smallScreen = window.matchMedia("(max-width: 800px)");
  const setLayout = () => { sectionMenu.open = !smallScreen.matches; };
  setLayout();
  smallScreen.addEventListener("change", setLayout);
  sectionMenu.querySelector("nav").addEventListener("click", event => {
    const anchor = event.target.closest("a");
    if (!anchor || !smallScreen.matches) return;
    sectionMenu.open = false;
    const section = document.getElementById(anchor.hash.slice(1));
    if (section) {
      section.tabIndex = -1;
      section.focus({preventScroll:true});
    }
  });
}

document.querySelectorAll(".codebar button").forEach(button => {
  button.addEventListener("click", async () => {
    const code = button.closest(".codebox").querySelector("code");
    try {
      await navigator.clipboard.writeText(code.textContent);
      button.textContent = "Скопировано";
    } catch {
      const range = document.createRange();
      range.selectNodeContents(code);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      button.textContent = "Код выделен";
    }
    window.setTimeout(() => { button.textContent = "Скопировать"; }, 2200);
  });
});
const price = document.querySelector("#order-price");
if (price) {
  const update = () => {
    const value = price.valueAsNumber;
    let result = "Введите целую сумму в тенге.";
    if (Number.isSafeInteger(value)) {
      if (value < 0) result = "Сумма меньше нуля. Входные данные ошибочны.";
      else if (value >= 10000) result = "Сумма от 10 000 ₸. Доставка бесплатная, 0 ₸.";
      else if (value >= 5000) result = "Сумма от 5 000 до 9 999 ₸. Доставка стоит 500 ₸.";
      else result = "Сумма от 0 до 4 999 ₸. Доставка стоит 1 000 ₸.";
    }
    document.querySelector("#fee").textContent = result;
  };
  price.addEventListener("input",update);
  document.querySelectorAll("[data-price]").forEach(button=>button.addEventListener("click",()=>{price.value=button.dataset.price;update();}));
  update();
}
const loop = document.querySelector("#loop-next");
if (loop) {
  const values = [1000,0,2500,500];
  let step = 0;
  const show = () => {
    const total = values.slice(0,step).reduce((a,b)=>a+b,0);
    document.querySelector("#loop-state").textContent = step ? "Шаг " + step + ". Взяли " + values[step-1] + " ₸. Накопленная сумма " + total + " ₸." + (step === values.length ? " Элементы закончились." : "") : "До первой итерации сумма равна 0 ₸.";
    loop.disabled = step === values.length;
  };
  loop.addEventListener("click",()=>{step++;show();});
  document.querySelector("#loop-reset").addEventListener("click",()=>{step=0;show();});
}
const axis = document.querySelector("#axis-demo");
if (axis) {
  const array = [[1,3,2],[4,2,3]];
  const sum = values => values.reduce((a,b)=>a+b,0);
  axis.querySelectorAll("[data-axis]").forEach(button=>button.addEventListener("click",()=>{
    const byColumn = button.dataset.axis === "0";
    const groups = byColumn ? array[0].map((_,i)=>array.map(row=>row[i])) : array;
    for (const item of axis.querySelectorAll("button")) item.setAttribute("aria-pressed", String(item === button));
    axis.querySelector("output").textContent = "A.sum(axis=" + button.dataset.axis + ") = [" + groups.map(sum).join(", ") + "]. " + groups.map(g=>g.join(" + ")+" = "+sum(g)).join(". ") + ". " + (byColumn ? "Остался один итог на каждый из трёх столбцов." : "Остался один итог на каждый из двух рядов.");
  }));
}
const normalType = document.querySelector("#normal-type");
if (normalType) {
  normalType.closest(".reader-tools").hidden = false;
  const article = document.querySelector(".reading");
  const largeType = document.querySelector("#large-type");
  const setType = large => {
    article.classList.toggle("type-large", large);
    normalType.setAttribute("aria-pressed", String(!large));
    largeType.setAttribute("aria-pressed", String(large));
    try { localStorage.setItem("braincode-reading-size", large ? "large" : "normal"); } catch {}
  };
  try { setType(localStorage.getItem("braincode-reading-size") === "large"); } catch {}
  normalType.addEventListener("click",()=>setType(false));
  largeType.addEventListener("click",()=>setType(true));
}
const chapterNav = [...document.querySelectorAll(".rail a")].map(link=>[link,document.getElementById(link.hash.slice(1))]).filter(pair=>pair[1]);
if (chapterNav.length) {
  let scheduled=false;
  function locate() {
    scheduled=false;
    let found=chapterNav[0][0];
    for (const [link,section] of chapterNav) {
      if (section.getBoundingClientRect().top <= Math.min(window.innerHeight*.3,180)) found=link;
    }
    for (const [link] of chapterNav) {
      if (link===found) link.setAttribute("aria-current","location");
      else link.removeAttribute("aria-current");
    }
  }
  window.addEventListener("scroll",()=>{if (!scheduled){scheduled=true;requestAnimationFrame(locate);}}, {passive:true});
  locate();
}
