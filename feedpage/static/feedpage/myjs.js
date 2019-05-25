$(document).ready(() => {
  // 댓글 펼치기
  $('.toggle-comments').on('click', function(event) {
    $(this).siblings('.all-comments').slideDown();
    $(this).hide();
  });

  //더보기버튼
  $('.more-js-btn').on('click', function() {
    $(this).next().toggle();
  })

  //클립보드에 복사
  $('.element').CopyToClipboard();

  // 댓글 달기 구현
  $('.comment-submit').on('click', function(event) {
    event.preventDefault();

    const $this = $(this);
    const id = $this.data('feedid');
    const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');

    $.ajax({
      type: 'POST',
      url: `/feeds/${id}/comments/`, // 앞 뒤 슬래시 꼭
      data: {
        csrfmiddlewaretoken: csrfmiddlewaretoken,
        id: id,
        content: $this.siblings('.comment-input-wrap').children('.comment-input').val()
      },
      dataType: 'json',
      success: function(data) {
        console.log(data);
        const str = `
<div>
  <div class="comment w-100 v-center mtb-1 inline-flex">
    <div class="sideicon norm"> ${data.comment.upvote_side} </div>
    <div class="font-11 v-center mtb-auto comment-reactor"><strong>${data.comment.reactor}</strong></div>
    <div class="font-14 v-center mtb-auto comment-content ellipsis">${data.comment.content}</div>
    <div class="ml-auto more-btn">
      <a href="/feeds/${id}/comments/${data.comment.id}/upvote">
        <i class="material-icons comment-heart v-center m-auto link-grey ml-1">favorite_border</i>
      </a>
    </div>
  </div>
</div>`;
        const $comments = $this.parent().siblings('.comment-wrap');
        $comments.append(str);
        $this.siblings('.comment-input-wrap').children('.comment-input').val('');
      },
      error: function(response, status, error) {
        alert('error');
        console.log(response, status, error);
      },
      complete: function(response) {
        console.log(response);
      },
    });
  });
})