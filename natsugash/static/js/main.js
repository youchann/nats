$('#submit-btn').on('click', function(e) {
  if ($('#tweetListForm input:checkbox:checked').length == 0) {
    alert('ツイートを選択してください！')
    return false
  } else {
    $('#tweetListForm').submit()
  }
})
