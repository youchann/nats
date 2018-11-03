let tweet_id = ''
let visible_num = 0
let visible_total = $('.display_tweet').length

// loadingの処理（雑にやってるけどとりあえずこれで）
$('.btn-to-mainpage').on('click', function() {
  $('#loading').show()
})
$(document).ready(function() {
  $('#loading').hide()
})

// topページへの遷移処理
$('#btn-top').on('click', function() {
  $("#endaria").css("display", "none")
  $("#mogmog").css("display", "block")
})
