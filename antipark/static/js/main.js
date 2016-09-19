var mainModule = (function () {

	var init = function () {
		_setUpListeners();
	};

	var _setUpListeners = function () {
		$('.contacts__button').on('click', _showPopup);
		$('.city__select').on('change', _changeCity);
		$('.buttonUp').on('click',_buttonUp);
		$(window).on('scroll',_triangleWhere);
		$('.form').on('submit', _formSubmit);
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

	var _formSubmit = function (e) {
		e.preventDefault();
		
		var form = $(this)
		    data = form.data("form"),
		    action = form.attr("action"),
		    method = form.attr("method"),
		    inputFile = form.find("input[type='file']").val(),
		    btn = form.find("input[type='submit']");

		if (data !== "file") {
			return;
		}

		if (inputFile === "") {
			return;
		}

    btn.attr("value", "Отправка...");

    var formData = new FormData(form),
        xhr = new XMLHttpRequest();
    
    xhr.open(method, action);
    xhr.onreadystatechange = function() {
    	if (xhr.readyState == 4) {
    		if(xhr.status == 200) {
    			data = xhr.responseText;
    			if(data == "OK") {
    				btn.attr("value", "Принято!");
    			} else {
    				btn.attr("value", "Ошибка! Мб ответ не ОК?");
    			}
    		}
    	}
    };

    setTimeout(function() {
    	btn.attr("value", "Загрузить");
    }, 2000);

    xhr.send(formData);
	};
  	
	return {
		init: init
	};

})();

mainModule.init();
