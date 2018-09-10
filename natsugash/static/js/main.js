
console.log('hello')

let tweet_id = ''
let visible_num = 0
console.log('hello')

for (var i = 0; i < 19; i++){
  $(".row").eq(i).css("display", "none")
}
$(".row").eq(0).css("display", "block")
console.log('hello')

$('.btn-audio-play').on('click', function() {
  let tweet_id = $(this).attr('id')
  console.log(tweet_id)
  // let substr_tweet_id = tweet_id.substr(5)
  // console.log(substr_tweet_id)
  let a = new Audio('static/voicefiles/' + tweet_id + '.wav')
  a.play()
  a.addEventListener('ended', function(e) {
    console.log('ended')
    $(".row").eq(visible_num).css("display", "none")
    visible_num += 1
    $(".row").eq(visible_num).css("display", "block")
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
