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
	document.getElementById("video").play();
})
