$(document).ready(() => {
  // 댓글 펼치기
  $('.toggle-comments').on('click', function(event) {
    const $this = $(this);
    $this.siblings('.all-comments').slideDown();
    $this.hide();
  });

  //더보기버튼
  $('.more-js-btn').on('click', function() {
    $(this).next().toggle();
  });

  //클립보드에 복사
  $('.element').CopyToClipboard();

  // // 댓글 하트 테두리버튼
  // $('.comment-heart-btn-on').on('click', function(event) {
  //   event.preventDefault();
  //   const $this = $(this);
  //   $this.hide();
  //   $this.siblings('.comment-heart-btn-off').show();
  // });

  // // 댓글 하트 빨강버튼
  // $('.comment-heart-btn-off').on('click', function(event) {
  //   event.preventDefault();
  //   const $this = $(this);
  //   $this.hide();
  //   $this.siblings('.comment-heart-btn-on').show();
  // });
  

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
        content: $this.siblings('.comment-input').val()
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
        const $comments = $this.parent().parent().siblings('.comment-wrap');
        $comments.append(str);
        $this.siblings('.comment-input').val('');
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

  //댓글달기 버튼 나오기
  $('.comment-input').on('input',
    function(event) {
      const $this = $(this);
      if ($this.val().length !== 0) {
        $this.siblings('.comment-submit').removeClass('invisible');
        }
      else {
        $this.siblings('.comment-submit').addClass('invisible');
      }
  });


  //인풋 너비 다르게 하기 코드
  // $('.feed-input-border').on('keydown',
  //   function(event){
  //     // $this = 
  //     var value = $('.feed-input-border').val();
  //     $(body).append('<div id="virtual_dom">' + value + '</div>'); 
  //       var inputWidth = $('#virtual_dom').width() + 10;
  //       $('.feed-input-border').css('width', inputWidth); 
  //       $('#virtual_dom').remove();
  // });

  // var imgTarget = $('.preview-image .upload-hidden'); imgTarget.on('change', function(){ var parent = $(this).parent(); parent.children('.upload-display').remove(); if(window.FileReader){ if (!$(this)[0].files[0].type.match(/image\//)) return; var reader = new FileReader(); reader.onload = function(e){ var src = e.target.result; parent.prepend('<div class="upload-display"><div class="upload-thumb-wrap"><img src="'+src+'" class="upload-thumb"></div></div>'); } reader.readAsDataURL($(this)[0].files[0]); } else { $(this)[0].select(); $(this)[0].blur(); var imgSrc = document.selection.createRange().text; parent.prepend('<div class="upload-display"><div class="upload-thumb-wrap"><img class="upload-thumb"></div></div>'); var img = $(this).siblings('.upload-display').find('img'); img[0].style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(enable='true',sizingMethod='scale',src=\""+imgSrc+"\")"; } });

})