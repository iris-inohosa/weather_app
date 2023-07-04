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
                    $(this).val('');
                    // get weather data and update html values
                    updateUI(data, city);
                    // reset autocompletet term value
                    $('#city-search').data().uiAutocomplete.term = null;
                })
            })
        });
    });

    function updateUI(data, city) {
        $('.weather-current').removeClass('hide-block');
        $('.weather-forecast').removeClass('hide-block');
        $('#today-title').html(`<b>${city}</b>`);
        $('#temperature').html(data.temperature + '°C');
        $('.extras').html('');
        $('.extras').append(`<li class='p-1'><i class="fa-solid fa-droplet px-2"></i>Humidity: ${data.relHumidity}%</li>`);
        $('.extras').append(`<li class='p-1'><i class="fa-solid fa-wind px-2"></i>Wind: ${data.windDirString} ${data.windSpeed}km/h</li>`);
        $('.extras').append(`<li class='p-1'><i class="fa-solid fa-cloud px-2"></i>Cloudiness: ${data.cloudiness}%</li>`);
        $('.extras').append(`<li class='p-1'><i class="fa-solid fa-temperature-quarter px-2"></i>Pressure: ${data.pressure}Pa</li>`);
        $('#weather-symbol').attr('src', `https://developer.foreca.com/static/images/symbols/${data.symbol}.png`);
        $('.symbol-phrase').html(`${data.symbolPhrase}, feels like ${data.feelsLikeTemp}°C`);
    }


})();