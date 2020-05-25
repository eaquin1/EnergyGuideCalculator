const csrfToken = $("#csrf_token");

//Autopopulate the average kWh for the chosen appliance
$("#appliance-select").change(async function () {
  let appliance = $(this).find("option:selected").val();
  let resp = await axios({
    method: "get",
    url: `/watts/${appliance}` + "?nocache=" + new Date().getTime(),
    headers: {
      "X-CSRFToken": csrfToken,
    },
  });

  $("#watts").val(resp.data.watts);
});

//Use geolocation if a user allows
$("#gps").on("click", async function (e) {
  e.preventDefault();
  geoFindMe();
});

//Autopopulate the average price for a region, based on the entered location
$("#zipcode").on("blur", async function () {
  const postalCode = $("#zipcode").val();
  const help = $("#help-location");

  if (isValidPostalCode(postalCode)) {
    help.text("");
    let resp = await axios({
      method: "get",
      url: `/zipcode` + "?nocache=" + new Date().getTime(),
      params: {
        zipcode: postalCode,
      },
      headers: {
        "X-CSRFToken": csrfToken,
      },
    });

    $("#rate").val(resp.data.rate);
  } else {
    help.text("Please enter a valid postal code");
  }
});

//Find postcode of user using geolocation
function geoFindMe() {
  const zipcode = $("#zipcode");
  const help = $("#help-location");

  async function success(position) {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    const resp = await axios({
      method: "get",
      url: "/zipcode" + "?nocache=" + new Date().getTime(),
      params: {
        lat: lat,
        lng: lng,
      },
      headers: {
        "X-CSRFToken": csrfToken,
      },
    });
    $("#rate").val(resp.data.rate);
    zipcode.val(resp.data.zip);
    help.text("");
  }

  function error() {
    help.textContent = "Unable to retrieve your location";
  }

  if (!navigator.geolocation) {
    help.text("Geolocation is not supported by your browser");
  } else {
    help.text("Locating…");
    navigator.geolocation.getCurrentPosition(success, error);
  }
}

function isValidPostalCode(postalCode) {
  pc = postalCode.toUpperCase();

  if (pc.length == 7) {
    postalCodeRegex = /^([A-Z][0-9][A-Z])\s*([0-9][A-Z][0-9])$/;
  } else if (pc.length == 5) {
    postalCodeRegex = /^([0-9]{5})(?:[-\s]*([0-9]{4}))?$/;
  } else if (pc.length == 3) {
    postalCodeRegex = /^(?:[A-Z0-9]+([- ]?[A-Z0-9]+)*)?$/;
  } else {
    return false;
  }

  return postalCodeRegex.test(pc);
}
