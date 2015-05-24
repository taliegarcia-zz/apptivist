
// I don't know how to link this to my html pages yet!
// FIXME. how do I link to this on the base.html

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

// $('.actionLinks a').click(function(event) { 
//                           event.preventDefault();
//                           var myObj = this.dataset;
//                           return console.log(myObj); 
//                         });

