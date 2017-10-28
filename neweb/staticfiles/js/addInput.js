var counter = 1;
function addInput(divName){
     
          var newdiv = document.createElement('div');
          newdiv.innerHTML = "<div class='input-field col s10 offset-s1'><input type='text' name='foodItem' id='item"+(counter+1)+"><label  for='item"+(counter+1)+"'>Food Item - "+(counter+1)+"</label></div>";
          document.getElementById(divName).appendChild(newdiv);
          counter++;
     
}
