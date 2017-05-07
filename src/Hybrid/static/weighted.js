$(function() {
	$( "#userUser-slider-vertical" ).slider({
		orientation: "vertical",
		range: "min",
		min: 0,
		max: 100,
		value: 100,
		slide: function( event, ui ) {
			$( "#userUser" ).val( ui.value );
		}
		});
	$( "#userUser" ).val( $( "#userUser-slider-vertical" ).slider( "value" ));
});

$(function() {
	$( "#itemItem-slider-vertical" ).slider({
		orientation: "vertical",
		range: "min",
		min: 0,
		max: 100,
		value: 100,
		slide: function( event, ui ) {
			$( "#itemItem" ).val( ui.value );
		}
		});
	$( "#itemItem" ).val( $( "#itemItem-slider-vertical" ).slider( "value" ));
});

$(function() {
	$( "#contentBased-slider-vertical" ).slider({
		orientation: "vertical",
		range: "min",
		min: 0,
		max: 100,
		value: 100,
		slide: function( event, ui ) {
			$( "#contentBased" ).val( ui.value );
		}
		});
	$( "#contentBased" ).val( $( "#contentBased-slider-vertical" ).slider( "value" ));
});

$('#predict').click(function(){
	var user = $('#user').val();
	var item = $('#item').val();
	var userUser = $('#userUser').val();
	var itemItem = $('#itemItem').val();
	var contentBased = $('#contentBased').val();

	$.get('http://localhost:8000/hybrid/'+user+'/'+item+'/'+userUser+'/'+itemItem+'/'+contentBased, function( data ) {
		$('#status').html(data.status);
		$('#prediction').html(data.prediction);
		if (data.rating)
		{
			$('#ratingSpan').show();
			$('#rating').html(data.rating);
		}
		else
		{
			$('#ratingSpan').hide();
		}
	});
	
})