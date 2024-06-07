const searchField = document.getElementById("exp-search")

searchField.addEventListener("keyup", (e) => {
    const searchVal = e.target.value;
    if (searchVal.trim().length > 0) {
        console.log(searchVal);
        fetch("/expenses/search", {
            // send to url via post
            body: JSON.stringify({search: searchVal}),
            method: "POST"
        })
        .then((res) => res.json()) // get the json response
        .then((data) => {
            console.log("data", data);
        });
    }
})