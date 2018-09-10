
$('.btn-audio-play').on('click', function() {
  let tweet_id = $(this).attr('id')
  console.log(tweet_id)
  // let substr_tweet_id = tweet_id.substr(5)
  // console.log(substr_tweet_id)
  let a = new Audio('static/voicefiles/' + tweet_id + '.wav')
  a.play()
  a.addEventListener('ended', function(e) {
    console.log('ended')
    $(`.row-wrapper #${tweet_id}`).css('display', 'none')
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
