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


  })