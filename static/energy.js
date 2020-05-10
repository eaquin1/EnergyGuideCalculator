$("#appliance-select").change(async function() {
    let appliance = $(this).find("option:selected").val();
    let resp = await axios.get(`/watts/${appliance}`)
     $("#wattage").val(resp.data.wattage)
})

$("#zipcode").on("blur", async function(){
    // send request to calculate the usage costs
    let calc_resp = await axios({
        method: 'get',
        url: '/calculate',
        params: {
            wattage: $("#wattage").val(),
            rate: $("#rate").val(),
            hours: $("#hours").val(),
            days: $("#days").val()
        }
    })

   //send request with zipcode to receive grid cleanliness
    let zip_resp = await axios({
        method: 'get',
        url: '/grid',
        params: {
            zipcode: $("#zipcode").val()
        }
    })

    $("#results").empty()
    for (let r in calc_resp.data){
        let htmlStr = `<p>${r}: ${calc_resp.data[r]}</p>`
        $("#results").append(htmlStr)
    }

    let grid_name_html = `<p> Grid: ${zip_resp.data.ba}</p>`
    let grid_emission = `<p> Current Emissions (%): ${zip_resp.data.percent}`

    $("#results").append(grid_name_html)
    $("#results").append(grid_emission)
})