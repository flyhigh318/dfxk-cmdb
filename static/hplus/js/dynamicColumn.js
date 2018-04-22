/**
 * Created by Maureen.Daelo on 11/6/2017.
 */
$(document).ready(function () {
    dynamicColumn("select_column")
})

var selected;
function dynamicColumn(id) {

    $('#'+ id +' select').selectpicker("destroy");
    var column_name = $("#"+id).attr("column-name") //table name

    if(!column_name){
        return false
    }

    var str = "<select class='selectpicker bs-select-hidden' multiple='' data-style='btn-white'>"
    var ctr = 1
    var selected_column
    $.ajax({
        type: 'GET',
        url: '/frontend/cmdb/column_list/get_column/?column=' + column_name,
        async: false,
        dataType: 'JSON',
        success: function(data, status) {
            selected_column = data
        },
        error: function(XHR, status, errorThrown) {

        }
    });

    var selected_column_array = []
    if(selected_column.length != 0) {
        var selected_column_array = selected_column[0].fields.field_name.split(',')

        $(".table.dataTable thead th a").each(function () {
            var coltext = $(this).text()
            var colname = $(this).attr("data-column")

            if(selected_column_array.indexOf(colname) > -1){
                str += "<option value='"+colname+"' selected>"+ coltext +"</option>"
            }else {
                $(this).parent().hide()
                str += "<option value='"+colname+"'>"+ coltext +"</option>"
                $(".table.dataTable tbody tr").each(function () {
                    $(this).find('td').eq(ctr).hide()
                })
            }
            ctr++
        })
    }else{
        $(".table.dataTable thead th a").each(function () {
            var coltext = $(this).text()
            var colname = $(this).attr("data-column")
            str += "<option value='"+colname+"' selected>"+ coltext +"</option>"
        })
    }


    str += "</select>"
    $("#" + id).html(str)


    $('#'+ id +' select').selectpicker()
    $('#'+ id +' .btn.dropdown-toggle.btn-white').removeAttr("title")
    $('#'+ id +' .btn.dropdown-toggle.btn-white').html("<i class='glyphicon glyphicon-th-large'></i>")
    selected = $('#'+ id +' select').val()
    $('#'+ id +' ul.dropdown-menu').on("click",function () {
        setTimeout(function () {
            selected = $('#'+ id +' select').val()
            if (selected == null){selected=[]}
            var ctr2 = 1
            $(".table.dataTable thead th a").each(function () {

                var colname = $(this).attr("data-column")
                if(selected.indexOf(colname) > -1){
                    $(this).parent().show()
                    $(".table.dataTable tbody tr").each(function () {
                        $(this).find('td').eq(ctr2).show()

                    })
                }else {
                    $(this).parent().hide()
                    $(".table.dataTable tbody tr").each(function () {
                        $(this).find('td').eq(ctr2).hide()
                    })
                }

                ctr2++
            })
        },500)

    })


    var str2 = "<div class='pull-right' style='padding-right: 5px'>" +
        "<button class='btn btn-xs btn-danger' style='margin-right: 5px'>Cancel</button>" +
        "<button class='btn btn-xs btn-primary' onclick=saveColumn('"+column_name+"')>Save</button></div>"
    $("#"+ id +" div.dropdown-menu ul").append(str2)

}//dynamicColumn

function saveColumn(column_name) {
    var field_name = selected
    $.ajax({
        type: 'GET',
        url: '/frontend/cmdb/column_list/update_column/?table_name=' + column_name + '&field_name=' + field_name,
        async: false,
        dataType: 'JSON',
        success: function(data, status) {
            selected_column = data
        },
        error: function(XHR, status, errorThrown) {

        }
    });
}//saveColumn