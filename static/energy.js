
const csrfToken = $("#csrf_token")


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

$("#submit-calc").on("click", async function(e){
    e.preventDefault();
    
    

    await calcResp().then(response => {
        htmlCalcResults(response)
    })
    
    // await calcGrid().then(response => {
    //     htmlGridResults(response);
    // })
   
    $("#submit-form").trigger('reset');
})

// $("#search-btn").on("click", async function(e){
//     e.preventDefault();
//     await saveSearch();
// })

//Axios request for calculated energy
async function calcResp() {
    console.log()
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
    console.log(data)
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
   
    
//     const tick = document.querySelector('.scorer-1-tick')
//     const style = document.createElement('style');
//     style.textContent = ` @keyframes ticker-mover-1 {
//     0% {
//       transform-origin: right center;
//       transform: rotate(0deg);
//     }
//     33% {
//       transform-origin: right center;
//       transform: rotate(${rotation -10}deg);
//     }
//     66% {
//       transform-origin: right center;
//       transform: rotate(${rotation -5}deg);
//     } 
//     100% {
//       transform-origin:right center;
//       transform: rotate(${rotation}deg); 
//     }
//   } `
//     tick.append(style)
    
}