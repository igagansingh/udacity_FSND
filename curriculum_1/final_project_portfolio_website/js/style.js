var homeIcon = document.getElementsByTagName('.c100');
window.onResize = function() {
  if (window.innerWidth <= 592) homeIcon.classList.add("small");
  else homeIcon.classList.remove("small");
};