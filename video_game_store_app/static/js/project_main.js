
  $(document).ready(function()
  {
    $('#same_billing_address').change(function() 
    {
      if(this.checked)
      {
          $('#billing-details').addClass('disabled')
          $('#billing-details').fadeOut( "slow" )
      }

      
      if(this.checked != true)
      {
          $('#billing-details').fadeIn( "slow" )
      }
    });   
  });