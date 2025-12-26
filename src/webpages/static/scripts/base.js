/// <reference types="jquery" />

const header = $(`
    <header>
        <ul>
            <li><a class="button" href="/">Главная</a></li>
            <li><a class="button" href="/analytics">Аналитика</a></li>
            <li><a class="button" href="/about">О программе</a></li>
            <li><a class="button" href="/register">Регистрация</a></li>
        </ul>
    </header>
`);

function goto_mainpage() {
    window.location.href = '/';
}

function goto_page(page_url) {
    window.location.href = page_url;
}

$(window).on('load', () => {
    $('body').prepend(header);
    $(window).trigger('html-loaded');
});