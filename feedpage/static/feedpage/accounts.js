$(document).ready(() => {

  // 프로필수정 페이지에서 select 버튼 바뀔 때
  $('.select-form').on('change', function() {
    if ($(this).val()) {
      return $(this).addClass('font-black');
    }
  });
  
  const regionValue = $('select[name="region"]').data('region');
  const genderValue = $('#gender').data('gender');
  const majorValue = $('#major').data('major');
  const mobileValue = $('#mobile').data('mobile');
  const politicsValue = $('#politics').data('politics');
  const religionValue = $('#religion').data('religion');
  const $regionSelected = $('select option[value="'+regionValue+'"]');
  $regionSelected.attr("selected",true);
  $regionSelected.parent().addClass("font-black");
  $('input:radio[name=gender]:input[value=' + genderValue + ']').attr("checked", true);
  $('input:radio[name=major]:input[value=' + majorValue + ']').attr("checked", true);
  $('input:radio[name=mobile]:input[value=' + mobileValue + ']').attr("checked", true);
  $('input:radio[name=politics]:input[value=' + politicsValue + ']').attr("checked", true);
  $('input:radio[name=religion]:input[value=' + religionValue + ']').attr("checked", true);
  

  //for profile_image
  $('.img-prf').on('change', function() {
    const $this = $(this)
    const $profileDiv = $this.parent();
    if(window.FileReader && $this[0].files[0]){
      var reader = new FileReader();
      reader.onload = function(e) {
        img = e.target.result;
        console.log("profile image changed")
        $profileDiv.children('.creator-img').remove();
        $profileDiv.prepend(`
        <div class="creator-img" style="background: url('`+img+`') center / cover;">
          <label class="photo-edit-btn" for="profile_image">
            <i class="material-icons" style="font-size: 13px;">photo_camera</i>
          </label>
        </div>
        `); 

      }
      reader.readAsDataURL($this[0].files[0]);
    } else {
      console.log('cancel editing profile picture');
    }
  });

//프로필 수정 제출
  $(document).on('click', '#profile-submit-btn', function(event) {
    event.preventDefault();

    const $this = $(this);
    const csrfmiddlewaretoken = $this.data('csrfmiddlewaretoken');
    const formData = new FormData($('#profile-form')[0]);

    $.ajax({
      type: "POST",
      enctype: 'multipart/form-data',
      url: `/accounts/profile/`,
      data: formData,
      processData: false,
      contentType: false,
      cache: false,
      timeout: 600000,
      dataType: "json",
      csrfmiddlewaretoken: csrfmiddlewaretoken,
      success: function (data) {
        const isSuccess = data.comment.is_success
        const isNewPremium = data.comment.is_new_premium
        const restInfoNum = data.comment.rest_info_num
        if (isSuccess) {
          const $lastMsg = $('#last-msg');
          if (isNewPremium) {
            $('#promote-msg').remove();
            $('#last-msg').text('이제, Premium user가 되셨습니다!');
            $('.version-status').text('Premium user입니다!')
            setTimeout(function() {
              location.reload();
            }, 2000);  
          } else if (isSuccess == true && restInfoNum > 0) {
            $lastMsg.text('성공적으로 반영되었습니다! 앞으로 딱 '+restInfoNum+'개만 더 채워주시면 Premium user가 됩니다.');
            $lastMsg.addClass('font-mid');
          } else {
            $lastMsg.text('성공적으로 반영되었습니다!');
            $lastMsg.addClass('font-mid');            
          }
        } else {
          const $CreatorSub = $('#creator-profile-email');
          $CreatorSub.addClass('font-red font-mid');
          $CreatorSub.text('사용할 수 없는 닉네임입니다.');
          $('.creator-name-edit').focus();
        }
      },

      error: function (e) {
          console.log("ERROR : ", e);
      }
    });
  })
})