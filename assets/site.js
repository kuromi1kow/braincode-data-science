"use strict";

const search = document.querySelector("#lesson-search");
if (search) {
  search.addEventListener("input", () => {
    const normalize = value => value.toLocaleLowerCase("ru").replaceAll("ё", "е").trim();
    const terms = normalize(search.value).split(/\s+/);
    const cards = [...document.querySelectorAll("[data-lesson]")];
    for (const card of cards) {
      const words = normalize(card.textContent + " " + card.dataset.lesson);
      card.hidden = !terms.every(term => words.includes(term));
    }
    for (const group of document.querySelectorAll(".group")) {
      group.hidden = !group.querySelector("[data-lesson]:not([hidden])");
    }
    const count = cards.filter(card => !card.hidden).length;
    document.querySelector("#found").textContent = count ? "Найдено занятий: " + count : "Занятий по этому запросу нет. Попробуйте «циклы», «массив» или номер занятия.";
    document.querySelector("#found").classList.toggle("sr", count > 0);
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
