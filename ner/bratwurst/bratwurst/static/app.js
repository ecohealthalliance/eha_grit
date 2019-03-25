$(document).ready(function () {

    $('#train').click(function () {
        $('#train').text('Training NER Classifier...');
        $.get('train').done(function (data) { $('#train').text('Done! Click to retrain'); });
    });

    $('#test').click(function () {
        var testData = {data: $('#test-data').val()};
        $.post('test', testData).done(function (data) { $('#test-results').html(data); }); 
    });

});