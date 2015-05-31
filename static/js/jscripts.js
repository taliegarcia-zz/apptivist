
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

                  // post url in form to server, returns opengraph data based on url
                  "/preview",
                  { url: data },

                  // insert preview into html
                  function (result) { 
                  $("#previewDiv").html('<strong>Headline: </strong>' + result.title 
                                        + '<br><img src="' + result.img 
                                        + '" /><br><strong>Description: </strong>' + result.desc);
                  $("#postArticle").attr({
                      "data-title" : result.title,
                      "data-img" : result.img
                    });
                 });
              }

// new problem. now need to post this to my server. 
              $("#url-field").change( function() { 
                                      if (checkUrl($(this).val())) {
                                        getPreview($(this).val());
                                      } else {
                                        $("#checkURL").html("Please enter a valid url.");
                                      };
                                    });

// working on posting to "/post_article"
$("#newArticle")

$("#postArticle").submit( function(e) { 
            e.preventDefault(); 
            console.log(this.dataset.title); 
            console.log(this.dataset.img); 
            console.log($("#date-field").val());
            console.log($("#url-field").val());
            // console.log("Checked for checkboxes: " + $("input:checked").val());
            var allTags = [];
            $("input:checked").each(function () {
              allTags.push($(this).val());
            });
            console.log("Print array of all tags: " + allTags);
            console.log(allTags);
           });


   
 