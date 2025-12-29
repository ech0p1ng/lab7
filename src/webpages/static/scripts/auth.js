/// <reference types="jquery" />

const AUTH_TOKEN_EXPIRE_DAYS = 3;

async function sign_in(user_name = "", password = "") {
    data = {
        'role_id': 2,
        'user_name': user_name,
        'password': password
    }

    try {
        const response = await $.ajax({
            type: 'POST',
            url: '/api/auth/login',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json',
        });
        setAuthToken(response.access_token, AUTH_TOKEN_EXPIRE_DAYS);
    } catch (xhr) {
        show_errors(xhr.responseJSON.detail);
        return;
    }
    goto_mainpage();

}


async function registration(user_name = "", password = "") {
    data = {
        'role_id': 2,
        'user_name': user_name,
        'password': password
    }
    try {
        await $.ajax({
            type: 'POST',
            url: '/api/auth/registration',
            data: JSON.stringify(data),
            dataType: 'json',
            contentType: 'application/json',
        });
        goto_page('/sign-in')
        // await sign_in(user_name, password);
    } catch (xhr) {
        show_errors(xhr.responseJSON.detail);
    }
}

function redirect_signedin() {
    if (getAuthToken()) {
        goto_mainpage();
    }
}

$(function () {
    $('#registration.auth-form').on('load', redirect_signedin);
    $('#sign-in.auth-form').on('load', redirect_signedin);
    
    $('#registration .submit').on('click', () => {
        registration(
            $('#registration #login').val(),
            $('#registration #password').val()
        )
    });

    $('#sign-in .submit').on('click', () => {
        sign_in(
            $('#sign-in #login').val(),
            $('#sign-in #password').val()
        );
    });

});