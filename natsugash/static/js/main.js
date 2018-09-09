console.log('hello')

let tweet_id = ''

$('.btn-audio-play').on('click', function() {
  let tweet_id = $(this).attr('id')
  let a = new Audio('static/voicefiles/' + tweet_id + '.wav')
  a.play()
  a.addEventListener('ended', function(e) {
    console.log('ended')
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
