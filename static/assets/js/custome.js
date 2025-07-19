$(document).ready(function () {
    $('#search-input').keyup(function () {
        var query = $(this).val();
        $.ajax({
            url: "{% url 'search_product' %}",
            data: {
                'search': query
            },
            dataType: 'json',
            success: function (data) {
                $('#product-table-body').empty();
                if (data.products.length > 0) {
                    data.products.forEach(function (product) {
                        var row =


                            '<div class="col-md-4"><a href=""> <div class="card text-center p-3 hover-card-class"> <h4>' + product.name + '</h4><h6>Price:' + product.price + '(' + product.tax + ')' + '</h6><p>Stock:' + product.stock + '</p></div></a></div>';


                        $('#product-table-body').append(row);
                    });
                } else {
                    $('#product-table-body').append('<tr><td colspan="5">No products found</td></tr>');
                }
            },
            error: function (xhr, status, error) {
                console.error('AJAX Error:', status, error);
            }
        });
    });
});



// for select input 

// $(document).ready(function () {
//     $('#mmySelect').select2({
//         placeholder: "Select an option",
//         allowClear: true
//     });
// });


$(document).ready(function () {
    if (typeof $.ui !== 'undefined') {
        console.log("jQuery UI loaded successfully.");
    } else {
        console.log("Error: jQuery UI not loaded.");
    }

    var customers = [
        {% for customer in customer %}
        {
            id: "{{ customer.id }}",
            value: "{{ customer.name }}",
            label: "{{ customer.name }}",
            contact: "{{ customer.phone }}",
            gst: "{{ customer.gst_number }}",
            address: "{{ customer.city }}, {{ customer.state }}, {{ customer.country }} - {{ customer.pincode }}"
        },
        {% endfor %}
    ];

    console.log("Customer data:", customers);

    $("#customerInput").autocomplete({
        source: customers,
        select: function (event, ui) {
            var selectedCustomer = ui.item;
            console.log("Selected customer details:", selectedCustomer);

            // Set the input field value to the selected customer's name
            $("#customerInput").val(selectedCustomer.label);

            // Perform an AJAX request to update the order's customer field
            updateOrderCustomer(selectedCustomer.id);

            // Prevent the default autocomplete behavior (which may replace the input value)
            return false;
        }
    }).on("focus", function() {
        // Clear the input field when it is clicked
        $(this).val("");
    });

    function updateOrderCustomer(customerId) {
        console.log("Updating order with customer ID:", customerId); // Debug log
        $.ajax({
            url: "{% url 'update_order_customer' %}",
            type: "POST",
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}',
                order_id: $("#orderId").val(),
                customer_id: customerId
            },
            success: function(response) {
                console.log("Order customer updated successfully.");
                // Optionally, update the UI or provide feedback to the user
                $("#customerdetails").html(response.html);
            },
            error: function(xhr, errmsg, err) {
                console.log("Error updating order customer:", errmsg);
            }
        });
    }
});