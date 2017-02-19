var mainModule = (function () {

	var init = function () {
		_setUpListeners();
	};

	var _setUpListeners = function () {
		$('.contacts__button').on('click', _showPopup);
		$('.city__select').on('change', _changeCity);
		$('.buttonUp').on('click',_buttonUp);
		$(window).on('scroll',_triangleWhere);
		$('.products__buy-btn').on('click', _showOrderPopup);
		$('.order-popup__form').on('submit', _makeOrder);
		$('.orderCall__form').on('submit', _orderCall);
		$('.mobile-menu__button').on('click', _showMenuPopup);
	};

	var _showSuccPopup = function (message) {
		console.log('show succ');
		var succPopup = $('.info-popup--success').text(message);
		succPopup.fadeIn(400, function() {
			var timer = setTimeout(function() {
				succPopup.fadeOut('400');
			}, 2000);
		});
	}

	var _showErrPopup = function (message) {
		console.log('show error');
		var errPopup = $('.info-popup--error').text(message);
		errPopup.fadeIn(400, function() {
			var timer = setTimeout(function() {
				errPopup.fadeOut('400');
			}, 2000);
		});
	}

	var _request = function(method, url, data, fn) {
    var xhr = new XMLHttpRequest();
    xhr.open(method, url);
    xhr.setRequestHeader('Content-Type', 'application/json;charset=UTF-8');
    //xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');


    xhr.addEventListener('readystatechange', function () {
      if (xhr.readyState == 4) {
        fn(xhr.responseText);
      }
    });
    xhr.send(JSON.stringify(data));
  };

	var _showPopup = function (e) {
		e.preventDefault();
		var bPopup = $('.orderCall__popup'),
		    currentCityMail = $('.city-mail--active a').text(),
		    cityMail = bPopup.find('.city-mail-input').val(currentCityMail);

		bPopup.bPopup({
			speed: 550,
			transition: 'slideDown',
			modalColor: '#7E8C99',
			opacity: 0.75,
		});
	};

	var _hidePopup = function (e) {
		if (e) {
			e.preventDefault();
		}
		var popup = $('.orderCall__popup');
		popup.bPopup();
		popup.close();
	};

	var _hideOrderPopup = function (e) {
		if (e) {
			e.preventDefault();
		}
		var popup = $('.order-popup');
		popup.bPopup();
		popup.close();
	};

	var _showOrderPopup = function (e) {
		e.preventDefault();
		var orderPopup = $('.order-popup'),
		    orderPopupBody = orderPopup.find('.order-popup__body'),
		    btn = $(this),
		    good = btn.closest('.products__item'),
		    goodsName = good.find('.products__attr-name').text(),
		    popupGoodsName = orderPopupBody.find('.order-popup__text--name strong').text(goodsName),
		    currentCityMail = $('.city-mail--active a').text(),
		    cityMail = orderPopup.find('.city-mail-input').val(currentCityMail);
		orderPopup.bPopup({
			speed: 550,
			transition: 'slideDown',
			modalColor: '#7E8C99',
			opacity: 0.75,
			closeClass: 'order-popup__btn--close'
		});
	};

	var _showMenuPopup = function (e) {
		e.preventDefault();
		var menuPopup = $('.menu-popup');

		menuPopup.bPopup({
			speed: 550,
			transition: 'slideDown',
			modalColor: '#7E8C99',
			opacity: 0.75,
			closeClass: 'order-popup__btn--close'
		});
	};

	var _makeOrder = function (e) {
		e.preventDefault();
		var form = $(this),
		    goodsName = form.find('.order-popup__text--name strong').text() || "Не заполнено",
		    userMail = form.find('.order-popup__input--mail').val() || "Не заполнено",
		    userTel = form.find('.order-popup__input--tel').val() || "Не заполнено",
		    goodsComment = form.find('.order-popup__textarea').val() || "Не заполнено",
		    sendTo = form.find('.city-mail-input').val() || false,
		    btn = form.find('.order-popup__btn--order'),
		    method = form.attr('method'),
		    action = form.attr('action'),
		    data = {
		    	good: goodsName,
		    	mail: userMail,
		    	tel: userTel,
		    	comment: goodsComment,
		    	sendTo: sendTo
		    };

		if (!sendTo) {
			_showErrPopup('Ошибка. Обновите страницу.');
			return;
		}

		btn.val('Отправка...')

    _request(method, action, data, function (response) {
      if (response == 'OK') {
        console.info('Успешно отправлено');
        _showSuccPopup('Заявка получена');
      }
      else {
        console.info('Ошибка');
        _showErrPopup('Ошибка на сервере');
      }

      _hideOrderPopup();
      btn.val('Заказать');
    });
	};

	var _orderCall = function (e) {
		e.preventDefault();
		var form = $(this),
		    tel = form.find('input[type=tel]'),
		    btn = form.find('.orderCall__form-button'),
		    sendTo = form.find('.city-mail-input').val() || false,
		    action = form.attr('action'),
		    method = form.attr('method'),
		    data = {
		    	tel: tel.val(),
		    	sendTo: sendTo
		    };

		if (!sendTo) {
			_showErrPopup('Ошибка. Обновите страницу.');
			return;
		}

		if (tel.val() === "") {
			_showErrPopup('Ошибка. Введите номер телефона.');
			return;
		}

		btn.val('Отправка...');

    _request(method, action, data, function (response) {
      if (response == 'OK') {
        console.info('Успешно отправлено');
        _showSuccPopup('Мы скоро Вам перезвоним');
      }
      else {
        console.info('Ошибка');
        _showErrPopup('Ошибка на сервере');
      }

      btn.val('Заказать звонок');
      tel.val('');
      _hidePopup();
    });
	};

	var _changeCity = function (e) {

		var $this = $(this),
			city = $this.val(),
			city__class = '.' + city + '-city',
			city__obj = $(city__class);

		$('.city-change').addClass('hidden');
		$('.city-mail').removeClass('city-mail--active');

		for (var i = 0; i < city__obj.length; i++) {
			if ($(city__obj[i]).hasClass('city-mail')) {
				$(city__obj[i]).addClass('city-mail--active');
			}
		}

		city__obj.removeClass('hidden');
	};

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
  };

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
	};

	return {
		init: init
	};

})();

mainModule.init();
