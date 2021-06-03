//
// // $(#staticBackdrop_2).on("click", 'input[type="submit"]', (e) ->
// //   modal.modal('show')
// //
//
// // $('#staticBackdrop_2').on('hidden.bs.modal', function() {
// //     return false;
// //   });
//
//
// // $('#mymodal').on('hidden.bs.modal', function() {
// //   this.modal('show');
// // });
//
// //
// // $( "#new_record_form" ).submit(function( event ) {
// //   event.preventDefault();
// // });
//
// //
// //
// // function overlay() {
// //     el = document.getElementById("staticBackdrop_2");
// //
// //     el.style.visibility =
// //         (el.style.visibility == "visible" ? "hidden" : "visible");
// //
// //     document.getElementById("#submit_new_record").addEventListener("click",
// //         function(event){
// //             event.preventDefault();
// //         }
// //     );
// // }
// //
// //
// // $.ajax({
// //     url: '/archef/store/',
// //     type: 'default GET (Other values: POST)',
// //     dataType: 'default: Intelligent Guess (Other values: xml, json, script, html)',
// //     data: {param1: 'value1'},
// // }).done(function() {
// //     console.log("success");
// // }).fail(function() {
// //     console.log("error");
// // }).always(function() {
// //     console.log("complete");
// // });
//
//
//
//
// $('#new_record_form').on('submit', function() {
//   $(#staticBackdrop_2).on('hide.bs.modal', function ( e ) {
//     e.preventDefault();
//   })
// });



$(function(){
    $('#new_record_form').submit(function(event){

        event.preventDefault();
        var form = $(this);
        console.log(form.serialize());

    });

})