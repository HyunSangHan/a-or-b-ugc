$(document).ready(() => {
  $(document).on("click", "#call_more_feeds", function() {
    const page = $("#page").val();
    callMoreFeedsAjax(page);
    $("#page").val(parseInt(page) + 1);
  });

  //scroll event
  window.addEventListener("scroll", function(e) {
    last_known_scroll_position = window.scrollY;
    console.log(last_known_scroll_position);
  });

  // $(window).scroll(function() {
  //   const scrollHeight = $(window).scrollTop() + $(window).height();
  //   console.log(scrollHeight);
  //   const documentHeight = $(document).height();
  //   console.log(documentHeight);

  //   if (scrollHeight + 300 >= documentHeight) {
  //     const page = $("#page").val();
  //     callMoreFeedsAjax(page);
  //     $("#page").val(parseInt(page) + 1);
  //   }
  // });

  function callMoreFeedsAjax(page) {
    $.ajax({
      url: `/feeds/ajax`,
      type: "GET",
      data: {
        page: page
      },
      success: addMoreFeedsByAjax,
      dataType: "html"
    });
  }

  function addMoreFeedsByAjax(data) {
    $("#feed_list_ajax").append(data);
    console.log("Loaded done");
  }

  // 댓글 펼치기
  $(document).on("click", ".toggle-comments", function() {
    const $this = $(this);
    $this.siblings(".all-comments").slideDown();
    $this
      .prev()
      .children(".comment")
      .children(".comment-heart-btn")
      .children(".comment-heart-num-hide")
      .fadeIn();
    $this.hide();
  });

  //더보기버튼
  $(document).on("click", ".more-js-btn", function() {
    $(this)
      .next()
      .toggle();
  });

  // 투표하기
  $(document).on("click", ".content-a-js, .content-b-js", function(event) {
    const $this = $(this);
    const $siblingA = $this.siblings(".content-a-js");
    const $siblingB = $this.siblings(".content-b-js");
    const fid = $this.data("feedid");
    const side = $this.data("feedside");
    const beforeSide = $this.parent().data("beforeside");
    const beforeNumA = Number(
      $this
        .parent()
        .children(".content-a-js")
        .data("num-a")
    );
    const beforeNumB = Number(
      $this
        .parent()
        .children(".content-b-js")
        .data("num-b")
    );
    let afterNumA, afterNumB, afterPerA, afterPerB;
    let afterTotalNum = beforeNumA + beforeNumB;
    const csrfthoken = $this
      .parent()
      .siblings(".csrf-js")
      .data("csrfmiddlewaretoken");
    const userIsAuthenticated = csrfthoken != undefined;

    $siblingA.children(".content-default-bg-js").addClass("content-default-bg");
    $siblingB.children(".content-default-bg-js").addClass("content-default-bg");
    $siblingA.children(".content-result").remove();
    $siblingB.children(".content-result").remove();
    $siblingA.children(".content-result-bg").remove();
    $siblingB.children(".content-result-bg").remove();

    const $clicked = `
    <div class="content-result-bg flex-center w-100 h-100 bg-black">
    </div>
    `;
    const $unclicked = `
    <div class="content-result-bg flex-center w-100 h-100 bg-grey op-7">
    </div>
    `;
    if (side == "A") {
      if (beforeSide == "A") {
        afterNumA = Number(beforeNumA) - 1;
        afterNumB = Number(beforeNumB);
        $this.data("num-a", beforeNumA - 1);
      } else if (beforeSide == "B") {
        afterNumA = Number(beforeNumA) + 1;
        afterNumB = Number(beforeNumB) - 1;
        $this.data("num-a", beforeNumA + 1);
        $siblingB.data("num-b", beforeNumB - 1);
      } else {
        afterNumA = Number(beforeNumA) + 1;
        afterNumB = Number(beforeNumB);
        $this.data("num-a", beforeNumA + 1);
        afterTotalNum += 1;
      }
    } else if (side == "B") {
      if (beforeSide == "A") {
        afterNumA = Number(beforeNumA) - 1;
        afterNumB = Number(beforeNumB) + 1;
        $siblingA.data("num-a", beforeNumA - 1);
        $this.data("num-b", beforeNumB + 1);
      } else if (beforeSide == "B") {
        afterNumA = Number(beforeNumA);
        afterNumB = Number(beforeNumB) - 1;
        $this.data("num-b", beforeNumB - 1);
      } else {
        afterNumA = Number(beforeNumA);
        afterNumB = Number(beforeNumB) + 1;
        $this.data("num-b", beforeNumB + 1);
        afterTotalNum += 1;
      }
    }
    afterPerA = ((afterNumA / afterTotalNum) * 100).toFixed(0);
    afterPerB = ((afterNumB / afterTotalNum) * 100).toFixed(0);
    const $resultA =
      `
    <div class="content-result flex-center w-100 h-100">
      <div class="mt-3">
        <span class="content-result-perc">` +
      afterPerA +
      `</span>%
        <div class="w-100 mt-2" style="text-align: center;">
          ( ` +
      afterNumA +
      ` )
        </div>
      </div>
    </div>
    `;
    const $resultB =
      `
    <div class="content-result flex-center w-100 h-100">
      <div class="mt-3">
        <span class="content-result-perc">` +
      afterPerB +
      `</span>%
        <div class="w-100 mt-2" style="text-align: center;">
          ( ` +
      afterNumB +
      ` )
        </div>
      </div>
    </div>
    `;

    if (userIsAuthenticated) {
      // frontend 먼저 반영하는 코드 (성능 이슈 해결을 위해)
      $siblingA.children(".bg-grey").addClass("bg-black");
      $siblingB.children(".bg-grey").addClass("bg-black");
      $siblingA.children(".bg-grey").removeClass("bg-grey");
      $siblingB.children(".bg-grey").removeClass("bg-grey");
      if (side === "A") {
        if (beforeSide === "") {
          $this.parent().data("beforeside", "A");
          $this
            .children(".content-default-bg-js")
            .removeClass("content-default-bg");
          $siblingB
            .children(".content-default-bg-js")
            .removeClass("content-default-bg");
          $this.prepend($resultA);
          $this.prepend($clicked);
          $siblingB.children(".content-label").toggleClass("bg-black");
          $siblingB.children(".content-label").toggleClass("bg-grey");
          $siblingB.prepend($resultB);
          $siblingB.prepend($unclicked);
        } else if (beforeSide === "A") {
          $this.parent().data("beforeside", "");
          $this
            .children(".content-default-bg-js")
            .addClass("content-default-bg");
          $siblingB
            .children(".content-default-bg-js")
            .addClass("content-default-bg");
          $this.children(".content-result").remove();
          $this.children(".content-result-bg").remove();
          $siblingB.children(".content-result").remove();
          $siblingB.children(".content-result-bg").remove();
        } else if (beforeSide === "B") {
          $this.parent().data("beforeside", "A");
          $this.children(".content-result").remove();
          $this.children(".content-result-bg").remove();
          $siblingB.children(".content-result").remove();
          $siblingB.children(".content-result-bg").remove();
          $this.children(".bg-grey").addClass("bg-black");
          $this.children(".bg-grey").removeClass("bg-grey");
          $this.prepend($resultA);
          $this.prepend($clicked);
          $siblingB.children(".content-label").removeClass("bg-black");
          $siblingB.children(".content-label").addClass("bg-grey");
          $siblingB.prepend($resultB);
          $siblingB.prepend($unclicked);
        }
      } else if (side === "B") {
        if (beforeSide === "") {
          $this.parent().data("beforeside", "B");
          $siblingA
            .children(".content-default-bg-js")
            .removeClass("content-default-bg");
          $this
            .children(".content-default-bg-js")
            .removeClass("content-default-bg");
          $this.prepend($resultB);
          $this.prepend($clicked);
          $siblingA.children(".content-label").toggleClass("bg-black");
          $siblingA.children(".content-label").toggleClass("bg-grey");
          $siblingA.prepend($resultA);
          $siblingA.prepend($unclicked);
        } else if (beforeSide === "A") {
          $this.parent().data("beforeside", "B");
          $this.children(".content-result").remove();
          $this.children(".content-result-bg").remove();
          $siblingA.children(".content-result").remove();
          $siblingA.children(".content-result-bg").remove();
          $this.children(".bg-grey").addClass("bg-black");
          $this.children(".bg-grey").removeClass("bg-grey");
          $this.prepend($resultB);
          $this.prepend($clicked);
          $siblingA.children(".content-label").removeClass("bg-black");
          $siblingA.children(".content-label").addClass("bg-grey");
          $siblingA.prepend($resultA);
          $siblingA.prepend($unclicked);
        } else if (beforeSide === "B") {
          $this.parent().data("beforeside", "");
          $siblingA
            .children(".content-default-bg-js")
            .addClass("content-default-bg");
          $this
            .children(".content-default-bg-js")
            .addClass("content-default-bg");
          $this.children(".content-result").remove();
          $this.children(".content-result-bg").remove();
          $siblingA.children(".content-result").remove();
          $siblingA.children(".content-result-bg").remove();
        }
      }
      // backend 실제 반영하는 코드
      $.ajax({
        url: `/feeds/${fid}/upvote_${side}`,
        type: "GET",
        dataType: "json",
        success: function(data) {
          console.log(beforeSide + " => " + side);
        },
        error: function(response, status, error) {
          console.log(response, status, error);
          console.log("error!!!");
          window.location.reload();
        },
        complete: function(response) {}
      });
    } else {
      alert("로그인이 필요한 서비스입니다.");
      window.location.href = "/accounts/login";
    }
  });

  // 신고하기
  $(document).on("click", ".report-js", function(event) {
    if (confirm("정말 신고하실 건가요?")) {
      const $this = $(this);
      const fid = $this.attr("data-feedid");
      $.ajax({
        url: `/feeds/${fid}/report`,
        type: "GET",
        dataType: "json",
        success: function(data) {
          console.log(data.total_report);
          console.log(data.report_before);
          if (data.report_before === 0) {
            console.log("정상적으로 신고되었습니다.");
            $this.addClass("font-lightgrey");
          } else {
            alert("이미 신고하셨습니다.");
            console.log("이미 신고하셨습니다.");
          }
          // $this.text(data.total_report);
        },
        error: function(response, status, error) {
          alert("error");
          console.log(response, status, error);
        },
        complete: function(response) {
          console.log(response);
        }
      });
    }
  });

  // TODO:구독하기 -> 수정 필요할 가능성 존재
  $(document).on("click", ".subscribe-js", function(event) {
    const $this = $(this);
    const creatorId = $this.attr("data-creatorid");
    const thisCreator = $('.subscribe-js[data-creatorid="' + creatorId + '"]');
    $.ajax({
      url: `/feeds/${creatorId}/follow`,
      type: "GET",
      dataType: "json",
      success: function(data) {
        thisCreator.text(data.message);
      },
      error: function(response, status, error) {
        alert("error");
        console.log(response, status, error);
      },
      complete: function(response) {
        console.log(response);
      }
    });
  });

  // 글 삭제
  $(document).on("click", ".delete-feed-js", function(event) {
    if (confirm("정말 삭제하실 건가요?")) {
      const $this = $(this);
      const fid = $this.attr("data-feedid");
      $.ajax({
        url: `/feeds/${fid}/delete`,
        type: "GET",
        dataType: "json",
        success: function(data) {
          console.log(data);
          $this
            .parent()
            .parent()
            .parent()
            .parent()
            .parent()
            .remove();
        },
        error: function(response, status, error) {
          alert("error");
          console.log(response, status, error);
        },
        complete: function(response) {
          console.log(response);
        }
      });
    }
  });

  // 댓글 하트(좋아요)
  $(document).on("click", ".comment-heart-btn", function() {
    console.log("click heart");
    const $this = $(this);
    const $heart = $this.children(".comment-heart");
    const $heartNum = $this.children(".comment-heart-num");
    const fid = $this.attr("data-feedid");
    const cid = $this.attr("data-commentid");

    $.ajax({
      url: `/feeds/${fid}/comments/${cid}/upvote`,
      type: "GET",
      dataType: "json",
      success: function(data) {
        const btnName = data.btn_name;
        const totalUpvote = data.total_upvote;
        console.log(btnName);
        console.log(totalUpvote);
        $heart.text(data.btn_name);
        $heart.toggleClass("font-red");
        $heartNum.toggleClass("font-red");
        $heartNum.toggleClass("font-grey");
        $heartNum.toggleClass("font-midlight");
        if (btnName === "favorite" && totalUpvote === 1) {
          $heartNum.text(totalUpvote + "x");
        } else if (btnName === "favorite_border" && totalUpvote === 0) {
          $heartNum.text("");
        } else {
          $heartNum.text(totalUpvote + "x");
        }
      },
      error: function(response, status, error) {
        alert("error");
        console.log(response, status, error);
      },
      complete: function(response) {
        console.log(response);
      }
    });
  });

  // 댓글 삭제
  $(document).on("click", ".comment-clear", function(event) {
    if (confirm("정말 삭제하실 건가요?")) {
      const $this = $(this);
      const id = $this.data("feedid");
      const cid = $this.data("commentid");
      const csrfmiddlewaretoken = $this.data("csrfmiddlewaretoken");
      $.ajax({
        type: "POST",
        url: `/feeds/${id}/comments/${cid}/`,
        data: {
          csrfmiddlewaretoken: csrfmiddlewaretoken,
          id: id,
          cid: cid
        },
        dataType: "json",
        success: function(data) {
          // $this.parent().next().remove();
          $this
            .parent()
            .parent()
            .remove();
        },
        error: function(response, status, error) {
          alert("error");
          console.log(response, status, error);
        },
        complete: function(response) {
          console.log(response);
        }
      });
    }
  });

  // 댓글 달기
  $(document).on("click", ".comment-submit-now", function(event) {
    event.preventDefault();

    const $this = $(this);
    const id = $this.data("feedid");
    const csrfmiddlewaretoken = $this.data("csrfmiddlewaretoken");
    const content = $this.siblings(".comment-input").val();

    if (content != "") {
      $.ajax({
        type: "POST",
        url: `/feeds/${id}/comments/`, // 앞 뒤 슬래시 꼭
        data: {
          csrfmiddlewaretoken: csrfmiddlewaretoken,
          id: id,
          content: content
        },
        dataType: "json",
        success: function(data) {
          let side = ``;
          if (data.comment.upvote_side === 1) {
            side = `<div class="sideicon norm"> A </div>`;
          } else if (data.comment.upvote_side === 2) {
            side = `<div class="sideicon norm"> B </div>`;
          }
          //show 페이지에서 댓글을 달았을 경우
          if ($("#new-comments")[0]) {
            $("#new-comments-next")[0].scrollIntoView(true);
            $("#new-comments").append(
              `
              <div class="comment norm w-100 v-center mtb-1 inline-flex">
                <div class="comment-width">
                  ` +
                side +
                `
                  <span class="font-11 v-center mtb-auto comment-reactor">
                    <strong>${data.comment.reactor}</strong>
                  </span>
                  <span class="font-14 v-center mtb-auto comment-content">
                    ${data.comment.content}
                  </span>
                  <span class="comment-clear" data-feedid="${id}" data-commentid="${data.comment.id}" data-csrfmiddlewaretoken="` +
                csrfmiddlewaretoken +
                `">
                    <i class="material-icons" style="font-size: 13px; color: grey; transform: translateY(4px);">clear</i>
                  </span>
                </div>
                <div style="width: 20px;" class="ml-auto comment-heart-btn" data-feedid="${id}" data-commentid="${data.comment.id}">
                  <i class="material-icons comment-heart v-center m-auto link-grey ml-1">favorite_border</i>
                  <div class="font-grey comment-heart-num">
                  </div>
                </div>
              </div>
            `
            );
          } else {
            //index등 show '외'의 페이지에서 댓글을 달았을 경우
            const $comments = $this
              .parent()
              .parent()
              .siblings(".new-comments");
            $comments.append(
              `
            <div class="comment norm w-100 v-center mtb-1 inline-flex">
              <div class="comment-width">
                ` +
                side +
                `
                <span class="font-11 v-center mtb-auto comment-reactor" style="margin-left: 0;">
                  <strong>${data.comment.reactor}</strong>
                </span>
                <span class="font-14 v-center mtb-auto comment-content">
                  ${data.comment.content}
                </span>
                <span class="comment-clear" data-feedid="${id}" data-commentid="${data.comment.id}" data-csrfmiddlewaretoken="` +
                csrfmiddlewaretoken +
                `">
                  <i class="material-icons" style="font-size: 13px; color: grey; transform: translateY(4px);">clear</i>
                </span>
              </div>
              <div style="width: 20px;" class="ml-auto comment-heart-btn" data-feedid="${id}" data-commentid="${data.comment.id}">
                <i class="material-icons comment-heart v-center m-auto link-grey ml-1">favorite_border</i>
                <div class="font-grey comment-heart-num">
                </div>
              </div>
            </div>
            `
            );
          }
          $this.siblings(".comment-input").val("");
        },
        error: function(response, status, error) {
          console.log(response, status, error);
          alert("error");
          window.location.reload();
        },
        complete: function(response) {
          console.log(response);
        }
      });
    }
  });

  //댓글달기 버튼 나오기
  $(document).on("input", ".comment-input", function(event) {
    const $this = $(this);
    if ($this.val().length !== 0) {
      $this.siblings(".comment-submit").removeClass("invisible");
    } else {
      $this.siblings(".comment-submit").addClass("invisible");
    }
  });

  //검색 버튼 나오기
  $(document).on("input", ".mdl-textfield__input", function(event) {
    const $this = $(this);
    if ($this.val().length !== 0) {
      $this.siblings(".search-btn").removeClass("invisible");
    } else {
      $this.siblings(".search-btn").addClass("invisible");
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

  //for uploading img A
  let prevFileA;
  $(".upload-a").on("change", function() {
    const $this = $(this);
    const $imgMenuOn = $this.siblings(".uploaded-a").children(".img-menu-on");
    const csrfmiddlewaretoken = $imgMenuOn.data("csrfmiddlewaretoken");
    const aorb = $imgMenuOn.data("aorb");
    let content_a;
    if (window.FileReader && $this[0].files[0]) {
      content_a = document.getElementsByClassName("content-a")[0].value;
    }
    const $eachContent = $this.parent();
    if (window.FileReader && $this[0].files[0]) {
      $eachContent.children(".uploaded-a").remove();
      let reader = new FileReader();
      reader.onload = function(e) {
        const img_a = e.target.result;
        $eachContent.prepend(
          `
          <div class="mr-1perc demo-card-image mdl-card content-img inner uploaded-a" style="background: url('` +
            img_a +
            `') center / cover;">
            <div class="content-label bg-black">
              <strong>A / </strong>
              <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content-a content-js" value="` +
            content_a +
            `" placeholder=" 내용(21자 이내)" name="content_a" maxlength="21" autocomplete="off" required>
            </div>
            <div class="w-100 h-100 img-menu-on" data-csrfmiddlewaretoken="` +
            csrfmiddlewaretoken +
            `" data-aorb="` +
            aorb +
            `">
            </div>
          </div>
        `
        );
      };
      reader.readAsDataURL($this[0].files[0]);
      prevFileA = $this[0].files;
    } else {
      $this[0].files = prevFileA;
      console.log("cancel editing the photo A");
    }
  });

  //for img B
  let prevFileB;
  $(".upload-b").on("change", function() {
    const $this = $(this);
    const $imgMenuOn = $this.siblings(".uploaded-b").children(".img-menu-on");
    const csrfmiddlewaretoken = $imgMenuOn.data("csrfmiddlewaretoken");
    const aorb = $imgMenuOn.data("aorb");
    let content_b;
    if (window.FileReader && $this[0].files[0]) {
      content_b = document.getElementsByClassName("content-b")[0].value;
    }
    const $eachContent = $this.parent();
    if (window.FileReader && $this[0].files[0]) {
      $eachContent.children(".uploaded-b").remove();
      let reader = new FileReader();
      reader.onload = function(e) {
        const img_b = e.target.result;
        $eachContent.append(
          `
          <div class="ml-1perc demo-card-image mdl-card content-img inner uploaded-b" style="background: url('` +
            img_b +
            `') center / cover;">
            <div class="content-label bg-black">
              <strong>B / </strong>
              <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content-b content-js" value="` +
            content_b +
            `" placeholder=" 내용(21자 이내)" name="content_b" maxlength="21" autocomplete="off" required>
            </div>
            <div class="w-100 h-100 img-menu-on" data-csrfmiddlewaretoken="` +
            csrfmiddlewaretoken +
            `" data-aorb="` +
            aorb +
            `">
            </div>
          </div>
        `
        );
      };
      reader.readAsDataURL($this[0].files[0]);
      prevFileB = $this[0].files;
    } else {
      $this[0].files = prevFileB;
      console.log("cancel editing the photo B");
    }
  });

  //직접업로드 vs 이미지추천 고르는 메뉴 띄우기
  $(document).on("click", ".img-menu-on", function() {
    const $this = $(this);
    const csrfmiddlewaretoken = $this.data("csrfmiddlewaretoken");
    const aorb = $this.data("aorb");

    $this.before(
      `
      <div class="content-img-input-bg w-100 h-100 bg-black font-15">
        <label class="content-img-input-msg-upper font-white flex-center" for="img-` +
        aorb +
        `">
          직접 업로드
        </label>
        <div class="content-img-input-msg-lower font-white flex-center img-srch-btn" data-csrfmiddlewaretoken="` +
        csrfmiddlewaretoken +
        `">
          이미지 추천
        </div>
      </div>
    `
    );
  });

  // 이미지추천
  $(document).on("click", ".img-srch-btn", function() {
    const $this = $(this);
    const $eachResult = $this
      .parent()
      .parent()
      .parent()
      .siblings(".each-srch-result-wrap")
      .children(".img-srch-result-js");
    const keyword = $this
      .parent()
      .siblings(".content-label")
      .children(".content-js")
      .val();
    const csrfmiddlewaretoken = $this.data("csrfmiddlewaretoken");
    if (keyword !== "") {
      $.ajax({
        type: "POST",
        url: `/feeds/new/image_search/`,
        data: {
          csrfmiddlewaretoken: csrfmiddlewaretoken,
          keyword: keyword
        },
        dataType: "json",
        success: function(data) {
          $eachResult.children(".each-srch-result-js").remove();
          const aorb = $this
            .parent()
            .siblings(".img-menu-on")
            .data("aorb");
          console.log("keyword: " + keyword + "(for " + aorb + ")");
          console.log(data);
          for (let i = 0; i < 40; i++) {
            if (
              data.result.items[i].sizeheight / data.result.items[i].sizewidth >
              0.75
            ) {
              thb = data.result.items[i].thumbnail.replace("&type=b150", "");
              $eachResult.append(
                `
                <img src=` +
                  thb +
                  ` alt="image_search" class="each-srch-result each-srch-result-js" data-csrfmiddlewaretoken="` +
                  csrfmiddlewaretoken +
                  `" data-aorb="` +
                  aorb +
                  `">
              `
              );
            }
          }
          $("img").on("error", function() {
            $(this).hide();
            console.log($(this));
          });
          $this.parent().hide();
        },
        error: function(response, status, error) {
          console.log(response, status, error);
        }
      });
    } else {
      console.log("there is no keyword");
      alert("이미지 라벨링을 채워주셔야 이미지추천이 가능합니다.");
    }
  });

  // 이미지클릭 시 씌워지기
  $(document).on("click", ".each-srch-result-js", function() {
    const $this = $(this);
    const $eachContent = $this
      .parent()
      .parent()
      .siblings(".each-content");
    const csrfmiddlewaretoken = $this.data("csrfmiddlewaretoken");
    const aorb = $this.data("aorb");
    const img = $this.attr("src");

    if (aorb === "a") {
      content_a = document.getElementsByClassName("content-a")[0].value;
      $eachContent.children(".uploaded-a").remove();
      $eachContent.prepend(
        `
        <div class="mr-1perc demo-card-image mdl-card content-img inner uploaded-a" style="background: url('` +
          img +
          `') center / cover;">
          <div class="content-label bg-black">
            <strong>A / </strong>
            <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content-a content-js" value="` +
          content_a +
          `" placeholder=" 내용(21자 이내)" name="content_a" maxlength="21" autocomplete="off" required>
          </div>
          <div class="w-100 h-100 img-menu-on" data-csrfmiddlewaretoken="` +
          csrfmiddlewaretoken +
          `" data-aorb="a">
          </div>
          <input type="hidden" name="img_url_a" value="` +
          img +
          `">
        </div>
      `
      );
    } else if (aorb === "b") {
      content_b = document.getElementsByClassName("content-b")[0].value;
      $eachContent.children(".uploaded-b").remove();
      $eachContent.append(
        `
        <div class="ml-1perc demo-card-image mdl-card content-img inner uploaded-b" style="background: url('` +
          img +
          `') center / cover;">
          <div class="content-label bg-black">
            <strong>B / </strong>
            <input type="text" class="w-80 font-15 feed-input-border font-white bg-black content-b content-js" value="` +
          content_b +
          `" placeholder=" 내용(21자 이내)" name="content_b" maxlength="21" autocomplete="off" required>
          </div>
          <div class="w-100 h-100 img-menu-on" data-csrfmiddlewaretoken="` +
          csrfmiddlewaretoken +
          `" data-aorb="b">
          </div>
          <input type="hidden" name="img_url_b" value="` +
          img +
          `">
        </div>
      `
      );
    }
  });

  // 해시태그 삭제
  $(document).on("click", ".delete-tag", function(event) {
    const $this = $(this);
    const id = $this.data("feedid");
    const trid = $this.data("tagrelationid");
    $.ajax({
      type: "GET",
      url: `/feeds/${id}/delete_tag/${trid}/`,
      dataType: "json",
      success: function(data) {
        $this.prev().remove();
        $this.remove();
      },
      error: function(response, status, error) {
        alert("error");
        console.log(response, status, error);
      },
      complete: function(response) {
        console.log(response);
      }
    });
  });

  //통계 - 1st layer를 클릭 시 2nd layer 펼쳐짐
  $(document).on("click", ".stat-menu-list-each", function() {
    const $this = $(this);
    const $secondMenuWrap = $this
      .parent()
      .parent()
      .siblings(".stat-menu-second-list-wrap");
    const statMenu = $this.data("statmenu");
    let $secondMenuNew;
    $(".stat-menu-list-each").removeClass("clicked");
    $this.addClass("clicked");
    if (statMenu === "gender") {
      $secondMenuNew =
        `
        <div class="stat-menu-list" data-statmenu="` +
        statMenu +
        `">
          <div class="stat-menu-second-list-each">
            <div class="stat-name">남성</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">여성</div>
          </div>
        </div>
      `;
    } else if (statMenu === "birth") {
      $secondMenuNew =
        `
        <div class="stat-menu-list" data-statmenu="` +
        statMenu +
        `">
          <div class="stat-menu-second-list-each">
            <div class="stat-name">10대미만</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">10대</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">20대</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">30대</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">40대</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">50대이상</div>
          </div>
        </div>
      `;
    } else if (statMenu === "major") {
      $secondMenuNew =
        `
        <div class="stat-menu-list" data-statmenu="` +
        statMenu +
        `">
          <div class="stat-menu-second-list-each">
            <div class="stat-name">문과계열</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">이과계열</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">예체능계열</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">기타</div>
          </div>
        </div>
      `;
    } else if (statMenu === "mobile") {
      $secondMenuNew =
        `
        <div class="stat-menu-list" data-statmenu="` +
        statMenu +
        `">
          <div class="stat-menu-second-list-each">
            <div class="stat-name">iOS</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">Android</div>
          </div>
        </div>
      `;
    } else if (statMenu === "region") {
      $secondMenuNew =
        `
        <div class="stat-menu-list" data-statmenu="` +
        statMenu +
        `">
          <div class="stat-menu-second-list-each">
            <div class="stat-name">서울경기</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">강원</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">충청</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">호남</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">영남</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">제주</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">국내전체</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">해외</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">기타</div>
          </div>
        </div>
      `;
    } else if (statMenu === "politics") {
      $secondMenuNew =
        `
        <div class="stat-menu-list" data-statmenu="` +
        statMenu +
        `">
          <div class="stat-menu-second-list-each">
            <div class="stat-name">진보</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">중도진보</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">중도</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">중도보수</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">보수</div>
          </div>
        </div>
      `;
    } else if (statMenu === "religion") {
      $secondMenuNew =
        `
        <div class="stat-menu-list" data-statmenu="` +
        statMenu +
        `">
          <div class="stat-menu-second-list-each">
            <div class="stat-name">무교</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">기독교계열</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">불교계열</div>
          </div>
          <div class="stat-menu-second-list-each">
            <div class="stat-name">기타</div>
          </div>
        </div>
      `;
    }
    const $secondMenuBefore = $secondMenuWrap.children(".stat-menu-list");
    $secondMenuBefore.remove();
    $secondMenuWrap.append($secondMenuNew);
    $("#new-comments-next")[0].scrollIntoView(true);
  });

  //통계 - 2nd layer를 클릭 시 그래프 펼쳐짐
  $(document).on("click", ".stat-menu-second-list-each", function() {
    const $this = $(this);
    const clickedStat = $this.children(".stat-name").text();
    const statMenu = $this.parent().data("statmenu");
    const id = $this
      .parent()
      .parent()
      .parent()
      .data("feedid");
    let $graph = `
      <div class="stat-detail-result-wrap">
        <div class="stat-detail-side">
          <span>A</span>
          <span>B</span>
        </div>
        <div class="stat-detail-graph flex-center font-13">
          <div class="graph-a flex-center font-16 font-white">
          </div>
          <div class="graph-b flex-center font-16 font-white">
          </div>
        </div>
        <div class="stat-detail-num font-light">
          <span class="perc-a"></span>
          <span class="perc-b"></span>
        </div>
      </div>
    `;
    $(".stat-menu-second-list-each").removeClass("clicked");
    $this.addClass("clicked");
    console.log(clickedStat);
    console.log(statMenu);
    $.ajax({
      type: "GET",
      url: `/feeds/${id}/statistics/` + statMenu + `/` + clickedStat + `/`,
      dataType: "json",
      success: function(data) {
        $(".stat-detail-result-wrap").remove();
        $(".stat-total-info").remove();
        $this
          .parent()
          .parent()
          .after($graph);
        const total = data.count_a + data.count_b;
        const $graphBar = $(".stat-detail-result-wrap").children(
          ".stat-detail-graph"
        );
        const $percentageBar = $(".stat-detail-result-wrap").children(
          ".stat-detail-num"
        );
        $this
          .parent()
          .parent()
          .after(
            `<div class="stat-total-info font-13 mt-3 text-right">[` +
              clickedStat +
              `] ` +
              total +
              `명이 투표했습니다.</div>`
          );
        if (total > 0) {
          const percentageA = ((data.count_a / total) * 100).toFixed(0);
          const percentageB = ((data.count_b / total) * 100).toFixed(0);
          $graphBar.children(".graph-a").css({ width: "" + percentageA + "%" });
          $graphBar.children(".graph-b").css({ width: "" + percentageB + "%" });
          $percentageBar.children(".perc-a").text("" + data.count_a + "명");
          $percentageBar.children(".perc-b").text("" + data.count_b + "명");
          if (data.count_b == 0) {
            $graphBar.children(".graph-a").addClass("bg-big-win");
            $graphBar.children(".graph-a").addClass("graph-big-win");
            $graphBar.children(".graph-a").text("A만 100%");
          } else if (data.count_a == 0) {
            $graphBar.children(".graph-b").addClass("bg-big-win");
            $graphBar.children(".graph-b").addClass("graph-big-win");
            $graphBar.children(".graph-b").text("B만 100%");
          } else {
            $graphBar.children(".graph-a").addClass("text-left");
            $graphBar.children(".graph-b").addClass("text-right");
            $graphBar.children(".graph-a").text("" + percentageA + "%");
            $graphBar.children(".graph-b").text("" + percentageB + "%");
            if (data.count_b > data.count_a) {
              $graphBar.children(".graph-a").addClass("bg-lose");
              $graphBar.children(".graph-b").addClass("bg-win");
            } else {
              $graphBar.children(".graph-a").addClass("bg-win");
              $graphBar.children(".graph-b").addClass("bg-lose");
            }
          }
        } else {
          $graphBar.children(".graph-a").remove();
          $graphBar.children(".graph-b").remove();
          $graphBar.addClass("graph-none");
          $graphBar.text("투표수 1 이상부터 그래프가 나타납니다.");
        }
        $("#new-comments-next")[0].scrollIntoView(true);
        console.log("-------------");
        console.log(data.count_a);
        console.log(data.count_b);
      },
      error: function(response, status, error) {
        console.log(response, status, error);
      }
    });
  });
});
