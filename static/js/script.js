
    function showInfo(btnNum) {
      // Hide all info divs
      var infoDivs = document.querySelectorAll('.info');
      infoDivs.forEach(function(div) {
        div.style.display = 'none';
      });

      // Show the selected info div
      var selectedInfo = document.getElementById('info' + btnNum);
      selectedInfo.style.display = 'block';
    }


    


    

    
  