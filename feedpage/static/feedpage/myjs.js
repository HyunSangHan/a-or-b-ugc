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

  // 댓글 하트
  $('.comment-heart-btn').on('click', function(event) {
    const $this = $(this);
    const fid = $this.attr("data-feedid");
    const cid = $this.attr("data-commentid");

    $.ajax({
      url: `/feeds/${fid}/comments/${cid}/upvote`,
      type: "GET",
      dataType: "json",
      success: function (data) {
        console.log(data);
        $this.children('.comment-heart').text(data.btn_name);
        $this.children('.comment-heart').toggleClass('font-red');
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

    // 댓글 달기
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


  //for img A
  var img_a, content_a;
  $('.upload-a').on('change', function() {
    const $this = $(this)
    if(window.FileReader && $this[0].files[0]){
      content_a = document.getElementsByClassName('content_a')[0].value;
    }
    var eachContent = $this.parent().parent().children('.each-content');
    eachContent.children('.uploaded-a').remove();
    if(window.FileReader && $this[0].files[0]){
      // if () {  
        var reader = new FileReader();
        reader.onload = function(e) {
          img_a = e.target.result;
          eachContent.prepend(`
            <div class="mr-1perc demo-card-image mdl-card content-img inner uploaded-a" style="background: url('`+img_a+`') center / cover;">
              <div class="content-label bg-black">
                <strong>A / </strong>
                <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content_a" value="`+content_a+`" placeholder=" 내용(21자 이내)" name="content_a" maxlength="21" required>
              </div>
            </div>
          `); 
        // }
      }
      reader.readAsDataURL($this[0].files[0]);
    } else {
      console.log('cancel editing the photo A');
      // $(this)[0].select();
      // $(this)[0].blur();
      eachContent.prepend(`
        <div class="mr-1perc demo-card-image mdl-card content-img inner uploaded-a" style="background: url('`+img_a+`') center / cover;">
          <div class="content-label bg-black">
            <strong>A / </strong>
            <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content_a" value="`+content_a+`" placeholder=" 내용(21자 이내)" name="content_a" maxlength="21" required>
          </div>
        </div>
      `);
      // var img = $(this).siblings('.upload-display').find('img');
      // img[0].style.filter = "progid:DXImageTransform.Microsoft.AlphaImageLoader(enable='true',sizingMethod='scale',src=\""+imgSrc+"\")";
    }
  });

  //for img B
  var img_b, content_b;
  $('.upload-b').on('change', function() {
    const $this = $(this)
    if(window.FileReader && $this[0].files[0]){
      content_b = document.getElementsByClassName('content_b')[0].value;
    }
    var eachContent = $this.parent().parent().children('.each-content');
    eachContent.children('.uploaded-b').remove();
    if(window.FileReader && $this[0].files[0]){
      // if () {  
        var reader = new FileReader();
        reader.onload = function(e) {
          img_b = e.target.result;
          eachContent.append(`
            <div class="ml-1perc demo-card-image mdl-card content-img inner uploaded-b" style="background: url('`+img_b+`') center / cover;">
              <div class="content-label bg-black">
                <strong>B / </strong>
                <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content_b" value="`+content_b+`" placeholder=" 내용(21자 이내)" name="content_b" maxlength="21" required>
              </div>
            </div>
          `); 
        // }
      }
      reader.readAsDataURL($this[0].files[0]);
    } else {
      console.log('cancel editing the photo B');
      eachContent.append(`
        <div class="ml-1perc demo-card-image mdl-card content-img inner uploaded-b" style="background: url('`+img_b+`') center / cover;">
          <div class="content-label bg-black">
            <strong>B / </strong>
            <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content_b" value="`+content_b+`" placeholder=" 내용(21자 이내)" name="content_b" maxlength="21" required>
          </div>
        </div>
        `); 
      }
  });

})