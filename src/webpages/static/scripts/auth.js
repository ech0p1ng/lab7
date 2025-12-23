/// <reference types="jquery" />

function registration(user_name, password) {
    alert(user_name, password);
    // $.post('/api/auth/registration')
}

$(window).on('load', () => {
    $('#registration.submit').on('click', registration(
        $('#registration.login').text(),
        $('#registration.password').text()
    ));
});