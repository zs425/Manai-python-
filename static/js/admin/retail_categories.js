$(document).ready(function(){
  $("#id_categories > option").each(function(index) {
      //alert(index + ': ' + $(this).text());
      if($(this).text().indexOf("Wholesale Shop") === 0 || $(this).text().indexOf("Shop") === 0){
        $(this).remove();
      }
  });

  $(".margin").remove();

  $(".edit-link").each(function(){
    $(this).attr("href", $(this).attr("href") + "/" + location.search )
  })

});