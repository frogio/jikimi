$(function () {
    $(document).scroll(function () {
        var $nav = $("#mainNavbar");
        $nav.toggleClass("scrolled", $(this).scrollTop() > $nav.height());
    });
});

$(document).on('click', '.cctv-li', function(e){
  // alert("isWorking?");

	$("video").attr("src", $(this).attr("id"));	
	$("video")[0].load();				// 위 함수를 호출해야 영상 소스를 바꿔서 재생 가능
	// document.getElementById("video").play();
})


// function detectReszie() {
  
  
// }
// window.addEventListener("resize", function() {
//   if (matchMedia("screen and (max-width: 768px)").matches) {

//     let video = document.querySelector('.cctv-left');
//     let div_wrp = document.querySelector(".cctv-wrapper");
//     div_wrp.appendChild(video);
  
//   } else {

//     let video = document.querySelector('.cctv-right');
//     let div_wrp = document.querySelector(".cctv-wrapper");
//     div_wrp.appendChild(video);
//   }

// })

var elem = document.getElementsByTagName("video");
  /* View in fullscreen */
function openFullscreen() {
  if (elem.requestFullscreen) {
    elem.requestFullscreen();
  } else if (elem.webkitRequestFullscreen) { /* Safari */
    elem.webkitRequestFullscreen();
  } else if (elem.msRequestFullscreen) { /* IE11 */
    elem.msRequestFullscreen();
  }
}

  /* Close fullscreen */
function closeFullscreen() {
  if (document.exitFullscreen) {
    document.exitFullscreen();
  } else if (document.webkitExitFullscreen) { /* Safari */
    document.webkitExitFullscreen();
  } else if (document.msExitFullscreen) { /* IE11 */
    document.msExitFullscreen();
  }
}

