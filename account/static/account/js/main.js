
$(function() {
        $('.material-card > .mc-btn-action').click(function () {
            var card = $(this).parent('.material-card');
            var icon = $(this).children('i');
            icon.addClass('fa-spin-fast');

            if (card.hasClass('mc-active')) {
                card.removeClass('mc-active');

                window.setTimeout(function() {
                    icon
                        .removeClass('fa-arrow-left')
                        .removeClass('fa-spin-fast')
                        .addClass('fa-bars');

                }, 800);
            } else {
                card.addClass('mc-active');

                window.setTimeout(function() {
                    icon
                        .removeClass('fa-bars')
                        .removeClass('fa-spin-fast')
                        .addClass('fa-arrow-left');

                }, 800);
            }
        });
    });



var LikeListPage = {
	init: function() {
		this.$container = $('.art-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-like', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.fa-thumbs-o-up', self).toggleClass('active');
					$(result.like).text((result.count).toString());
				}
			});

			return false;
		});
	}
};

var FlagListPage = {
	init: function() {
		this.$container = $('.art-container');
		this.render();
		this.bindEvents();
	},

	render: function() {

	},

	bindEvents: function() {
		$('.btn-flag', this.$container).on('click', function(e) {
			e.preventDefault();

			var self = $(this);
			var url = $(this).attr('href');
			$.getJSON(url, function(result) {
				if (result.success) {
					$('.glyphicon-flag', self).toggleClass('active');
					$(result.flag).text((result.count).toString());
				}
			});

			return false;
		});
	}
};


$(document).ready(function() {
	LikeListPage.init();
	FlagListPage.init();
});

$(function(){
    $('.niceimg').Chocolat({
        imageSize: 'contain'
    });
});

