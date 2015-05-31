
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
   
            var allTags = [];
                $("input:checked").each(function () {
                  allTags.push($(this).val());
                  return allTags;
                });
            
            console.log("Tags after first assignment: " + allTags);

            var formInfo = { title: this.dataset.title,
              img_src: this.dataset.img,
              url: $("#url-field").val(),
              date: $("#date-field").val(),
              tag_list: allTags
            }

            console.log("Obj first assigned: " + formInfo);
            console.log("Tags after object is assigned: " + allTags);

            $.post("/post_article", formInfo, 
                function(r) {
                   alert("Got " + r); 
                });

            console.log("Obj after posting to db: " + formInfo)
            console.log("Tags after posted to db: " + allTags);

           });


   
 