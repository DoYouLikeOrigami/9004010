var indexModule = (function () {

	var init = function () {
		_setUpListeners();
		_slick();
	};

	var _setUpListeners = function () {
		//$('.service__link-popup').on('click', _showPopup);
	};

	var _slick = function () {
		$('.clients__slider').slick({
			infinite: true,
		    slidesToShow: 3,
		    slidesToScroll: 3,
		    autoplay: true
		});
	}

	var _showPopup = function (e) {
		e.preventDefault();
		var $this = $(this),
			id = $this.attr('id'),
			arr = id.split('-'),
			indx = arr[1],
			bPopup = $('#service__popup-' + indx);
		bPopup.bPopup({
			speed: 550,
			transition: 'slideDown',
			modalColor: '#7E8C99',
			opacity: 0.75,
		});
	};
	
	return {
		init: init
	};

})();

indexModule.init();
