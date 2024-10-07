
$(document).ready(function () {
    var table = $('#datatablesSimple').DataTable({
        language: {
            "decimal": ",",
            "emptyTable": "No hay datos disponibles en la tabla",
            "info": "Mostrando _START_ a _END_ de _TOTAL_ entradas",
            "infoEmpty": "Mostrando 0 a 0 de 0 entradas",
            "infoFiltered": "(filtrado de _MAX_ entradas totales)",
            "lengthMenu": "Mostrar _MENU_ entradas",
            "loadingRecords": "Cargando...",
            "processing": "Procesando...",
            "search": "Buscar:",
            "zeroRecords": "No se encontraron coincidencias",
            "paginate": {
                "first": "Primero",
                "last": "Último",
                "next": "Siguiente",
                "previous": "Anterior"
            }
        }
    });


    function formatCurrency(amount) {
        // Formatea a cpl
        return new Intl.NumberFormat('es-CL', {
            style: 'currency',
            currency: 'CLP'
        }).format(amount);
    }

    function calcularTotales() {

        var totalMensual = Array(table.columns().header().length - 1).fill(0); 
        

        table.rows().every(function () {
            var data = this.data();

            for (var i = 1; i <= totalMensual.length; i++) {
                var valor = parseFloat(data[i]) || 0;
                console.log(valor)
                totalMensual[i - 1] += valor; 

                data[i] = formatCurrency(valor)
            }

           
            this.data(data);


        });

        

        $('#filaTotales').find('th').slice(1).remove();

        totalMensual.forEach(function (total) {
            var formattedTotal = formatCurrency(total);
            $('#filaTotales').append('<th data-dt-column="1" rowspan="1" colspan="1" class="dt-type-numeric dt-orderable-asc dt-orderable-desc" tabindex="0"><span class="dt-column-title"</span><span class="dt-column-order"></span>' + formattedTotal + '</th>');
        });
    }

   

    calcularTotales();

    table.on('draw', function () {
        calcularTotales();
    });
});

