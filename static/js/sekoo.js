odoo.define('sekoo_web.sekoo', function(require){
	'use strict';

	var toggleTopContent = true;

	$('document').ready(function(){
		console.log('my document is now ready for javascript');

		$('#topMenuToggleDown').click(function(){
			if(toggleTopContent === true){
				$('#header_arrow').text('keyboard_arrow_up');
				toggleTopContent = false;
				$('#toggle-top-content').show();
			}else{
				$('#header_arrow').text('keyboard_arrow_down');
				toggleTopContent = true;
				$('#toggle-top-content').hide();
			}
		});

		$('.header-item').mouseover(function () { 
			$(this).css('box-shadow', '2px 5px 2px rgba(40,40,40,0.1)');
			$(this).children('.sekoo-default-button').show();
		});

		$('.header-item').mouseout(function () { 
			$(this).css('box-shadow', '0px 0px 0px rgba(40,40,40,0.1)');
			$(this).children('.sekoo-default-button').hide();
		});

		$('#close_popup').click(function(){
			console.log('closing popup');
			if($('#popUpInfo').is(':visible')){
				console.log('all got now');
				$('#popUpInfo').attr("style","display:none!important");
				$('#joinNowLink').attr("style","display:flex!important");
			}
		});

		$('#closeSekooTopMenuIn').click(function(){
			console.log('hiding submenu');
			$('#subcontent').hide();
		})
		$('#closeSekooTopMenuOut').click(function(){
			console.log('hiding submenu');
			$('#subcontent').hide();
		})

		// $('.sekoo-default-button').parent().mouseover(function(){
		// 	console.log('hello world...')
		// 	$(this).css('display','block');
		// })
	});
});