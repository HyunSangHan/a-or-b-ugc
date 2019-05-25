$(document).ready(() => {
  $('.toggle-comments').on('click', function() {
    $(this).next().slideDown();
    $(this).hide();
  })
  $('.more-js-btn').on('click', function() {
    $(this).next().toggle();
  })
  $('.element').CopyToClipboard();

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
        content: $this.siblings('.comment-input-js').children('.comment-input').val()
      },
      dataType: 'json',
      success: function(data) {
        console.log(data);
        const str = `
<div class="toggle-comment last-comment">
  <p>${data.comment.username}: ${data.comment.content}</p>
  <form action="/feeds/${id}/comments/${data.comment.id}/" method="POST">
    <input type="hidden" name="csrfmiddlewaretoken" value=${csrfmiddlewaretoken}>
    <button class="mdl-button mdl-js-button mdl-button--icon">
      <i class="material-icons">clear</i>
    </button>
  </form>
</div>`;
        const $commentList = $this.parent().parent().siblings('.all-comments');
        $commentList.prepend(str);
        $this.siblings('.mdl-textfield__input').val('');
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