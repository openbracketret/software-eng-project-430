$(function() {

    if (!localStorage.getItem("token") && !window.location.href.includes("login")) {
        window.location.href = "/login.html";
    }

    let baseApiURL = "http://api.luke-soft.me:8000/api/v1/"


    // Index Page

    $("#customer-submit").click(function() {
        
        let data = {
            "id_number": $("#customer-id-no").val(),
            "contact_number": $("#customer-contact").val(),
            "first_name": $("#customer-firstname").val(),
            "surname": $("#customer-surname").val(),
            "address": $("#customer-address").val()
        }
        // $("#index-modal").modal("toggle");
        $.ajax({
            type: "POST",
            url: baseApiURL + "script_actions/add_customer/",
            data: data,
            headers: {
                "Authorization": "Token " + localStorage.getItem("token")
            },
            success: function (response) {
                if (response.success == true){
                    $("#index-modal-title").html("<h2>Customer added</h2>");
                    $("#new-customer-id-no").val($("#customer-id-no").val());
                    $("#redeem-customer-id-no").val($("#customer-id-no").val());
                    $("#index-modal").modal("toggle");
                } else {
                    $("#index-modal-title").html("<h2>An Error Occured</h2>");
                    $("#index-modal").modal("toggle");
                }
            }
        });

    });


    $("#new-submit").click(function() {
        var formData = new FormData();
        var file = $("#new-file").prop('files')[0];
        formData.append("file", file);
        formData.append("max_redeems", $("#new-max-redeems").val());
        formData.append("customer_id_number", $("#new-customer-id-no").val());
        $.ajax({
            type: "post",
            url: baseApiURL + "external_actions/upload_script/",
            processData: false,
            contentType: false,
            data: formData,
            headers: {
                "Authorization": "Token " + localStorage.getItem("token")
            },
            success: function(response) {
                if (response.success == true) {
                    $("#index-modal-title").html("<h2>File added</h2>");
                    $("#index-modal").modal("toggle");
                } else {
                    $("#index-modal-title").html("<h2>An error occurred</h2>");
                    $("#index-modal").modal("toggle");
                }
            }
        });


    });

    $("#redeem-submit").click(function() {
        $.ajax({
            type: 'post',
            url: baseApiURL + "script_actions/redeem_script/",
            data: {
                customer_id_number: $("#redeem-customer-id-no").val(),
                script_id: $("#redeem-script-id").val()
            },
            headers: {
                "Authorization": "Token " + localStorage.getItem("token")
            },
            success: function(response) {
                if (response.success == true) {
                    $("#index-modal-title").html("<h2>Script Redeemed</h2>");
                    $("#index-modal").modal("toggle");
                } else {
                    $("#index-modal-title").html("<h2>An error occurred</h2>");
                    $("#index-modal").modal("toggle");
                    console.log(response);
                }
            }
        });
    });


    $("#redeem-search").click(function() {

        $.ajax({
            type: 'post',
            url: baseApiURL + "script_actions/check_for_existing_script/",
            data: {
                id_number: $("#redeem-customer-id-no").val()
            },
            headers: {
                "Authorization": "Token " + localStorage.getItem("token")
            },
            success: function(response) {
                if (response.success == true) {
                    $("#index-modal-title").html("<h2>Script Found</h2>");
                    $("#index-modal").modal("toggle");
                    $("#redeem-script-id").val(response.payload.id);
                } else {
                    $("#index-modal-title").html("<h2>An error occurred</h2>");
                    $("#index-modal").modal("toggle");
                }
            }
        });

    });

    // Login Page

    $("#login-submit").click(function() {

        let data = {
            "username": $("#login-username").val(),
            "password": $("#login-password").val()
        }
        // console.log(data);

        $.ajax({
            type: "POST",
            url: "http://api.luke-soft.me:8000/auth-token/",
            data: data,
            success: function (response) {
                console.log("success");
                console.log(response);
                localStorage.setItem("token", response.token);
                window.location.href = '/index.html';
            },
            error: function(response) {
                if (response.status === 200) {
                    let responseData = JSON.parse(response.responseText);
                    localStorage.setItem("token", responseData.token);
                    console.log(responseData.token)
                    console.log("token set");
                    window.location.href = '/index.html';
                } else {
                    console.log(response);
                    alert(response);
                }
            }
        });

    });

    // External User Register

    $("#external-submit").click(function() {

        $("#index-modal-title").html("<h2>External User Registered</h2>");
        $("#index-modal").modal("toggle");

    });

});