$(document).ready(() => {
  // 댓글 펼치기
  $('.toggle-comments').on('click', function(event) {
    const $this = $(this);
    $this.siblings('.all-comments').slideDown();
    $this.prev().children('.comment-heart-num-row-hide').fadeIn();
    $this.hide();
  });

  //더보기버튼
  $('.more-js-btn').on('click', function() {
    $(this).next().toggle();
  });

  //클립보드에 복사
  $('.element').CopyToClipboard();

  // 투표하기
  $('.content-a-js, .content-b-js').on('click', function(event) {
    const $this = $(this);
    const siblingA = $this.siblings('.content-a-js')
    const siblingB = $this.siblings('.content-b-js')
    const fid = $this.attr("data-feedid");
    const side = $this.attr("data-feedside");
    console.log(side + " clicked")
    $.ajax({
      url: `/feeds/${fid}/upvote_${side}`,
      type: "GET",
      dataType: "json",
      success: function (data) {
        var upvote_before = data.upvote_before;
        var upvote_after = data.upvote_after;
        var clicked = `
        <div class="content-result-bg flex-center w-100 h-100 bg-black">
        </div>
        `;
        var unclicked = `
        <div class="content-result-bg flex-center w-100 h-100 bg-grey op-7">
        </div>
        `;
        var resultA = `
        <div class="content-result flex-center w-100 h-100">
          <div class="mt-3">
            <span class="content-result-perc">`+data.perc_a+`</span>%
            <div class="w-100 mt-2" style="text-align: center;">
              ( `+data.upvote_a+` )
            </div>
          </div>
        </div>
        `;
        var resultB = `
        <div class="content-result flex-center w-100 h-100">
          <div class="mt-3">
            <span class="content-result-perc">`+data.perc_b+`</span>%
            <div class="w-100 mt-2" style="text-align: center;">
              ( `+data.upvote_b+` )
            </div>
          </div>
        </div>
        `;
        if (upvote_after === 1) {
          if (upvote_before === 0) {
            $this.prepend(resultA);
            $this.prepend(clicked);
            siblingB.children('.content-label').toggleClass('bg-black');
            siblingB.children('.content-label').toggleClass('bg-grey');
            siblingB.prepend(resultB);
            siblingB.prepend(unclicked);
          } else if (upvote_before === 1) {
            $this.children('.content-result').remove();
            $this.children('.content-result-bg').remove();
            siblingB.children('.content-label').toggleClass('bg-black');
            siblingB.children('.content-label').toggleClass('bg-grey');
            siblingB.children('.content-result').remove();
            siblingB.children('.content-result-bg').remove();
          } else if (upvote_before === 2) {
            $this.children('.content-result').remove();
            $this.children('.content-result-bg').remove();
            siblingB.children('.content-result').remove();
            siblingB.children('.content-result-bg').remove();
            $this.children('.bg-grey').addClass('bg-black');
            $this.children('.bg-grey').removeClass('bg-grey');
            $this.prepend(resultA);
            $this.prepend(clicked);
            siblingB.children('.content-label').removeClass('bg-black');
            siblingB.children('.content-label').addClass('bg-grey');
            siblingB.prepend(resultB);
            siblingB.prepend(unclicked);
          }
        } else if (upvote_after === 2) {
          if (upvote_before === 0) {
            $this.prepend(resultB);
            $this.prepend(clicked);
            siblingA.children('.content-label').toggleClass('bg-black');
            siblingA.children('.content-label').toggleClass('bg-grey');
            siblingA.prepend(resultA);
            siblingA.prepend(unclicked);
          } else if (upvote_before === 1) {
            $this.children('.content-result').remove();
            $this.children('.content-result-bg').remove();
            siblingA.children('.content-result').remove();
            siblingA.children('.content-result-bg').remove();
            $this.children('.bg-grey').addClass('bg-black');
            $this.children('.bg-grey').removeClass('bg-grey');
            $this.prepend(resultB);
            $this.prepend(clicked);
            siblingA.children('.content-label').removeClass('bg-black');
            siblingA.children('.content-label').addClass('bg-grey');
            siblingA.prepend(resultA);
            siblingA.prepend(unclicked);
          } else if (upvote_before === 2) {
            $this.children('.content-result').remove();
            $this.children('.content-result-bg').remove();
            siblingA.children('.content-label').toggleClass('bg-black');
            siblingA.children('.content-label').toggleClass('bg-grey');
            siblingA.children('.content-result').remove();
            siblingA.children('.content-result-bg').remove();
          }

        } else {
          $this.children('.content-result').remove();
          $this.children('.content-result-bg').remove();
          siblingA.children('.bg-grey').addClass('bg-black');
          siblingA.children('.bg-grey').removeClass('bg-grey');
          siblingA.children('.content-result').remove();
          siblingA.children('.content-result-bg').remove();
          siblingB.children('.bg-grey').addClass('bg-black');
          siblingB.children('.bg-grey').removeClass('bg-grey');
          siblingB.children('.content-result').remove();
          siblingB.children('.content-result-bg').remove();
      }
      },
      error: function(response, status, error) {
        window.location.href = "/accounts/login";
        alert('로그인이 필요한 서비스입니다.');
        console.log(response, status, error);
      },
      complete: function(response) {
      },
    });
  });

  // 신고하기
  $('.report-js').on('click', function(event) {
    if (confirm('정말 신고하실 건가요?')) {
      const $this = $(this);
      const fid = $this.attr("data-feedid");
      $.ajax({
        url: `/feeds/${fid}/report`,
        type: "GET",
        dataType: "json",
        success: function (data) {
          console.log(data.total_report);
          console.log(data.report_before);
          if (data.report_before === 0) {
            console.log('정상적으로 신고되었습니다.');
            $this.addClass('font-lightgrey');
          } else {
            alert('이미 신고하셨습니다.');
            console.log('이미 신고하셨습니다.');
          }
          // $this.text(data.total_report);
        },
        error: function(response, status, error) {
          alert('error');
          console.log(response, status, error);
        },
        complete: function(response) {
          console.log(response);
        },
      });
    }
  });

  // TODO:구독하기 -> 수정 필요할 가능성 존재
  $('.subscribe-js').on('click', function(event) {
    const $this = $(this);
    const creatorId = $this.attr("data-creatorid");
    const thisCreator = $('.subscribe-js[data-creatorid="'+creatorId+'"]')
    $.ajax({
      url: `/feeds/${creatorId}/follow`,
      type: "GET",
      dataType: "json",
      success: function (data) {
        thisCreator.text(data.message);
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

  // 글 삭제
  $('.delete-feed-js').on('click', function(event) {
    if (confirm('정말 삭제하실 건가요?')) {
      const $this = $(this);
      const fid = $this.attr("data-feedid");
      $.ajax({
        url: `/feeds/${fid}/delete`,
        type: "GET",
        dataType: "json",
        success: function (data) {
          console.log(data);
          $this.parent().parent().parent().parent().parent().remove();
        },
        error: function(response, status, error) {
          alert('error');
          console.log(response, status, error);
        },
        complete: function(response) {
          console.log(response);
        },
      });
    }
  });

  // 댓글 하트(좋아요)
  $(document).on('click', '.comment-heart-btn', function() {
    console.log("click heart");
    const $this = $(this);
    const $heart = $this.children('.comment-heart');
    const $heartNum = $this.parent().next().children('.comment-heart-num');
    const fid = $this.attr("data-feedid");
    const cid = $this.attr("data-commentid");

    $.ajax({
      url: `/feeds/${fid}/comments/${cid}/upvote`,
      type: "GET",
      dataType: "json",
      success: function (data) {
        btnName = data.btn_name;
        totalUpvote = data.total_upvote;
        console.log(btnName);
        console.log(totalUpvote);
        $heart.text(data.btn_name);
        $heart.toggleClass('font-red');
        $heartNum.toggleClass('font-red');
        $heartNum.toggleClass('font-grey');
        if (btnName === 'favorite' && totalUpvote === 1) {
          $heartNum.text('x' + totalUpvote);
        } else if (btnName === 'favorite_border' && totalUpvote === 0) {
          $heartNum.text('');
        } else {
          $heartNum.text('x' + totalUpvote);
        }
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

  // 댓글 삭제
  $(document).on('click', '.comment-clear', function(event) {
    if (confirm('정말 삭제하실 건가요?')) {
      const $this = $(this);
      const id = $this.data('feedid');
      const cid = $this.data('commentid');
      const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
      $.ajax({
        type: "POST",
        url: `/feeds/${id}/comments/${cid}/`,
        data: {
          csrfmiddlewaretoken: csrfmiddlewaretoken,
          id: id,
          cid: cid
        },
        dataType: "json",
        success: function (data) {
          $this.parent().next().remove();
          $this.parent().remove();
        },
        error: function(response, status, error) {
          alert('error');
          console.log(response, status, error);
        },
        complete: function(response) {
          console.log(response);
        },
      });
    }
  });


    // 댓글 달기
  $('.comment-submit-now').on('click', function(event) {
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
        var side = ``;
        if (data.comment.upvote_side === 1) {
          side = `<div class="sideicon norm"> A </div>`;
        } else if (data.comment.upvote_side === 2) {
          side = `<div class="sideicon norm"> B </div>`;
        }
        if ($('#new-comments')[0]) {
          $('#new-comments')[0].scrollIntoView();
          $('#new-comments').prepend(`
          <div class="comment w-100 v-center mtb-1 inline-flex">
          `+side+`
            <div class="font-11 v-center mtb-auto comment-reactor"><strong>${data.comment.reactor}</strong></div>
            <div class="font-14 v-center mtb-auto comment-content ellipsis-span">${data.comment.content}</div>
            <span class="comment-clear" data-feedid="${id}" data-commentid="${data.comment.id}" data-csrfmiddlewaretoken="`+csrfmiddlewaretoken+`">
              <i class="material-icons" style="font-size: 16px; color: grey;">clear</i>
            </span>
            <div class="ml-auto more-btn comment-heart-btn" data-feedid="${id}" data-commentid="${data.comment.id}">
              <i class="material-icons comment-heart v-center m-auto link-grey ml-1">favorite_border</i>
            </div>
          </div>
          <div class="comment-heart-num-row"></div>
          `);
        } else {
          const $comments = $this.parent().parent().siblings('.new-comments');
          $comments.append(`
            <div class="comment w-100 v-center mtb-1 inline-flex">
            `+side+`
              <div class="font-11 v-center mtb-auto comment-reactor"><strong>${data.comment.reactor}</strong></div>
              <div class="font-14 v-center mtb-auto comment-content ellipsis-span">${data.comment.content}</div>
              <span class="comment-clear" data-feedid="${id}" data-commentid="${data.comment.id}" data-csrfmiddlewaretoken="`+csrfmiddlewaretoken+`">
                <i class="material-icons" style="font-size: 16px; color: grey;">clear</i>
              </span>
              <div class="ml-auto more-btn comment-heart-btn" data-feedid="${id}" data-commentid="${data.comment.id}">
                <i class="material-icons comment-heart v-center m-auto link-grey ml-1">favorite_border</i>
              </div>
            </div>
          `);
        }
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

  //검색 버튼 나오기
  $('.mdl-textfield__input').on('input',
    function(event) {
      const $this = $(this);
      if ($this.val().length !== 0) {
        $this.siblings('.search-btn').removeClass('invisible');
        }
      else {
        $this.siblings('.search-btn').addClass('invisible');
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
    const eachContent = $this.parent();
    if(window.FileReader && $this[0].files[0]){
      eachContent.children('.uploaded-a').remove();
      var reader = new FileReader();
      reader.onload = function(e) {
        img_a = e.target.result;
        eachContent.prepend(`
          <div class="mr-1perc demo-card-image mdl-card content-img inner uploaded-a" style="background: url('`+img_a+`') center / cover;">
            <label for="img_a" style="height: 100%; width: 100%;">
              <div class="content-label bg-black">
                <strong>A / </strong>
                <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content_a" value="`+content_a+`" placeholder=" 내용(21자 이내)" name="content_a" maxlength="21" required>
              </div>
            </label>
          </div>
        `); 
      }
      reader.readAsDataURL($this[0].files[0]);
    } else {
      console.log('cancel editing the photo A');
    }
  });

  //for img B
  var img_b, content_b;
  $('.upload-b').on('change', function() {
    const $this = $(this)
    if(window.FileReader && $this[0].files[0]){
      content_b = document.getElementsByClassName('content_b')[0].value;
    }
    const eachContent = $this.parent();
    if(window.FileReader && $this[0].files[0]){
      eachContent.children('.uploaded-b').remove();
      var reader = new FileReader();
      reader.onload = function(e) {
        img_b = e.target.result;
        eachContent.append(`
          <div class="ml-1perc demo-card-image mdl-card content-img inner uploaded-b" style="background: url('`+img_b+`') center / cover;">
            <label for="img_b" style="height: 100%; width: 100%;">
              <div class="content-label bg-black">
                <strong>B / </strong>
                <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content_b" value="`+content_b+`" placeholder=" 내용(21자 이내)" name="content_b" maxlength="21" required>
              </div>
            </label>
          </div>
        `); 
      }
      reader.readAsDataURL($this[0].files[0]);
    } else {
      console.log('cancel editing the photo B');
      }
  });


  // 이미지검색
  $(document).on('click', '.img-srch-btn', function() {
    const $this = $(this);
    const $eachResult = $this.siblings('.each-srch-result-wrap').children('.img-srch-result-js')
    const keyword = $('.content_b').val();
    const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');

    console.log("keyword: "+ keyword);
    if (keyword !== "") {
      $.ajax({
        type: 'POST',
        url: `/feeds/new/image_search/`,
        data: {
          csrfmiddlewaretoken: csrfmiddlewaretoken,
          keyword: keyword
        },
        dataType: 'json',
        success: function(data) {
          console.log(data);
          $eachResult.children('.each-search-result-js').remove();
          for (var i=0; i<40; i++) {
            if (data.result.items[i].sizeheight / data.result.items[i].sizewidth > 0.75) {
              thb = data.result.items[i].thumbnail.replace('&type=b150','');
              $eachResult.append(`
                <img src=`+thb+` alt="image_search" class="each-srch-result each-search-result-js">
              `)
            }
          };

        },
        error: function(response, status,  error) {
          console.log(response, status, error);
        }
      });
    } else {
      console.log("there is no keyword");
    }
  });

    // 이미지클릭 시(test ver.)
  $(document).on('click', '.each-search-result-js', function() {
    const $this = $(this);
    const eachContent = $this.parent().parent().siblings('.each-content');
    var img = $this.attr('src');
    content_b = document.getElementsByClassName('content_b')[0].value;
    eachContent.children('.uploaded-b').remove();
    eachContent.append(`
        <div class="ml-1perc demo-card-image mdl-card content-img inner uploaded-b" style="background: url('`+img+`') center / cover;">
          <label for="img_b" style="height: 100%; width: 100%;">
            <div class="content-label bg-black">
              <strong>B / </strong>
              <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content_b" value="`+content_b+`" placeholder=" 내용(21자 이내)" name="content_b" maxlength="21" required>
            </div>
          </label>
        </div>
      `); 
  });


})