
function showCardWithDelay() {
    setTimeout(function() {
      var card = document.querySelector('.card-delay');
      card.style.display = 'block';
    }, 4500);
  }
  
window.onload = showCardWithDelay;

