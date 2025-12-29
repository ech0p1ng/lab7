function image_tag(img_path) {
    return $(`<img style="width: 30%;" src="${img_path}"></img>`)
}

async function getAnalytics() {
    try {
        const response = await $.ajax({
            type: 'GET',
            url: '/api/analytics/',
            contentType: 'application/json',
        });

        $('main').empty();

        $('main').append(table(response.table.name, response.table.data));

        const models = Object.values(response.table.data.model);

        models.forEach(modelName => {
            // Собираем только данные для текущей модели
            let $item = $(`<div id="${modelName}"></div>`);
            const modelData = {};
            Object.keys(response.table.data).forEach(metric => {
                modelData[metric] = {};
                Object.keys(response.table.data[metric]).forEach(idx => {
                    if (response.table.data.model[idx] === modelName) {
                        modelData[metric][idx] = response.table.data[metric][idx];
                    }
                });
            });

            // Таблица метрик
            $item.append(table(modelName, modelData));

            // Находим ROC-кривую в confussion_matrixes
            const cm = response.confussion_matrixes.find(c => c.method === modelName);
            if (cm && cm.roc_curve) {
                $item.append(image_tag(cm.roc_curve));
            } else if (response.graphs[modelName]) {
                // fallback на graphs, если нет в confussion_matrixes
                $item.append(image_tag(response.graphs[modelName]));
            }

            // Матрица ошибок
            if (cm) {
                $item.append(table(`Матрица ошибок: ${modelName}`, cm.matrix));
            }
            $('main').append($item);
        });

    } catch (xhr) {
        $('main .code-format').html('Ошибка загрузки данных');
        show_errors(xhr.responseJSON.detail);
    }
}

$(function () {
    getAnalytics();
});
