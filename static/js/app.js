var data = []
var token = ""

function truncateString(str) {
    num = 85
    if (str.length <= num)
        return str
    return str.slice(0, num) + '...'
}
function truncateScore(str) {
    num = 6
    return String(str).slice(0, num)
}

jQuery(document).ready(function () {
    var slider = $('#max_sentences')
    slider.on('change mousemove', function (evt) {
        $('#label_max_sentences').text('Top k sentences: ' + slider.val())
    })

    $('#btn-process').on('click', function () {

        $.ajax({
            url: '/get_predictions',
            type: "post",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({
                "input_corpus": $('#input_corpus').val(),
                "input_query": $('#input_query').val(),
                "split_token": $('#split_token').val(),
                "top_k": slider.val(),
            }),
            beforeSend: function () {
                $('#output').hide()
                $('.overlay').show()
                $('#output-use').empty()
                $('#output-bm25').empty()
                $('#output-sentenceBERT').empty()
                $('#output-bert').empty()
                $('#output-roberta').empty()
                $('#output-infersent').empty()
            },
            complete: function () {
                $('.overlay').hide()
                $('#output').show()
            }
        }).done(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
            meta_info = jsondata['meta_info']            
            for(var model_info of meta_info) {
                var content = ""
                model = model_info['name']
                desc = model_info['desc']

                for (i = 0; i < jsondata[model+'_sentences'].length; i++) {
                    cor = i % 2
                    el = `<p class='cor_${cor}'>
                        <b>Score: ${truncateScore(jsondata[model+'_scores'][i])}</b><br>
                        ${truncateString(jsondata[model+'_sentences'][i])}</p>`                    
                    content = content.concat(el)
                }
                el = `<p class='cor_${jsondata[model+'_sentences'].length%2}'>
                    <b>Elapsed: ${(jsondata[model+'_elapsed'])}</b>
                    </p>`                
                content = content.concat(el)
                result = `<div class="form-group col-md-6">
                            <label>${desc}</label>
                            <div class="output-container" id="output-${model}">${content}</div>
                        </div>` 
                $('#output_content').append(result)               
            }

        }).fail(function (jsondata, textStatus, jqXHR) {
            console.log(jsondata)
        });
    })
})