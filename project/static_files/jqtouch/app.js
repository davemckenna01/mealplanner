var jQT = new $.jQTouch({
    icon: 'jqtouch.png',
    addGlossToIcon: false,
    startupScreen: 'jqt_startup.png',
    statusBar: 'black',
    formSelector: '.form',
    preloadImages: [
        '/static_files/lib/jqtouch/themes/jqt/img/back_button.png',
        '/static_files/lib/jqtouch/themes/jqt/img/back_button_clicked.png',
        '/static_files/lib/jqtouch/themes/jqt/img/button_clicked.png',
        '/static_files/lib/jqtouch/themes/jqt/img/grayButton.png',
        '/static_files/lib/jqtouch/themes/jqt/img/whiteButton.png',
        '/static_files/lib/jqtouch/themes/jqt/img/loading.gif'
        ]
});

$(function(){

    
    var $li_no_a = $("<li class='arrow'></li>");
    var $li_w_a = $("<li class='arrow'><a></a></li>");

    var $back_btn_basic = $("<a class='back'>Back</a>");


    var $ul_rounded = $("<ul class='rounded'></ul>");

    var p = "";
    p += "<div>";
        p += "<div class='toolbar'>";
            p += "<h1></h1>";
        p += "</div>";
    p += "</div>";

    var $generic_page_list = $(p);

    
    

    function add_list_items(page, list_num, anchors, data, page_id, title_text_label){
        var title_text = eval("data."+title_text_label);
        if (anchors){
            var $list_item = $li_w_a.clone();
            var $anchor = $list_item.children("a")
            $anchor.html(title_text);
            $anchor.attr('href', "#" + page_id);
        } else {
            var $list_item = $li_no_a.clone();
            $list_item.html(title_text);
        }
        page.children('.list_' + list_num).append($list_item);
    }

    function create_page($page, page_id, page_class, data){
        var $child_page = $generic_page_list.clone();
        $child_page.attr('id', page_id);
        $child_page.addClass(page_class);
        $child_page.children('.toolbar').children('h1').html(data.name);
        var $back_btn = $back_btn_basic.clone();
        $child_page.children('.toolbar').append($back_btn);

        var $ul = $ul_rounded.clone();
        $ul.addClass("list_1");
        $child_page.append($ul);

        $child_page.data('obj_id', data.id)
        $('body').append($child_page);
    }

    $("#meals").bind("pageAnimationEnd", function(e, info){
        if (info.direction == "out") return;

        var $page = $(this);
        if ($page.data("loaded")) return;

        $.ajax({
            url: "/api/meals/",
            cache: false,
            success: function(data){
                $.each(data, function(){

                    var page_id = "meals" + "_" + this.id;

                    if ($("#" + page_id).length == 0){
                        create_page($page, page_id, "meals_item", this);
                    }
                    
                    add_list_items($page, 1, true, this, page_id, "name");

                });
                $page.data("loaded", true);

            },
            error: function(a, b, c){
                alert (a + b + c);
            }
        });
    });


    $(".meals_item").live("pageAnimationEnd", function(e, info){
        
        if (info.direction == "out") return;

        var $page = $(this);
        
        if ($page.data("loaded")) return;

        $.ajax({
            url: "/api/meals/" + $(this).data("obj_id") + "/",
            cache: false,
            success: function(data){
                $.each(data.dishes, function(){

                    var page_id = "dishes_" + this.id;

                    if ($("#" + page_id).length == 0){
                        create_page($page, page_id, "dishes_item", this);
                    }

                    add_list_items($page, 1, true, this, page_id, "name");

                });

                $page.data("loaded", true);

            },
            error: function(a, b, c){
                alert (a + b + c);
            }
        });
    });


    $(".dishes_item").live("pageAnimationEnd", function(e, info){

        if (info.direction == "out") return;

        var $page = $(this);



        if ($page.data("loaded")) return;

        $page.append("<a class='delete_dish'>Delete</a>");

        $(".delete_dish").tap(function(){
            $.ajax({
                url: "/api/dishes/" + $page.data("obj_id") + "/",
                cache: false,
                type: "DELETE",
                success: function(data){
                    console.log(data);

                },
                error: function(a, b, c){
                    console.log(a, b, c);
                }
            });
        });

        $.ajax({
            url: "/api/dishes/" + $(this).data("obj_id") + "/",
            cache: false,
            success: function(data){
                $.each(data.ingredients, function(){

                    var page_id = "ingredients_" + this.id;
                    
                    add_list_items($page, 1, false, this, page_id, "shrt_desc");

                });

                $page.data("loaded", true);

            },
            error: function(a, b, c){
                alert (a + b + c);
            }
        });
    });



    $("#dishes").bind("pageAnimationEnd", function(e, info){
        if (info.direction == "out") return;

        var $page = $(this);
        if ($page.data("loaded")) return;

        $.ajax({
            url: "/api/dishes/",
            cache: false,
            success: function(data){
                $.each(data, function(){

                    var page_id = "dishes_" + this.id;

                    if ($("#" + page_id).length == 0){
                        create_page($page, page_id, "dishes_item", this);
                    }

                    add_list_items($page, 1, true, this, page_id, "name");

                });
                
                $page.data("loaded", true);

            },
            error: function(a, b, c){
                alert (a + b + c);
            }
        });
    });


    $("#weeks").bind("pageAnimationEnd", function(e, info){
        if (info.direction == "out") return;

        var $page = $(this);
        if ($page.data("loaded")) return;

        $.ajax({
            url: "/api/weeks/",
            cache: false,
            success: function(data){
                $.each(data, function(){

                    var page_id = "weeks_" + this.id;

                    if ($("#" + page_id).length == 0){
                        create_page($page, page_id, "weeks_item", this);
                    }

                    add_list_items($page, 1, true, this, page_id, "name");

                });

                $page.data("loaded", true);

            },
            error: function(a, b, c){
                alert (a + b + c);
            }
        });
    });


    $(".weeks_item").live("pageAnimationEnd", function(e, info){
        if (info.direction == "out") return;

        var $page = $(this);
        if ($page.data("loaded")) return;

        $.ajax({
            url: "/api/weeks/" + $(this).data("obj_id") + "/",
            cache: false,
            success: function(data){
                $.each(data.days, function(){

                    var page_id = "days_" + this.id;

                    if ($("#" + page_id).length == 0){
                        create_page($page, page_id, "days_item", this);
                    }

                    add_list_items($page, 1, true, this, page_id, "name");

                });

                $page.data("loaded", true);

            },
            error: function(a, b, c){
                alert (a + b + c);
            }
        });
    });


    $(".days_item").live("pageAnimationEnd", function(e, info){
        if (info.direction == "out") return;

        var $page = $(this);
        if ($page.data("loaded")) return;

        $.ajax({
            url: "/api/days/" + $(this).data("obj_id") + "/",
            cache: false,
            success: function(data){

                var meal_types = new Array();
                $.each(data.entry_set, function(){                     
                    if ($.inArray(this.meal_type.name, meal_types) == -1){
                        meal_types.push(this.meal_type.name);
                    }
                });

                //create enough ul's so that there are as many
                //ul's as meal types
                for (var i=0; i < meal_types.length - 1; i++){
                    var $ul = $ul_rounded.clone();
                    $ul.addClass("list_" + (i + 2));
                    $page.append($ul);
                }

                for (var i=0; i < meal_types.length; i++){
                    $page.children(".list_" + (i+1)).before("<h2>" + meal_types[i] + "</h2>");
                }

                $.each(data.entry_set, function(){

                    var page_id = "meals_" + this.meal.id;

                    if ($("#" + page_id).length == 0){
                        create_page($page, page_id, "meals_item", this.meal);
                    }

                    var meal_type_num = $.inArray(this.meal_type.name, meal_types) + 1;
                    add_list_items($page, meal_type_num, true, this.meal, page_id, "name");
                    
                });

                $page.data("loaded", true);

            },
            error: function(a, b, c){
                alert (a + b + c);
            }
        });
    });


    $("#find").bind("pageAnimationEnd", function(e, info){
        //API Key
        //ABQIAAAA8ux2_Z3In8tQ-TG0_HvZNBTUn9YBxdDplu4o-4qP5p4rw5-j2BTY_CcWNyHLXmZo_eXzvinYpTgQVw
        if (info.direction == "out") return;

        var $page = $(this);
        //if ($page.data("loaded")) return;

        function show_map(position){
            var lattitude = position.coords.latitude;
            var longitude = position.coords.longitude;
            
            var lat_lng = new google.maps.LatLng(lattitude, longitude);
            var my_options = {
              zoom: 13,
              center: lat_lng,
              streetViewControl: true,
              mapTypeId: google.maps.MapTypeId.ROADMAP
            };
            var map = new google.maps.Map(document.getElementById("find"),
                my_options);


            var marker = new google.maps.Marker({
              position: lat_lng,
              map: map,
              title:"You are here dude."
            });

            var win = new google.maps.InfoWindow({
                content: "sheeeeit",
                position: marker.position
            });
            win.open(map);

            var a = new google.maps.LatLng(43.6525, -79.382667);
            var b = new google.maps.LatLng(43.6515, -79.381667);
            var c = new google.maps.LatLng(43.6415, -79.389667);

            var line = new google.maps.Polyline({
               path: new Array(a,b,c),
               map: map,
               strokeColor: "#ff0000",
               strokeWeight: "2"
            });



        }

        navigator.geolocation.getCurrentPosition(show_map);
        


    });



















    $("#dish_create a.submit").tap(function(e){
        var $form = $(this).closest("form");
        return app.create_dish($form);
    });

//    $("#dish_create").submit(function(e){
//        var $form = $(this);
//        return app.create_dish($form);
//    });


    var app = {
        create_dish: function($form){
            $.ajax({
               type: $form.attr("method"), url: $form.attr("action"),
               //dataType: "json",
               data: $form.serialize(),
               complete: function(req){

                   console.log(req);

                   if (req.status == 201){
                       alert("that shit got created.");
                       jQT.goBack();
                   } else {
                       alert("there was an error creating that. try again.");
                   }
               }
            });

            return false;
        }
    };


})
