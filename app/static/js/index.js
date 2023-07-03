(() => {
    $(function () {
        $("#city-search").autocomplete({
            source: `api/get-cities/${$('#city-search').val()}`,
            //source: availableTags,
            minLength: 3,
            //delay: 500,
            select: function (event, ui) {
                const city = ui.item.label;
                const cityId = ui.item.value
                // set selected value to stockname
                $(this).val(city);
                $(this).attr('city-id', cityId);
                //setStockCardValues(stockName, 'abcndf', 'abcndf', 'abcndf', 'abcndf');
                return false;
            }
        });
    });
    $(document).ready(function () {
        $('#city-search').on('autocompletechange', function () {
            let city = this.value;
            let cityId = $(this).attr('city-id')
            fetch(`/get-current-weather/${cityId}`).then(resp => {
                resp.json().then(data => {
                    // get weather data and update html values
                    console.log(data);
                    $('#today-title').html('Today in ' + city);
                    $('#temperature').html(data.temperature);

                })
            })
        });
    });


})();