/* global $ */
$(document).ready(function() {

  // changes the number of text inputs on the fly.  
  $("#players").change(function() {
    set_players($("#players")); // passing in item $("#players") into the function
  })

  // disable enter on the form, this will stop incomplete form submissions,  
  $(document).on('keyup keypress', 'form input[type="text"]', function(event) {
    if (event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

  // jQuery smooth scroll
  var allLinks = $("a") // targetting all the links
  smoothScroll(allLinks) // Add smooth scrolling to all links

})


// simplified version of console.log to be used for debugging 
function log(...args) {
  // prints however many parameters passed in
  console.log(...args)
}


// change the number of text inputs
function set_players(item) {

  // get item's current value
  var count = item.val();

  // logic to change number of text input based on the selection made by the user.
  if (count === "3") {
    $(".extend").html(`<label class="ml-3">Player 3: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Yoni" minlength="2" maxlength="7" required/></label><br>`)
  }
  else if (count === "4") {
    $(".extend").html(`<label class="ml-3">Player 3: &nbsp<input class="form-control-sm" type="text" name="username" placeholder=" Yoni" minlength="2" maxlength="7" required/></label><br><label class="ml-4">Player 4: &nbsp<input class="form-control-sm" type="text" name="username" placeholder="" minlength="2" maxlength="7" required/></label><br>`)
  }
  else {
    $(".extend").html(``)
  }
}


// jQuery smooth scroll
function smoothScroll(element) {

  element.on('click', function(event) {

    // Make sure this.hash has a value before overriding default behavior
    if (this.hash !== "") {
      // Prevent default anchor click behavior
      event.preventDefault();

      // Store hash
      var hash = this.hash;

      // Using jQuery's animate() method to add smooth page scroll
      // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
      $('html, body').animate({
        scrollTop: $(hash).offset().top
      }, 1500);
    } // End if
  });
}
