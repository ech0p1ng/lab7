/// <reference types="jquery" />

const header = $(`
    <header>
        <ul>
            <li id="main"><a class="button" href="/">Главная</a></li>
            <li id="analytics"><a class="button" href="/analytics">Аналитика</a></li>
            <li id="about"><a class="button" href="/about">О программе</a></li>
        </ul>
    </header>
`);

function goto_mainpage() {
    window.location.href = '/';
}

function goto_page(page_url) {
    window.location.href = page_url;
}

$(function () {
    if (getAuthToken()) {
        let logout_button = $(`<li id="logout"><span class="button">Выход</span></li>`)
        header.find('ul').append(logout_button);
        logout_button.find('span').on('click', () => {
            removeAuthToken();
            goto_mainpage();
        })
    }
    else {
        const register_button = $(`<li id="register"><a class="button" href="/register">Регистрация</a></li>`);
        const signin_button = $(`<li id="signin"><a class="button" href="/sign-in">Вход</a></li>`);
        header.find('ul').append(register_button);
        header.find('ul').append(signin_button);
    }
    $('body').prepend(header);
    $(window).trigger('html-loaded');
});


function show_errors(detail) {
    let messages = "";
    detail.forEach(d => {
        messages += d.msg + "\n";
    });
    alert(messages);
    console.log(messages)
}