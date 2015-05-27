
// the link to js is working now!

console.log("linked jscript working!");

console.log("activated actionLinks!");
$('.actionLinks a').click( function(event) { 
                  event.preventDefault();
                    var actionObj = this.dataset;
                    console.log(actionObj); 
                    $.post("/action", 
                         { tag_id: actionObj.tagid,
                            article_id: actionObj.articleid,
                            action_type: actionObj.linktype
                          }, 
                          function (result) { alert(result) }
                          );
                          });

// changed slider to carousel mode
$(document).ready(function(){
  $('.slider1').bxSlider({
    slideWidth: 200,
    minSlides: 3,
    maxSlides: 5,
    slideMargin: 10
  });
});

// toDo. Check out slick carousel slider for the more options like:
// Center mode
// "Slider Syncing" = the centered slide takes up the top bar, featured
// http://kenwheeler.github.io/slick/

