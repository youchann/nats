
console.log('hello')

let tweet_id = ''
let visible_num = 0

for (var i = 0; i < 19; i++){
  $(".display_tweet").eq(i).css("display", "none")
}
$(".display_tweet").eq(0).css("display", "block")
console.log('hello')

$('.btn-audio-play').on('click', function() {
  let tweet_id = $(this).attr('id')
  $(".display_tweet").eq(visible_num).addClass("animated zoomOutDown");

  let a = new Audio('static/voicefiles/' + tweet_id + '.wav')
  a.play()
  a.addEventListener('ended', function(e) {
    console.log('ended')
    $(".display_tweet").eq(visible_num).css("display", "none")
    visible_num += 1
    $(".display_tweet").eq(visible_num).css("display", "block")
  })
})

// loadingの処理（雑にやってるけどとりあえずこれで）
$('.btn-to-mainpage').on('click', function() {
  console.log('抽出開始')
  $('#loading').show()
})
$(document).ready(function() {
  $('#loading').hide()
})
