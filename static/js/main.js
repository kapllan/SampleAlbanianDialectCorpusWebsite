function myFunction() {
  var matches = [];

  var inputs = document.getElementsByClassName("input_form_search");

  for (var key in inputs) {
    var value = inputs[key].value;

    matches.push(value);
  }

  console.log(matches);
}

// Map related

// initialize Leaflet
var map = L.map("map").setView({ lon: 20, lat: 41.3 }, 8);

// add the OpenStreetMap tiles
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  maxZoom: 18,
  attribution:
    '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap contributors</a>',
}).addTo(map);

// show the scale bar on the lower left corner
L.control.scale({ imperial: true, metric: true }).addTo(map);

function create_marker(item, MapObject) {
  let _lon = item.coordinates_place_name.lon;
  let _lat = item.coordinates_place_name.lat;
  let _count = item.count;
  let _place_name = item.place_name;
  let _id = item.id;
  let marker = L.marker({ lon: _lon, lat: _lat }).addTo(MapObject);

  marker.bindTooltip(_place_name + ": " + _count, {
    permanent: false,
    direction: "center",
  });
  //https://gis.stackexchange.com/questions/321774/returning-data-based-on-clicked-marker-using-leaflet
  marker.myID = _id;
  marker.bindPopup(_id).on("click", function (e) {
    marker.valueOf()._icon.style.backgroundColor = "red";
    console.log(_id);
    toggle_by_class(_id);
  });
}

function addMarkersToMap(data_for_map, MapObject) {
  for (var i = 0; i < data_for_map.length; i++) {
    create_marker(data_for_map[i], MapObject);
  }
}

// --------------

function create_bar_chart(x_y_values, name_of_chart, title) {
  var xValues = x_y_values.x_values;
  var yValues = x_y_values.y_values;
  var barColors = x_y_values.colors;

  new Chart(name_of_chart, {
    type: "bar",
    data: {
      labels: xValues,
      datasets: [
        {
          backgroundColor: barColors,
          data: yValues,
        },
      ],
    },
    options: {
      scales: {
        yAxes: [
          {
            ticks: {
              beginAtZero: true,
              stepSize: 1,
            },
          },
        ],
      },
      legend: { display: false },
      responsive: true, // This is important, otherwise the bars will change unpredictably
      //maintainAspectRatio: false,
      title: {
        display: true,
        text: title,
      },
    },
  });
}

//var table = document.getElementById("result_table");

function inserExamples(response) {
  var items = response.results;
  $("#example_container").innerHTML = "";
  const example_container = document.getElementById("example_container");
  items.forEach((item) => {
    var div = document.createElement("div");
    div.className = "linguistic_example";
    div.id = item.coordinates_place_name;
    var meta_infos = document.createElement("div");
    meta_infos.className = "meta_infos";
    var info = document.createElement("p");
    info.innerHTML =
      "Place name: " + item.place_name + ", " + "Dialect: " + item.dialect;
    meta_infos.appendChild(info);
    div.appendChild(meta_infos);
    var example = document.createElement("p");
    example.innerHTML = item.context;
    div.appendChild(example);
    example_container.appendChild(div);
  });

  create_bar_chart(
    response.x_y_values_dialect_bar_chart,
    "dialect_bar_chart",
    "Frequency of occurences among dialects in percentage over all occurences"
  );
  create_bar_chart(
    response.x_y_values_country_bar_chart,
    "country_bar_chart",
    "Frequency of occurences among countries in percentage over all occurences"
  );
  create_bar_chart(
    response.x_y_values_country_dialect,
    "country_dialect_bar_chart",
    "Frequency of occurences among countries and dialects in percentage over all occurences"
  );

  addMarkersToMap(response.data_for_map, map);
}

function search() {
  const search_field = "search_field";

  var form = document.getElementById(search_field);
  var formData = new FormData(form);

  var all_inputs = {};

  formData.forEach(function (value, key) {
    all_inputs[key] = value;
  });

  all_inputs = JSON.stringify(all_inputs);

  console.log(typeof all_inputs);

  console.log(all_inputs);
  for (var [key, value] of formData) {
    console.log(key, value);
  }

  $.ajax({
    type: "POST",
    url: "/",
    data: all_inputs,
    contentType: "application/json",
    dataType: "json",
    success: function (response) {
      inserExamples(response);
    },
  });
}

function changeVisibilityOfElementById(_id, visibility) {
  let element = document.getElementById(_id);
  element.innerHTML.style.display = visibility;
}

function changeVisibilityOfElementByClass(_id, visibility) {
  let elements = document.getElementsByClassName(_id);
  for (var i = 0; i < elements.length; i++) {
    elements[i].style.display = visibility;
  }
}

function clear_everything() {
  window.location.reload();
}

document.getElementById("reset").addEventListener("click", function (e) {
  clear_everything();
});

document.getElementById("start_search").addEventListener("click", function (e) {
  search();
  e.preventDefault();
});

// Filter

function toggle_by_class(cls) {
  all_examples = document.getElementsByClassName("linguistic_example");
  for (var i = 0; i < all_examples.length; i++) {
    let example_id = all_examples[i].id;
    console.log(example_id);
    if (example_id != cls) {
      all_examples[i].style.display = "none";
    } else {
      all_examples[i].style.display = "block";
    }
  }
}
