"use strict";

// element toggle function
const elementToggleFunc = function (elem) {
  elem.classList.toggle("active");
};

// sidebar variables
const sidebar = document.querySelector("[data-sidebar]");
const sidebarBtn = document.querySelector("[data-sidebar-btn]");

// sidebar toggle functionality for mobile
sidebarBtn.addEventListener("click", function () {
  elementToggleFunc(sidebar);
});

// testimonials variables
const testimonialsItem = document.querySelectorAll("[data-testimonials-item]");
const modalContainer = document.querySelector("[data-modal-container]");
const modalCloseBtn = document.querySelector("[data-modal-close-btn]");
const overlay = document.querySelector("[data-overlay]");

// modal variable
const modalImg = document.querySelector("[data-modal-img]");
const modalTitle = document.querySelector("[data-modal-title]");
const modalText = document.querySelector("[data-modal-text]");
const modalTime = document.querySelector("[data-modal-time]");

// modal toggle function
const testimonialsModalFunc = function () {
  modalContainer.classList.toggle("active");
  overlay.classList.toggle("active");
};

// add click event to all modal items
for (let i = 0; i < testimonialsItem.length; i++) {
  testimonialsItem[i].addEventListener("click", function () {
    modalImg.src = this.querySelector("[data-testimonials-avatar]").src;
    modalImg.alt = this.querySelector("[data-testimonials-avatar]").alt;
    modalTitle.innerHTML = this.querySelector(
      "[data-testimonials-title]"
    ).innerHTML;
    modalText.innerHTML = this.querySelector(
      "[data-testimonials-text]"
    ).innerHTML;
    modalTime.innerHTML = this.querySelector(
      "[data-testimonials-time]"
    ).innerHTML;

    testimonialsModalFunc();
  });
}

// add click event to modal close button
modalCloseBtn.addEventListener("click", testimonialsModalFunc);
overlay.addEventListener("click", testimonialsModalFunc);

// custom select variables
const select = document.querySelector("[data-select]");
const selectItems = document.querySelectorAll("[data-select-item]");
const selectValue = document.querySelector("[data-select-value]");
const filterBtn = document.querySelectorAll("[data-filter-btn]");

select.addEventListener("click", function () {
  elementToggleFunc(this);
});

// add event in all select items
for (let i = 0; i < selectItems.length; i++) {
  selectItems[i].addEventListener("click", function () {
    let selectedValue = this.innerText.toLowerCase();
    selectValue.innerText = this.innerText;
    elementToggleFunc(select);
    filterFunc(selectedValue);
  });
}

// filter variables
const filterItems = document.querySelectorAll("[data-filter-item]");

const filterFunc = function (selectedValue) {
  for (let i = 0; i < filterItems.length; i++) {
    if (selectedValue === "All") {
      filterItems[i].classList.add("active");
    } else if (selectedValue === filterItems[i].dataset.category) {
      filterItems[i].classList.add("active");
    } else {
      filterItems[i].classList.remove("active");
    }
  }
};

// add event in all filter button items for large screen
let lastClickedBtn = filterBtn[0];

for (let i = 0; i < filterBtn.length; i++) {
  filterBtn[i].addEventListener("click", function () {
    let selectedValue = this.innerText;
    console.log(selectValue)
    selectValue.innerText = this.innerText;
    filterFunc(selectedValue);

    lastClickedBtn.classList.remove("active");
    this.classList.add("active");
    lastClickedBtn = this;
  });
}

// contact form variables
const form = document.querySelector("[data-form]");
const formInputs = document.querySelectorAll("[data-form-input]");
const formBtn = document.querySelector("[data-form-btn]");

// add event to all form input field
for (let i = 0; i < formInputs.length; i++) {
  formInputs[i].addEventListener("input", function () {
    // check form validation
    if (form.checkValidity()) {
      formBtn.removeAttribute("disabled");
    } else {
      formBtn.setAttribute("disabled", "");
    }
  });
}

// page navigation variables
const navigationLinks = document.querySelectorAll("[data-nav-link]");
const pages = document.querySelectorAll("[data-page]");

// add event to all nav link
for (let i = 0; i < navigationLinks.length; i++) {
  navigationLinks[i].addEventListener("click", function () {
    for (let i = 0; i < pages.length; i++) {
      if (this.innerHTML.toLowerCase() === pages[i].dataset.page) {
        pages[i].classList.add("active");
        navigationLinks[i].classList.add("active");
        window.scrollTo(0, 0);
      } else {
        pages[i].classList.remove("active");
        navigationLinks[i].classList.remove("active");
      }
    }
  });
}


// portfolio variables
const portfoliosItem = document.querySelectorAll("[data-portfolio-item]");
const modalContainerPortfolio = document.querySelector("[data-modal-container-portfolio]");
const modalCloseBtnPortfolio = document.querySelector("[data-modal-close-btn-portfolio]");
const overlayPortfolio = document.querySelector("[data-overlay-portfolio]");

const modalImgPortfolio1 = document.querySelector("[data-modal-img-portfolio-1]");
const modalImgPortfolio2 = document.querySelector("[data-modal-img-portfolio-2]");
const modalImgPortfolio3 = document.querySelector("[data-modal-img-portfolio-3]");
const modalTitlePortfolio = document.querySelector("[data-modal-title-portfolio]");
const modalTextPortfolio = document.querySelector("[data-modal-text-portfolio]");

// portfolio modal toggle function

const portfoliotestimonialsModalFunc = function () {
  modalContainerPortfolio.classList.toggle("active");
  overlayPortfolio.classList.toggle("active");
};

// add click event to all modal items
for (let i = 0; i < portfoliosItem.length; i++) {
  portfoliosItem[i].addEventListener("click", function () {
    modalImgPortfolio1.src = this.querySelector("[data-portfolio-image-1]").src;
    modalImgPortfolio1.alt = this.querySelector("[data-portfolio-image-1]").alt;
    modalImgPortfolio2.src = this.querySelector("[data-portfolio-image-2]").src;
    modalImgPortfolio2.alt = this.querySelector("[data-portfolio-image-2]").alt;
    modalImgPortfolio3.src = this.querySelector("[data-portfolio-image-3]").src;
    modalImgPortfolio3.alt = this.querySelector("[data-portfolio-image-3]").alt;

    modalTitlePortfolio.innerHTML = this.querySelector(
      "[data-portfolio-title]"
    ).innerHTML;
    modalTextPortfolio.innerHTML = this.querySelector(
      "[data-portfolio-text]"
    ).innerHTML;

    portfoliotestimonialsModalFunc();
  });
}

// add click event to modal close button
modalCloseBtnPortfolio.addEventListener("click", portfoliotestimonialsModalFunc);
overlayPortfolio.addEventListener("click", portfoliotestimonialsModalFunc);


/// Resume Download

document.addEventListener("DOMContentLoaded", function () {
  // Get the download icon element
  const downloadIcon = document.getElementById("download-icon");

  // Add a click event listener to the download icon
  downloadIcon.addEventListener("click", function () {
    // Replace the URL with the direct link to your resume file
    const resumeURL = "https://drive.google.com/file/d/1jogPlWs63P6upqMFUOjaYFwVLJg99W4o/view?usp=sharing";

    // Create a temporary link to trigger the download
    const tempLink = document.createElement("a");
    tempLink.href = resumeURL;
    tempLink.setAttribute("download", "resume.pdf"); // Set the desired file name for the download
    tempLink.style.display = "none";

    // Append the link to the DOM and trigger the click event
    document.body.appendChild(tempLink);
    tempLink.click();

    // Remove the link from the DOM
    document.body.removeChild(tempLink);
  });
});


///// Typewriter

var span = document.querySelector(".typewriter span");
var textArr = span.getAttribute("data-text").split(", ");
var maxTextIndex = textArr.length;

var sPerChar = 0.10;
var sBetweenWord = 1.0;
var textIndex = 0;

typing(textIndex, textArr[textIndex]);

function typing(textIndex, text) {
  var charIndex = 0;
  var maxCharIndex = text.length - 1;

  var typeInterval = setInterval(function () {
    span.innerHTML += text[charIndex];
    if (charIndex == maxCharIndex) {
      clearInterval(typeInterval);
      setTimeout(function () { deleting(textIndex, text) }, sBetweenWord * 1000);

    } else {
      charIndex += 1;
    }
  }, sPerChar * 1000);
}

function deleting(textIndex, text) {
  var minCharIndex = 0;
  var charIndex = text.length - 1;

  var typeInterval = setInterval(function () {
    span.innerHTML = text.substr(0, charIndex);
    if (charIndex == minCharIndex) {
      clearInterval(typeInterval);
      textIndex + 1 == maxTextIndex ? textIndex = 0 : textIndex += 1;
      setTimeout(function () { typing(textIndex, textArr[textIndex]) }, sBetweenWord * 1000);
    } else {
      charIndex -= 1;
    }
  }, sPerChar * 1000);
}
