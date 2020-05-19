
const csrfToken = $("#csrf_token")

//Autopopulate the average kWh for the chosen appliance
$("#appliance-select").change(async function() {
    let appliance = $(this).find("option:selected").val();
    let resp = await axios({
        method: 'get', 
        url: `/watts/${appliance}` + '?nocache=' + new Date().getTime(),
        headers: {
            "X-CSRFToken": csrfToken
        }
    })

    $("#watts").val(resp.data.watts);
})

//Use geolocation if a user allows
$("#gps").on("click", async function(e){
    e.preventDefault()
    geoFindMe()
})

//Autopopulate the average price for a region, based on the entered location
$("#zipcode").on("change", async function(){
    let postalcode = $("#zipcode").attr('data-place');
    console.log(postalcode)
    let resp = await axios({
        method: 'get',
        url: `/rates/${postalcode}` + '?nocache=' + new Date().getTime(),
        headers: {
            "X-CSRFToken": csrfToken
        }
    })

    $('#rate').val(resp.data.rate)
})
//submit appliance search form
$("#submit-calc").on("click", async function(e){
    e.preventDefault();
    

    await calcResp().then(response => {
        htmlCalcResults(response)
    })
    
   
    $("#submit-form").trigger('reset');
})


//Axios request for calculated energy
async function calcResp() {
    
    const resp = await axios({
        method: 'get',
        url: '/calculate' + '?nocache=' + new Date().getTime(),
        params: {
            watts: $("#watts").val(),
            rate: $("#rate").val(),
            hours: $("#hours").val(),
            days: $("#days").val(),
            zipcode: $("#zipcode").val(),
            applianceId: $("#appliance-select").val(),
            time: new Date()
        },
        headers: {
            "X-CSRFToken": csrfToken
        } 
    })

    return resp
}

//Axios request for saving searches
// async function saveSearch() {
//     const resp = await axios({
//         method: 'post',
//         url: '/save'  + '?nocache=' + new Date().getTime(),
//         headers: {
//             "X-CSRFToken": csrfToken
//         }
//     })
// }

//Turn calculated energy results into HTML
function htmlCalcResults(calc_resp) {
    $("#calc-results").empty()

    let data = calc_resp.data;
   
    //create calculation div 
    const $calcDiv = $('<div/>', {
        'class': 'card card-body'
    });

    let dailyEnergy = `<p>Daily energy consumption: ${data["daily_kWh"].toFixed(2)} kWh</p>`;
    let annualEnergyConsump   = `<p>Annual energy consumption: ${data["annual_consump"].toFixed(2)} kWh</p>`;
    let annualCost = `<p>Annual cost: <b>$${data["annual_cost"].toFixed(2)}/year</b></p>`;
   $calcDiv.append(dailyEnergy);
   $calcDiv.append(annualEnergyConsump);
   $calcDiv.append(annualCost); 

    $("#calc-results").append($calcDiv);

    //create grid div
    const $gridDiv = $('<div/>', {
        'class': 'card card-body'
    });

    let grid_name_html = `<p> Grid: ${data["ba"]}</p>`;
    let grid_emission = `<p> Current Emissions (%): ${data["percent"]}</p>`;
    let location = `<p> ${data["city"]}, ${data["state"]} </p>`;
    let time = new Date();
    let htmlTime = `<p> ${time.toLocaleDateString()}, ${time.toLocaleTimeString()}</p>`;
    $gridDiv.append(grid_name_html);
    $gridDiv.append(grid_emission);
    $gridDiv.append(location);
    $gridDiv.append(htmlTime);
    
    $("#grid-results").append($gridDiv);
    controlTicker(data["percent"])
}


//set ticker hand to the correct percentage
function controlTicker(gridpercent) {

    let rotation = 180 * (gridpercent/100)
    
    const tick = document.querySelector('.scorer-1-tick')
    
    tick.style.transformOrigin = "right center"
    tick.style.transform = `rotate(${rotation}deg)`
       
}

//Find postcode of user using geolocation
function geoFindMe() {
   
    const zipcode = $("#zipcode");
    const help = $("#help-location")
    
  
    async function success(position) {
      const lat  = position.coords.latitude;
      const lng = position.coords.longitude;

        
        const resp = await axios({
            method: 'get',
            url: '/zipcode' + '?nocache=' + new Date().getTime(),
            params: {
                lat: lat,
                lng: lng
            },
            headers: {
                "X-CSRFToken": csrfToken
            } 
        })

        zipcode.val(resp.data.zip)
        zipcode.attr('data-place', resp.data.state)
    }
  
    function error() {
      help.textContent = 'Unable to retrieve your location';
    }
  
    if(!navigator.geolocation) {
      help.textContent = 'Geolocation is not supported by your browser';
    } else {
      help.textContent = 'Locating…';
      navigator.geolocation.getCurrentPosition(success, error);
    }
  
  }
  

  

  