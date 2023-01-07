let rangeMin = 0;

const ranges = document.querySelectorAll(".range");
ranges.forEach((range) => {
    const rangeSelected = range.querySelector(".range-selected");
    const rangeInput = range.querySelectorAll(".range-input input");
    const rangePrice = range.querySelectorAll(".range-price input");

    rangeInput.forEach((input) => {
        input.addEventListener("input", (e) => {
            let minRange = parseInt(rangeInput[0].value);
            let maxRange = parseInt(rangeInput[1].value);
            if (maxRange - minRange < rangeMin) {
                if (e.target.className === "min") {
                    rangeInput[0].value = maxRange - rangeMin;
                } else {
                    rangeInput[1].value = minRange + rangeMin;
                }
            } else {
                rangePrice[0].value = minRange;
                rangePrice[1].value = maxRange;
                rangeSelected.style.left = (minRange / rangeInput[0].max) * 100 + "%";
                rangeSelected.style.right = 100 - (maxRange / rangeInput[1].max) * 100 + "%";
            }
        });
    });

    rangePrice.forEach((input) => {
        input.addEventListener("input", (e) => {
            let minPrice = rangePrice[0].value;
            let maxPrice = rangePrice[1].value;
            if (maxPrice - minPrice >= rangeMin && maxPrice <= rangeInput[1].max) {
                if (e.target.className === "min") {
                    rangeInput[0].value = minPrice;
                    rangeSelected.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
                } else {
                    rangeInput[1].value = maxPrice;
                    rangeSelected.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
                }
            }
        });
    });
});