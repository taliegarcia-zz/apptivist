$.post("/action",
        actionObj, 
        function() {
            alert('wow');
        });

            // or combine with variable...and function...
             var myObj = $('.actionLinks a').click( function(event) { 
                                                        event.preventDefault;
                                                        $.post("/action",
                                                            this.dataset
                                                        );
                                                    });




$.post("/action",
        { name: 'Jessica', age: 27 }, 
        function() {
            alert('wow');
        });


$('.actionLinks a').click( function(event) { 
                                event.preventDefault();
                                var superObj = this.dataset,
                                return superObj; 
                                });