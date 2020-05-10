$("#appliance-select").change(async function() {
    let appliance = $(this).find("option:selected").val();
    let resp = await axios.get(`/watts/${appliance}`)
     $("#wattage").val(resp.data.wattage)
})

$("#days").on("blur", async function(){
    let resp = await axios({
        method: 'get',
        url: '/calculate',
        params: {
            wattage: $("#wattage").val(),
            rate: $("#rate").val(),
            hours: $("#hours").val(),
            days: $("#days").val()
        }
    })
    console.log(resp.data)
    for (let r in resp.data){
        let htmlStr = `<p>${r}: ${resp.data[r]}</p>`
        $("#results").append(htmlStr)
    }
})