var mainModule = (function () {

	var init = function () {
		_setUpListeners();
	};

	var _setUpListeners = function () {
		$('.contacts__button').on('click', _showPopup);
		$('.city__select').on('change', _changeCity);
		$('.buttonUp').on('click',_buttonUp);
		$(window).on('scroll',_triangleWhere);
	};

	var _showPopup = function (e) {
		e.preventDefault();
		var bPopup = $('.orderCall__popup');
		bPopup.bPopup({
			speed: 550,
			transition: 'slideDown',
			modalColor: '#7E8C99',
			opacity: 0.75,
		});
	};

	var _changeCity = function (e) {

		var $this = $(this),
			city = $this.val(),
			city__class = '.' + city + '-city';

		$('.city-change').addClass('hidden');
		$(city__class).removeClass('hidden');
	}

	var _createQtip = function (el) {
		
		var pos = {
			my: 'right center',
			at: 'left center'
			},
			text = el.attr('qtip-text');
	
		el.qtip({
			content: {
				text: text
			},
			show: {
				event: 'show'
			},
			hide: {
				event: 'keydown hideTooltip'
			},
			position: pos,
			style: {
				classes: 'qtip qtip-rounded'
			}
			}).trigger('show');

	};


	var _buttonUp = function () {
		var scroll = $(window).scrollTop();
		if (scroll>0) {
			$('html, body').animate({scrollTop: 0	}, 600);
			$('.buttonUp').attr('href', scroll);
		}
	    else {
			$('html, body').animate({scrollTop: $('.buttonUp').attr('href')}, 600);
	}
	return false;
}
	var _triangleWhere = function (e) {
		e.preventDefault;
		if ($(window).scrollTop()>0) {
			$('.buttonUp-body').removeClass('buttonUp-transform');
			$('.buttonUp').css('display','block');
		}
		else if (!$('.buttonUp').attr('href')) {
			$('.buttonUp').css('display','none');
		}
		else {
			$('.buttonUp-body').addClass('buttonUp-transform');
		}
	}
  	
	return {
		init: init
	};

})();

mainModule.init();
