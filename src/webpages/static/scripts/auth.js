/// <reference types="jquery" />

const AUTH_TOKEN_EXPIRE_DAYS = 3;

$(document).on('load', () => {
    if ((getAuthToken())) {
        goto_mainpage();
    }
})

async function sign_up(user_name, password) {
    data = {
        'user_name': user_name,
        'password': password
    }
    let response = await $.ajax({
        type: 'POST',
        url: '/api/auth/login',
        data: JSON.stringify(data),
        dataType: 'json',
        contentType: 'application/json'
    });

    setAuthToken(response.access_token, AUTH_TOKEN_EXPIRE_DAYS);
    goto_mainpage();
}


async function registration(user_name, password) {
    data = {
        'user_name': user_name,
        'password': password
    }
    try {
        var response = await $.ajax({
            type: 'POST',
            url: '/api/auth/registration',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json',
        });
        // goto_page('/sign-up');
        // await sign_up(user_name, password);
    } catch (xhr) {
        console.error(xhr.responseJSON.detail);
        alert(xhr.responseJSON.detail);
    }
}


$(window).on('load', () => {
    $('#registration .submit').on('click', () => {
        registration(
            $('#registration #login').val(),
            $('#registration #password').val()
        )
    });
});

$(window).on('load', () => {
    $('#sign-up .submit').on('click', () => {
        sign_up(
            $('#sign-up #login').val(),
            $('#sign-up #password').val()
        )
    });
});