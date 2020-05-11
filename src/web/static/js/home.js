$(function(){

    $('#refreshToken').on('click', function(){
        var $form = $(this).closest('form');
        $.get('/refresh_token').done(function(authResult){
            $form.find('#accessToken').val(authResult.accessToken);
            $form.find('#expiresOn').text(authResult.expiresOn || '');
        })
    });

    $('#getresources').on('click', function(){
        var $form = $(this).closest('form');
        $.get('/user_groups').done(function(){
           
  
        });
    })
});