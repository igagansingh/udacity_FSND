var responsive=true;
function myFunction(x) {
     x.classList.toggle("change");
     if(responsive == false){
          document.getElementById('filter_id').style.width = "100%";
          document.getElementById('items').style.width = "100%";
          document.getElementById('list').style.width = "22%";
          document.getElementById('map').style.width = "78%";
          $('#name_id').html("Neighborhood Map");
          $('#search_id').show();
          responsive = true;
     } else{
          document.getElementById('filter_id').style.width = "0px";
          document.getElementById('items').style.width = "0px";
          document.getElementById('list').style.width = "0px";
          document.getElementById('map').style.width = "100%";
          $('#name_id').html("");
          $('#search_id').hide();
          responsive = false;
     }
}
