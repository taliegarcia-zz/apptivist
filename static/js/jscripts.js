
// the link to js is working now!

console.log("linked jscript working!");

// This function enables the site to track users' action-items, such as meetup/giving/congress
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

// Preview article posting, getting Headline, Image, and Description 
function getPreview(evt) {
                evt.preventDefault();
                $.post(
                  "/preview",
                  { url: $("#url-field").val() },
                  function (result) {
                    $("#preview").html('<strong>Headline:</strong> ' + result.title 
                                        + '<br><img src="' + result.img 
                                        + '" /><br><strong>Description: </strong>' + result.desc);
                  }
                );
              }


              $("#preview-form").on("submit", getPreview);


 