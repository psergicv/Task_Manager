const inputs = document.querySelectorAll(".input");


function addcl(){
	let parent = this.parentNode.parentNode;
	parent.classList.add("focus");
}

function remcl(){
	let parent = this.parentNode.parentNode;
	if(this.value == ""){
		parent.classList.remove("focus");
	}
}


inputs.forEach(input => {
	input.addEventListener("focus", addcl);
	input.addEventListener("blur", remcl);
})

// Get the side menu element
var sideMenu = document.querySelector(".navbar");

// Get the offset position of the menu
var menuPosition = sideMenu.offsetTop;

// Add an event listener to the window to listen for scroll events
window.addEventListener("scroll", function() {
  // Check if the current scroll position is greater than the menu's offset position
  if (window.pageYOffset > menuPosition) {
    // If it is, add the "sticky" class to the menu
    sideMenu.classList.add("sticky");
  } else {
    // If it isn't, remove the "sticky" class from the menu
    sideMenu.classList.remove("sticky");
  }
});