//Nunca subir pra produção com o endereço local, sempre o de produção deve estar ativo
function get_url(){

    return "http://127.0.0.1:8000";
}

async function get_periodo_setores(){
    let result;

    try{
        result = await $.ajax({

            url: get_url()+"/api/v1/dashboard/get_periodo_setores",
            type: "GET",
            contentType: "application/json",
        });

    } catch(error){
        console.log(error)
    }

    return result;
}

async function get_periodo_portes(){
    let result;

    try{
        result = await $.ajax({

            url: get_url()+"/api/v1/dashboard/get_periodo_portes",
            type: "GET",
            contentType: "application/json",
        });

    } catch(error){
        console.log(error)
    }

    return result;
}

async function create_html_periodos(){

    let dataset_setores = await get_periodo_setores()
    let dataset_portes = await get_periodo_portes()

    $('#periodo-ini-setores').empty();
    $('#periodo-fim-setores').empty();
    $('#periodo-ini-portes').empty();
    $('#periodo-fim-portes').empty();
    
    $.each(dataset_setores.msg, function(k, v) {
        $("#periodo-ini-setores").append(new Option(formata_data(v[1], 1), v[0]));
        $("#periodo-fim-setores").append(new Option(formata_data(v[1], 1), v[0]));
    });

    $.each(dataset_portes.msg, function(k, v) {
        $("#periodo-ini-portes").append(new Option(formata_data(v[1], 1), v[0]));
        $("#periodo-fim-portes").append(new Option(formata_data(v[1], 1), v[0]));
    });
}

async function get_dash_cresc_dec_set(dataset){
    let result;

    try{
        result = await $.ajax({

            url: get_url()+"/api/v1/dashboard/get_dash_cresc_dec_set",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(dataset),
        });

    } catch(error){
        console.log(error)
    }

    return result;
}

async function get_dash_porte_set(dataset){
    let result;

    try{
        result = await $.ajax({

            url: get_url()+"/api/v1/dashboard/get_dash_porte_set",
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify(dataset),
        });

    } catch(error){
        console.log(error)
    }

    return result;
}

async function render_dash_cresc_dec_set(){

    $('.div-carousel-1-0').empty();
    $('.div-carousel-1-1').empty();
    var dataset = {"data_ini": $("#periodo-ini-setores").val(),
                   "data_fim": $("#periodo-fim-setores").val()};

    if(dataset.data_ini == dataset.data_fim){
        alert("Não pode realizar pesquisa de duas datas iguais.")

    } else {

        const dados = await get_dash_cresc_dec_set(dataset);
        
        for(var x = 0; x < dados.msg.length; x++){

            const numberOfCharts = Math.ceil(dados.msg[x][0].length / 5); // Cada carrossel terá 10 itens

            for (let i = 0; i < numberOfCharts; i++) {
                const slicedData = dados.msg[x][0].slice(i * 5, (i + 1) * 5); // Carrossel com 10 itens

                const chartData = create_dash_cresc_dec_set(slicedData);
                
                const canvas = $('<canvas id="chart1' + x + i + '"></canvas>');
                $('.div-carousel-1-'+x).append(canvas);

                const ctx = document.getElementById('chart1' + x + i).getContext('2d');
                const myChart = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    
                    options: {
                        indexAxis: 'x',
                        scales: {
                            x: { stacked: false },
                            y: { stacked: false }
                        }
                    }
                });
   
            }
            $('.div-carousel-1-'+x).slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: true,
                autoplaySpeed: 10000,
                arrows: true,
                dots: true,
                infinite: true
            });
        }
    }
}

async function render_dash_porte_set(){

    $('.div-carousel-2-0').empty();
    $('.div-carousel-2-1').empty();

    var dataset = {"data_ini": $("#periodo-ini-portes").val(),
                   "data_fim": $("#periodo-fim-portes").val()};

    if(dataset.data_ini == dataset.data_fim){
        alert("Não pode realizar pesquisa de duas datas iguais.")

    } else {

        const dados = await get_dash_porte_set(dataset);
        
        for(let x = 0; x < dados.msg.length; x++){

            const numberOfCharts = Math.ceil(dados.msg[x][0].length / 5); // Cada carrossel terá 10 itens

            for (var i = 0; i < numberOfCharts; i++) {

                const slicedData = dados.msg[x][0].slice(i * 5, (i + 1) * 5); // Carrossel com 10 itens
                
                const chartData = create_dash_porte_set(slicedData);

                const canvas = $('<canvas id="chart2' + x + i + '"></canvas>');
                $('.div-carousel-2-'+x).append(canvas);

                const ctx = document.getElementById('chart2' + x + i).getContext('2d');
                const myChart = new Chart(ctx, {
                    type: 'bar',
                    data: chartData,
                    options: {
                        indexAxis: 'x',
                        scales: {
                            x: { stacked: false },
                            y: { stacked: false }
                        }
                    }
                });
            }
            $('.div-carousel-2-'+x).slick({
                slidesToShow: 1,
                slidesToScroll: 1,
                autoplay: true,
                autoplaySpeed: 10000,
                arrows: true,
                dots: true,
                infinite: true
            });
        }
    }
}

function create_dash_cresc_dec_set(dados) {
    
    const dataBySector = {
        labels: dados.map(item => item.setor),
        datasets: [{
            label: 'Quantidade de empresas por Setor',
            data: dados.map(item => item.qtd_porte),
            backgroundColor: getRandomColor(),
        }]
    };
    return dataBySector;
}

function create_dash_porte_set(dados) {

    const dataBySector = {
        labels: dados.map(item => item.setor),
        datasets: dados[0].portes.split(',').map((cat, index) => {
            return {
                label: cat.trim(), // Remover espaços extras
                data: dados.map(item => convertStringToNumbers(item.qtd_porte)[index]),
                backgroundColor: getRandomColor(),
                
            };
        })
    };
    return dataBySector;
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function convertStringToNumbers(str) {
    return str.split(',').map(Number);
}

function formata_data(data, day=0){

    try{
        if(data != null){
            var new_date = new Date(new Date(data).setDate(new Date(data).getDate() + day));
            return new_date.toLocaleDateString("pt-br");
        }
    } catch {
        return "";
    }
}