
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
    // send request to calculate the usage costs
    let calc_resp = await axios({
        method: 'get',
        url: '/calculate' + '?nocache=' + new Date().getTime(),
        params: {
            watts: $("#watts").val(),
            rate: $("#rate").val(),
            hours: $("#hours").val(),
            days: $("#days").val()
        },
        headers: {
            "X-CSRFToken": csrfToken
        } 
    })

   //send request with zipcode to receive grid cleanliness
    let zip_resp = await axios({
        method: 'get',
        url: '/grid'  + '?nocache=' + new Date().getTime(),
        params: {
            zipcode: $("#zipcode").val()
        },
        headers: {
            "X-CSRFToken": csrfToken
        }
    })

    htmlCalcResults(calc_resp);
    htmlGridResults(zip_resp);
    
})

//Turn calculated energy results into HTML
function htmlCalcResults(calc_resp) {
    $("#calc-results").empty()

    let data = calc_resp.data;
    
    let htmlObj = {};
    htmlObj["dailyEnergy"] = `<p>Daily energy consumption: ${data["daily_kWh"].toFixed(2)} kWh</p>`;
    htmlObj["annualEnergyConsump"] = `<p>Annual energy consumption: ${data["annual_consump"].toFixed(2)} kWh</p>`;
    htmlObj["annualCost"] = `<p>Annual cost: <b>$${data["annual_cost"].toFixed(2)}/year</b></p>`;
    $("#calc-results").append(htmlObj["dailyEnergy"])
    $("#calc-results").append(htmlObj["annualEnergyConsump"])
    $("#calc-results").append(htmlObj["annualCost"]) 
}

function htmlGridResults(grid_result) {
    $("#grid-results").empty()

    let grid_name_html = `<p> Grid: ${grid_result.data.ba}</p>`
    let grid_emission = `<p> Current Emissions (%): ${grid_result.data.percent}`

    $("#grid-results").append(grid_name_html)
    $("#grid-results").append(grid_emission)
}