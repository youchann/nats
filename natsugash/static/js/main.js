let tweet_id = ''
let visible_num = 0
let visible_total = $('.display_tweet').length

// ツイートを一つずつ表示する
for (var i = 0; i < visible_total; i++) {
  $(".display_tweet").eq(i).css("display", "none")
  $(`.display_tweet:eq(${i}) .btn-audio-play`).css('display', 'none')
}
$(".display_tweet").eq(0).css("display", "block")


// 一括自動再生ボタンの押下時
$('.btn-audio-autoplay').on('click', function() {
  $('.display_tweet:eq(0) .btn-audio-play').click()
  $(this).css('display', 'none')
})

// interval function
let viewNextTweet = function() {
  $(".display_tweet").eq(visible_num).css("display", "none")
  visible_num += 1
  if (visible_num < visible_total) {
    $(".display_tweet").eq(visible_num).css("display", "block")
    $(`.display_tweet:eq(${visible_num}) .btn-audio-play`).click()
    $('.packman-wrapper').css('display', 'none')
  } else {
    $("#endaria").css("display", "block")
    $("#mogmog").css("display", "none")
  }
}

// 各ツイートにくっついてる再生ボタンの押下時
$('.btn-audio-play').on('click', function() {
  let tweet_id = $(this).attr('id')
  let a = new Audio('static/voicefiles/' + tweet_id + '.wav')
  a.play()
  a.addEventListener('ended', function(e) {
    $('.packman-wrapper').css('display', 'block')
    $('.display_tweet').eq(visible_num).addClass("animated zoomOutRight")
    setTimeout(viewNextTweet, 2000)
  })
})

// loadingの処理（雑にやってるけどとりあえずこれで）
$('.btn-to-mainpage').on('click', function() {
  $('#loading').show()
})
$(document).ready(function() {
  $('#loading').hide()
})

// topページへの遷移処理
$('#btn-top').on('click', function() {
  // location.href='http://127.0.0.1:5000'
  $("#endaria").css("display", "none")
  $("#mogmog").css("display", "block")
})
