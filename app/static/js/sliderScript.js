ranges.forEach((range) => {
    const rangeSelected = range.querySelector(".range-selected");
    const rangeInput = range.querySelectorAll(".range-input input");
    const rangePrice = range.querySelectorAll(".range-price input");

    rangeInput.forEach((input) => {
        input.addEventListener("input", (e) => {
            let minRange = parseFloat(rangeInput[0].value);
            let maxRange = parseFloat(rangeInput[1].value);

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
                rangeSelected.style.width = ((maxRange - minRange) / rangeInput[0].max) * 100 + "%";
                rangeInput[0].style.zIndex = 1;
                rangeInput[1].style.zIndex = 1;
            }

            // Check which input was last clicked and set the z-index accordingly
            if (e.target.className === "min") {
                rangeInput[0].style.zIndex = 2;
            } else {
                rangeInput[1].style.zIndex = 2;
            }
        });
    });

    rangePrice.forEach((input) => {
        input.addEventListener("input", (e) => {
            let minPrice = parseFloat(rangePrice[0].value);
            let maxPrice = parseFloat(rangePrice[1].value);
            console.log(minPrice)
            console.log(maxPrice)
            if (minPrice >= rangeInput[0].min && maxPrice <= rangeInput[1].max && minPrice <= maxPrice) {
                if (e.target.className === "min") {
                    rangeInput[0].value = minPrice;
                    rangeSelected.style.left = (minPrice / rangeInput[0].max) * 100 + "%";
                } else {
                    rangeInput[1].value = maxPrice;
                    rangeSelected.style.right = 100 - (maxPrice / rangeInput[1].max) * 100 + "%";
                }
                rangeSelected.style.width = ((maxPrice - minPrice) / rangeInput[0].max) * 100 + "%";
            } else if (e.target.className === "min") {
                rangePrice[0].value = rangeInput[0].value;
            } else {
                rangePrice[1].value = rangeInput[1].value;
            }
        });
    });

});

