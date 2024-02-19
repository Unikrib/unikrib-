//displays search parameters in search result heading
function searchParameter() {
    let community = $("#location-search :selected").text();
    let type = $("#Apartment-type :selected").text();
    let minimum = document.getElementById("minimum-price").value;
    let maximum = document.getElementById("maximum-price").value;
     document.getElementById("search-filter").innerHTML = 
     "Search results for " + community + " , " + type + " from " + minimum
     + " to " + maximum;
}

// changes the search button colour from green to purple
var button2 = document.getElementById("apartment-search");
button2.addEventListener("click", changeColor)

function changeColor() {
    button2.style.backgroundColor = "purple"
}

let currentSlide = 0;

function startSlider() {
  let imageCount = document.querySelectorAll(".Ad-img-container");

  if (imageCount.length === 0) {
    imageCount = document.querySelectorAll("Ad-img-container");
    images.style.transform = `translateX(0%)`;
    return;
  }

  let images = document.querySelector(".slides");
  images.style.transform = `translateX(-${currentSlide * 50}%)`;

  if (currentSlide === imageCount.length - 1) {
    currentSlide = 0;
  } else {
    currentSlide++;
  }
}

setInterval(() => {
    startSlider();
  }, 3500)

  const accordion_button = document.querySelectorAll('.accordion-item button');
const all_item = document.querySelectorAll('.accordion-item');
accordion_button.forEach((ele) => {
	ele.addEventListener('click', () => {
		let content = ele.nextElementSibling;
		let active = document.querySelector('.accordion-item.active');
		if (active) {
			if (ele.parentElement.classList.contains('active')) {
				ele.parentElement.classList.remove('active');
				active.lastElementChild.style.height = '0';
			} else {
				active.classList.remove('active');
				active.lastElementChild.style.height = '0';
				ele.parentElement.classList.add('active');
				content.style.height = content.scrollHeight + 'px';
			}
		} else {
			ele.parentElement.classList.add('active');
			content.style.height = content.scrollHeight + 'px';
		}
	});
});
// console.log(accordion_button);
