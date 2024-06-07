function showchart(data, ctx) {
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: data.labels,
      datasets: [{
        label: data.currency,
        data: data.values,
        borderWidth: 1
      }]
    },
    options: {
      indexAxis: "y",
      scales: {
        y: {
          beginAtZero: true
        }
      },
      plugins: {
        title: {
          display: true,
          text: `Total: ${data.total} ${data.currency}`
        },
        legend: {
          display: false
        }
      }
    }
  });
}


async function buildchart(endpoint, chart_cont, key, m=0) {
  // destroy and remake canvas
  while (chart_cont.firstChild) {
    chart_cont.removeChild(chart_cont.firstChild);
  }

  let postbody = new URLSearchParams();
  postbody.append("month", m);

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {"Content-Type": "application/x-www-form-urlencoded"},
    // headers: {"Content-Type": "application/json"},
    body: postbody
  });
  // console.log("month", m);
  const data = await response.json();
  // console.log(key, data[key])
  if (data[key]) {
    const cv = document.createElement("canvas");
    cv.height = 240;
    cv.classList.add("my-4");
    cv.classList.add("w-100");
    chart_cont.appendChild(cv);
    await showchart(data[key], cv);
  } else {
    chart_cont.innerHTML = "<h4 class=\"mt-4 text-muted\">No data found</h4>"
  }
}

const mnthBtn = document.getElementById("submitMonth");
const mnth = document.getElementById("month");

const exp_cont = document.getElementById("exp_cont");
const inc_cont = document.getElementById("inc_cont");

buildchart("month_charts/", exp_cont, "exp_chart");
buildchart("month_charts/", inc_cont, "inc_chart");

mnthBtn.addEventListener("click", () => {
  const m = mnth.value;
  buildchart("month_charts/", exp_cont, "exp_chart", m);
  buildchart("month_charts/", inc_cont, "inc_chart", m);
});