$(function () {
    var goToCartIcon = function($addTocartBtn){
      var $cartIcon = $(".my-cart-icon");
      var $image = $('<img width="30px" height="30px" src="' + $addTocartBtn.data("image") + '"/>').css({"position": "fixed", "z-index": "999"});
      $addTocartBtn.prepend($image);
      var position = $cartIcon.position();
      $image.animate({
        top: position.top,
        left: position.left
      }, 500 , "linear", function() {
        $image.remove();
      });
    }

    $('.my-cart-btn').myCart({
      currencySymbol: '₹',
      classCartIcon: 'my-cart-icon',
      classCartBadge: 'my-cart-badge',
      classProductQuantity: 'my-product-quantity',
      classProductRemove: 'my-product-remove',
      classCheckoutCart: 'my-cart-checkout',
      affixCartIcon: true,
      showCheckoutModal: true,
      numberOfDecimals: 2,
      //cartItems: [],
      clickOnAddToCart: function($addTocart){
        goToCartIcon($addTocart);
      },
      afterAddOnCart: function(products, totalPrice, totalQuantity) {
        console.log("afterAddOnCart", products, totalPrice, totalQuantity);
      },
      clickOnCartIcon: function($cartIcon, products, totalPrice, totalQuantity) {
        console.log("cart icon clicked", $cartIcon, products, totalPrice, totalQuantity);
      },
      checkoutCart: function(products, totalPrice, totalQuantity) {

          var dtotal = 0;
      $.each(products, function(index, value){
        dtotal +=  parseInt(value.delivery);
        console.log(dtotal);
        //dtotal = MathHelper.getRoundedNumber(dtotal) * 1;
      });
       console.log(parseInt(dtotal));
       totalPrices = parseInt(totalPrice) + parseInt(dtotal)

	    var list = [];
        var checkoutString = "Total Price: " + totalPrices + "\nTotal Quantity: " + totalQuantity;
        checkoutString += "\n\n id \t name \t summary \t price \t quantity \t image \t path \t delivery";
        $.each(products, function(){
          checkoutString += ("\n " + this.id + " \t " + this.name + " \t " + this.summary + " \t " + this.price + " \t " + this.quantity + " \t " + this.image + " \t " + this.delivery);
          list.push({"total_price": totalPrices,"id":this.id, "name":this.name, "summary":this.summary, "price":this.price, "quantity":this.quantity, "image":this.image, "delivery":this.delivery});
		});
        //alert(checkoutString);
		//alert(typeof list);
		//alert(JSON.stringify(list));
		lists = JSON.stringify(list)
		localStorage.setItem( 'listToPass', lists );
		window.location = "/brushflick/delivery_details/";
        console.log("checking out", products, totalPrice, totalQuantity);
      },
      getDiscountPrice: function(products, totalPrice, totalQuantity) {
          var dtotal = 0;
      $.each(products, function(index, value){
        dtotal +=  parseInt(value.delivery);
        //dtotal = MathHelper.getRoundedNumber(dtotal) * 1;
      });
       totalPrices = parseInt(totalPrice) + parseInt(dtotal)

        console.log("calculating discount", products, totalPrice, totalQuantity);
        //return totalPrice * 0.5;
		return totalPrices;
      }
    });

    $("#addNewProduct").click(function(event) {
      var currentElementNo = $(".row").children().length + 1;
      $(".row").append('<div class="col-md-3 text-center"><img src="images/img_empty.png" width="150px" height="150px"><br>product ' + currentElementNo + ' - <strong>$' + currentElementNo + '</strong><br><button class="btn btn-danger my-cart-btn" data-id="' + currentElementNo + '" data-name="product ' + currentElementNo + '" data-summary="summary ' + currentElementNo + '" data-price="' + currentElementNo + '" data-quantity="1" data-image="images/img_empty.png">Add to Cart</button><a href="#" class="btn btn-info">Details</a></div>')
    });
  });