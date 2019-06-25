$(document).ready(() => {
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
    $('input:radio[name=likes_iphone]:input[value=' + mobileValue + ']').attr("checked", true);
    $('input:radio[name=politics]:input[value=' + politicsValue + ']').attr("checked", true);
    $('input:radio[name=religion]:input[value=' + religionValue + ']').attr("checked", true);
  
    // 프로필수정 페이지에서 select 버튼 바뀔 때
    $('select').on('change', function() {
      if ($(this).val()) {
        return $(this).addClass('font-black');
      }
    });
  
    // $('.date-form').on('change', function() {
    //   if ($(this).val()) {
    //     return $(this).addClass('font-black');
    //   }
    // });
  
  })