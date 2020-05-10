$("#appliance-select").change(async function() {
    let appliance = $(this).find("option:selected").val();
    let resp = await axios.get(`/watts/${appliance}`)
     $("#wattage").val(resp.data.wattage)
})

$("#days").on("blur", async function(){
    let resp = await axios({
        method: 'get',
        url: '/calculate',
        //headers: {"X-CSRFToken": csrfToken}
    })

    console.log(resp)
})