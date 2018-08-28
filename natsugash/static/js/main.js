console.log('hello')

$('.btn-audio-play').on('click', function() {
  let tweet_id = $(this).attr('id')
  console.log('click !', tweet_id)
  $('#audio' + tweet_id)[0].play()
})

$('.btn-to-mainpage').on('click', function() {
  console.log('抽出開始')
})
