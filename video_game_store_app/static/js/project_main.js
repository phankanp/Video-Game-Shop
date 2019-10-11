$(document).ready(function() {
  $("#same_billing_address").change(function() {
    if (this.checked) {
      $("#billing-details").addClass("disabled");
      $("#billing-details").fadeOut("slow");
    }

    if (this.checked != true) {
      $("#billing-details").fadeIn("slow");
    }
  });
});

$(document).on("submit", "#checkoutForm", function(e) {
  e.preventDefault();

  var serializedData = $(this).serialize();

  $.ajax({
    type: "POST",
    action: "{% url 'checkout' %}",
    data: serializedData,
    success : function(response){
       // meaning that everyhting went ok
        $("#exampleModal").modal("show");
    },
    error : function(response){
      window.location.href='checkout'
    }
  });
});
