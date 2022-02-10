$(function(e){
    let location=window.location;
    let root_url=location.protocol+"//"+location.host;
    var trouve=false;
    $.when(
        $(".activate-current-url >ul li > a,.activate-current-url button").each(function(elt){
            let potential_url=root_url+"/"+$(this).attr("href");
            let potential_url2=root_url+$(this).attr("href");
            if(potential_url==location || potential_url2==location){
                $(this).addClass("active");
                trouve=true;
            }
        })
    ).done(function(event){
        if(trouve==false){
            $(".activate-current-url button").addClass("active")
        }
    });
});