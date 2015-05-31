
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

// function for checking valid url, using regex from msdn.microsoft.com
function checkUrl(url) {
    return /^(ht|f)tp(s?)\:\/\/[0-9a-zA-Z]([-.\w]*[0-9a-zA-Z])*(:(0-9)*)*(\/?)([a-zA-Z0-9\-\.\?\,\'\/\\\+&amp;%\$#_]*)?$/.test(url);
}

// Preview article posting, getting Headline, Image, and Description 
function getPreview(data) {
                $.post(
                  "/preview",
                  { url: data },
                  function (result) {
                   
                  $("#previewDiv").html('<strong>Headline: </strong>' + result.title 
                                        + '<br><img src="' + result.img 
                                        + '" /><br><strong>Description: </strong>' + result.desc);
                    
                    

                  }
                );
              }
// new problem. now need to post this to my server. 
              $("#url-field").change( function() { 
                                      if (checkUrl($(this).val())) {
                                        getPreview($(this).val());
                                      } else {
                                        $("#checkURL").html("Please enter a valid url.");
                                      };
                                    });

// working on posting to "/new_post"
                  $("#newpost-form").on("submit", function () { $.post('/new_post',
                                                      article,                                                       
                                                      function () {
                                                        alert("posted new article!");
                                                      })  
                                                      });

 