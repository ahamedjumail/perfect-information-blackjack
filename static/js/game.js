$(document).ready(function() {

})

/* disbale "HIT" and "STAND" if a verdict was passed 
if a verdict was passed Enable/Display "NEXT PLAYER" button */
function console_guidance(game_verdict) {
    if (game_verdict !== "UNDECIDED") {
        $("#hit").prop('disabled', true);
        $("#stand").prop('disabled', true);
        $('#next').removeAttr('disabled');
    }
    else {
        $('#hit').removeAttr('disabled');
        $('#stand').removeAttr('disabled');
        $("#next").prop('disabled', true);
        $("#next").css('visibility', 'hidden')
    }
}

/* Guidance (change mini counter colour to green) - user has blackjack, no need to hit! */
function miniCounterGuidance(player_verdict) {
    if (player_verdict === "BLACKJACK") {
        $(".mini_counter").css("background-color", "green")
        $(".mini_counter").css("border", "3px solid #000000")
        $(".mini_counter").css("border-radius", "5px")
        $(".mini_counter > p").css("color", "black")
    }
}

/* Guidance (change "STAND" colour to green) - hand is good enough to "STAND" */
function standGuidance(player_count) {
    if (player_count <= 21 && player_count > 17) {
        $("#stand").addClass("console-btn-next")
    }
}
